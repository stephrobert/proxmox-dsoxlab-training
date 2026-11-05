"""Mesures communes des labs mono-nœud, avec refus des lectures impossibles."""

from __future__ import annotations

import json
import re
import shlex
import subprocess
import time
import warnings

from conftest import message


def run_command(host, command):
    try:
        return host.run(command)
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        raise AssertionError(message(
            en=f"The check command could not complete: {command}\n{exc}",
            fr=f"La commande de contrôle n'a pas pu aboutir : {command}\n{exc}",
        )) from exc


def read(host, command):
    result = run_command(host, command)
    assert result.rc == 0, message(
        en=f"The check command failed: {command}\n{result.stdout}\n{result.stderr}",
        fr=f"La commande de contrôle a échoué : {command}\n{result.stdout}\n{result.stderr}",
    )
    return result.stdout.strip()


def read_json(host, command, expected_type):
    output = read(host, command)
    try:
        value = json.loads(output)
    except (ValueError, TypeError) as exc:
        raise AssertionError(message(
            en=f"Unreadable JSON from {command}: {output!r}",
            fr=f"JSON illisible avec {command} : {output!r}",
        )) from exc
    assert isinstance(value, expected_type), message(
        en=f"Unexpected measurement format from {command}.",
        fr=f"Format de mesure inattendu avec {command}.",
    )
    return value


def config(host, tool, identifier):
    output = read(host, f"{tool} config {identifier}")
    values = dict(line.split(":", 1) for line in output.splitlines() if ":" in line)
    values = {key.strip(): value.strip() for key, value in values.items()}
    assert values, message(
        en=f"Create {tool} guest {identifier} before checking its properties.",
        fr=f"Créez l'invité {tool} {identifier} avant de contrôler ses propriétés.",
    )
    return values


def options(value):
    return dict(part.split("=", 1) for part in value.split(",") if "=" in part)


def require_equal(actual, expected, label):
    assert actual == expected, message(
        en=f"Set {label} to {expected!r}; observed {actual!r}.",
        fr=f"Réglez {label} à {expected!r} ; valeur observée : {actual!r}.",
    )


def witness(host, directory, kind, identifier):
    nonce = host.file(f"{directory}/nonce").content_string.strip()
    assert nonce, message(
        en="The lab nonce is missing: run the lab preparation again.",
        fr="Le nonce du lab est absent : rejouez sa préparation.",
    )
    return f"temoin {nonce} {kind} {identifier}"


def page(host, address):
    return read(host, f"curl --fail --silent --show-error --max-time 5 http://{address}:8080/")


def require_page(host, address, expected):
    assert expected in page(host, address).splitlines(), message(
        en=f"Serve the exact witness line from http://{address}:8080/.",
        fr=f"Servez la ligne témoin exacte depuis http://{address}:8080/.",
    )


def require_guest_page(host, tool, identifier, address, expected):
    """Le contenu doit dépendre de l'interface de l'invité réellement noté."""
    require_page(host, address, expected)
    interface = f"{'veth' if tool == 'pct' else 'tap'}{identifier}i0"
    links = read_json(host, f"ip -j link show dev {interface}", list)
    assert len(links) == 1 and "UP" in links[0].get("flags", []), message(
        en=f"Start guest interface {interface} before checking its service.",
        fr=f"Activez l'interface invitée {interface} avant de contrôler son service.",
    )
    try:
        read(host, f"ip link set dev {interface} down")
        links = read_json(host, f"ip -j link show dev {interface}", list)
        assert len(links) == 1 and "UP" not in links[0].get("flags", []), message(
            en="The service-origin measurement could not isolate the guest interface.",
            fr="La mesure d'origine du service n'a pas pu isoler l'interface invitée.",
        )
        result = run_command(host, f"curl --silent --show-error --max-time 5 --output /dev/null --write-out '%{{http_code}}' http://{address}:8080/")
        assert result.rc in (0, 7, 28), message(
            en=f"Cannot measure service origin: curl returned {result.rc}: {result.stderr}",
            fr=f"Impossible de mesurer l'origine du service : curl retourne {result.rc} : {result.stderr}",
        )
        assert result.rc in (7, 28) and result.stdout.strip() == "000", message(
            en="The HTTP response survives guest-interface isolation: serve it from the assigned guest.",
            fr="La réponse HTTP survit à l'isolement de l'interface invitée : servez-la depuis l'invité attribué.",
        )
    finally:
        cleanup(host, f"ip link set dev {interface} up")
    wait_page(host, address, expected)


def wait_state(host, tool, identifier, expected, seconds=120):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        state = read(host, f"{tool} status {identifier}")
        if state == f"status: {expected}":
            return
        time.sleep(2)
    raise AssertionError(message(
        en=f"Guest {identifier} never reached state {expected}.",
        fr=f"L'invité {identifier} n'a pas atteint l'état {expected}.",
    ))


def restart(host, tool, identifier):
    """Constater l'arrêt avant de démarrer : une page déjà en ligne ne suffit pas."""
    read(host, f"{tool} shutdown {identifier} --timeout 120")
    wait_state(host, tool, identifier, "stopped")
    read(host, f"{tool} start {identifier}")
    wait_state(host, tool, identifier, "running")


