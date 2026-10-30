"""Note le conteneur 170 que l'apprenant a créé et mis en service.

Contrat du TP `pve-creer-lxc` (src/data/parcours/proxmox.yaml du site) : le
conteneur reste NON privilégié, son service répond depuis un client séparé,
ses limites s'appliquent réellement, et données comme service survivent à un
redémarrage. Le nœud joue le client.

Chaque preuve porte sur l'état EFFECTIF. Une ligne `unprivileged: 1` dans la
configuration ne prouve pas l'isolation : on lit la table de correspondance des
UID du conteneur. Une limite déclarée ne prouve pas une limite appliquée : on
lit le cgroup du conteneur.
"""

from __future__ import annotations

import re
import secrets
import time

import pytest

from conftest import lab_host, lab_target_host, message

CIBLE = lab_target_host("pve.lab")
CTID = 170
ADRESSE = "10.10.113.170"
PORT = 8080
NONCE = "/opt/lab-proxmox/pve-creer-lxc/nonce"
MEMOIRE_OCTETS = 512 * 1024 * 1024


@pytest.fixture(scope="module")
def pve():
    return lab_host(CIBLE)


def _config(hote) -> dict[str, str]:
    res = hote.run(f"pct config {CTID}")
    if res.rc != 0:
        return {}
    return {
        cle.strip(): valeur.strip()
        for cle, _, valeur in (ligne.partition(":") for ligne in res.stdout.splitlines())
    }


def _exiger_ct(hote) -> dict[str, str]:
    config = _config(hote)
    assert config, message(
        en=f"Container {CTID} does not exist. Create it with the CTID given in the lab manifest.",
        fr=f"Le conteneur {CTID} n'existe pas. Créez-le avec le CTID donné par le manifeste du lab.",
    )
    return config


def _ligne_attendue(hote) -> str:
    return f"temoin {hote.file(NONCE).content_string.strip()} ctid {CTID}"


def _page(hote) -> str:
    res = hote.run(f"curl -s --max-time 5 http://{ADRESSE}:{PORT}/")
    return res.stdout if res.rc == 0 else ""


def _cgroup(hote, fichier: str) -> str:
    """Lit un fichier du cgroup du conteneur, quel que soit son niveau."""
    for chemin in (f"/sys/fs/cgroup/lxc/{CTID}/{fichier}", f"/sys/fs/cgroup/lxc/{CTID}/ns/{fichier}"):
        res = hote.run(f"cat {chemin}")
        if res.rc == 0 and res.stdout.strip():
            return res.stdout.strip()
    return ""


def test_le_conteneur_reste_non_privilegie(pve) -> None:
    config = _exiger_ct(pve)
    assert config.get("unprivileged") == "1", message(
        en="The container is privileged: its root is the host's root. Recreate it unprivileged.",
        fr="Le conteneur est privilégié : son root est celui de l'hôte. Recréez-le non privilégié.",
    )
    etat = pve.run(f"pct status {CTID}").stdout
    assert "running" in etat, message(
        en=f"Container {CTID} is not running ({etat.strip()}).",
        fr=f"Le conteneur {CTID} ne tourne pas ({etat.strip()}).",
    )
    # La preuve effective : root (UID 0) du conteneur est projeté sur un UID
    # non privilégié de l'hôte.
    table = pve.run(f"pct exec {CTID} -- cat /proc/self/uid_map").stdout.split()
    assert len(table) >= 2 and table[0] == "0" and int(table[1]) >= 100000, message(
        en=f"The container UID map does not shift root to an unprivileged host UID: {' '.join(table)}",
        fr=f"La table d'UID du conteneur ne projette pas root vers un UID non privilégié de l'hôte : {' '.join(table)}",
    )


def test_le_service_repond_depuis_le_client(pve) -> None:
    _exiger_ct(pve)
    attendu = _ligne_attendue(pve)
    page = _page(pve)
    assert attendu in page, message(
        en=(
            f"http://{ADRESSE}:{PORT}/ does not serve the expected line from the node:\n  {attendu}\n"
            "Check the container address, then that the service listens (ss -tlnp)."
        ),
        fr=(
            f"http://{ADRESSE}:{PORT}/ ne sert pas la ligne attendue depuis le nœud :\n  {attendu}\n"
            "Vérifiez l'adresse du conteneur, puis que le service écoute (ss -tlnp)."
        ),
    )
    proprietaires = pve.run(f"pct exec {CTID} -- ps -o user= -C python3").stdout.split()
    assert proprietaires and set(proprietaires) == {"web"}, message(
        en=f"The service must run as user web, not as {', '.join(proprietaires) or 'nobody'}.",
        fr=f"Le service doit tourner sous l'utilisateur web, pas sous {', '.join(proprietaires) or 'personne'}.",
    )


def test_les_limites_s_appliquent_reellement(pve) -> None:
    config = _exiger_ct(pve)
    ecarts = []
    if config.get("memory") != "512":
        ecarts.append(f"memory={config.get('memory', '512 (défaut)')} dans la configuration, attendu 512")
    if config.get("swap", "512") != "0":
        ecarts.append(f"swap={config.get('swap', '512 (défaut)')}, attendu 0")
    if config.get("cores") != "1":
        ecarts.append(f"cores={config.get('cores', 'tous (défaut)')}, attendu 1")
    memoire = _cgroup(pve, "memory.max")
    if memoire != str(MEMOIRE_OCTETS):
        ecarts.append(f"memory.max du cgroup = {memoire or 'illisible'}, attendu {MEMOIRE_OCTETS}")
    cpus = _cgroup(pve, "cpuset.cpus.effective")
    nombre = sum(
        (int(b) - int(a) + 1) if b else 1
        for a, b in re.findall(r"(\d+)(?:-(\d+))?", cpus)
    )
    if nombre != 1:
        ecarts.append(f"cpuset effectif = {cpus or 'illisible'}, attendu un seul cœur")
    assert not ecarts, message(
        en="The limits are not those of the manifest, or are not applied:\n  " + "\n  ".join(ecarts),
        fr="Les limites ne sont pas celles du manifeste, ou ne s'appliquent pas :\n  " + "\n  ".join(ecarts),
    )


def test_donnees_et_service_survivent_au_redemarrage(pve) -> None:
    _exiger_ct(pve)
    attendu = _ligne_attendue(pve)
    assert attendu in _page(pve), message(
        en="The service does not answer before the reboot: fix the previous tests first.",
        fr="Le service ne répond pas avant le redémarrage : corrigez d'abord les tests précédents.",
    )
    marqueur = secrets.token_hex(8)
    pve.run(f"pct exec {CTID} -- sh -c 'echo {marqueur} > /root/marqueur-lab'")
    pve.run(f"pct reboot {CTID} --timeout 60")
    limite = time.monotonic() + 180
    while time.monotonic() < limite and attendu not in _page(pve):
        time.sleep(5)
    relu = pve.run(f"pct exec {CTID} -- cat /root/marqueur-lab").stdout.strip()
    assert relu == marqueur, message(
        en="A file written before the reboot is gone: the container root disk does not persist.",
        fr="Un fichier écrit avant le redémarrage a disparu : le disque racine du conteneur ne persiste pas.",
    )
    assert attendu in _page(pve), message(
        en="After a reboot, the service no longer answers: it is not enabled (systemctl enable).",
        fr="Après un redémarrage, le service ne répond plus : il n'est pas activé (systemctl enable).",
    )