def wait_page(host, address, expected, seconds=240):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        result = run_command(host, f"curl --fail --silent --show-error --max-time 5 http://{address}:8080/")
        if result.rc == 0 and expected in result.stdout.splitlines():
            return
        time.sleep(3)
    raise AssertionError(message(
        en=f"Restore the witness service after restarting guest {address}.",
        fr=f"Rétablissez le service témoin après le redémarrage de l'invité {address}.",
    ))


def cleanup(host, command):
    """Ne jamais remplacer l'échec pédagogique par celui du nettoyage."""
    try:
        result = host.run(command)
        if result.rc:
            warnings.warn(f"Measurement cleanup failed: {command}: {result.stderr}", stacklevel=2)
    except Exception as exc:  # noqa: BLE001 - un nettoyage ne remplace jamais le vrai échec.
        warnings.warn(f"Measurement cleanup failed: {exc}", stacklevel=2)


def cgroup(host, identifier, filename):
    # Le chemin est déterminé depuis le PID réel du conteneur et son cgroup.
    pid = read(host, f"lxc-info -n {identifier} -pH")
    assert pid.isdigit(), message(
        en="Start the container before measuring its effective limits.",
        fr="Démarrez le conteneur avant de mesurer ses limites effectives.",
    )
    membership = read(host, f"cat /proc/{pid}/cgroup")
    paths = [line[3:] for line in membership.splitlines() if line.startswith("0::/")]
    assert len(paths) == 1, message(
        en="Cannot locate the container's unified cgroup.",
        fr="Impossible de localiser le cgroup unifié du conteneur.",
    )
    path = paths[0].rstrip("/")
    # memory.max et memory.swap.max sont hiérarchiques : un sous-cgroup
    # peut annoncer max tout en héritant de la limite du conteneur parent.
    limits = []
    while path:
        directory = shlex.quote(f"/sys/fs/cgroup{path}")
        target = shlex.quote(f"/sys/fs/cgroup{path}/{filename}")
        read(host, f"test -d {directory}")
        present = run_command(host, f"test -e {target}")
        assert present.rc in (0, 1), message(
            en=f"Cannot locate cgroup controller {filename}.",
            fr=f"Impossible de localiser le contrôleur cgroup {filename}.",
        )
        if present.rc == 1:
            path = path.rpartition("/")[0]
            continue
        value = read(host, "cat " + target)
        if filename == "cpuset.cpus.effective":
            return value
        assert value == "max" or value.isdigit(), message(
            en=f"Cannot read effective limit {filename}.",
            fr=f"Impossible de lire la limite effective {filename}.",
        )
        if value != "max":
            limits.append(int(value))
        path = path.rpartition("/")[0]
    assert filename != "cpuset.cpus.effective", message(
        en="No effective CPU controller was found for the container.",
        fr="Aucun contrôleur CPU effectif n'a été trouvé pour le conteneur.",
    )
    return str(min(limits)) if limits else "max"


def cpu_count(value):
    assert re.fullmatch(r"\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*", value), message(
        en="Cannot read the effective CPU set.",
        fr="Impossible de lire l'ensemble des CPU effectifs.",
    )
    cpus = set()
    for item in value.split(","):
        first, _, last = item.partition("-")
        cpus.update(range(int(first), int(last or first) + 1))
    return len(cpus)


def physical_bridge_ports(host, bridge):
    ports = read_json(host, f"bridge -j link show master {bridge}", list)
    physical = []
    for port in ports:
        name = port.get("ifname", "")
        assert name, message(
            en="Cannot identify a bridge port.", fr="Impossible d'identifier un port du pont.",
        )
        target = read(host, "readlink -f " + shlex.quote(f"/sys/class/net/{name}"))
        assert target.startswith("/sys/devices/"), message(
            en=f"Cannot classify bridge port {name}.", fr=f"Impossible de classifier le port {name} du pont.",
        )
        if not target.startswith("/sys/devices/virtual/net/"):
            physical.append(name)
    return physical


def active_repository(text):
    """Lire les lignes actives .list et les paragraphes deb822 .sources."""
    for line in text.splitlines():
        match = re.match(r"^\s*deb\s+(?:\[[^]]+\]\s+)?https?://\S+\s+\S+\s+(.+)$", line.split("#", 1)[0])
        if match and "pve-no-subscription" in match[1].split():
            return True
    for paragraph in re.split(r"\n\s*\n", text):
        fields = {}
        for line in paragraph.splitlines():
            if line.lstrip().startswith("#"):
                continue
            key, sep, value = line.partition(":")
            if sep:
                fields[key.lower().strip()] = value.strip()
        if (
            fields.get("enabled", "yes").lower() not in {"no", "false", "0", "off"}
            and "deb" in fields.get("types", "").split()
            and fields.get("uris", "").startswith(("https://", "http://"))
            and fields.get("suites")
            and "pve-no-subscription" in fields.get("components", "").split()
        ):
            return True
    return False
