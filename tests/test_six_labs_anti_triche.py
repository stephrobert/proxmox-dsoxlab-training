"""Chaque propriété des six labs accepte son témoin et refuse sa dégradation."""

from __future__ import annotations

import json
import runpy
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from shared import proxmox_checks

ROOT = Path(__file__).resolve().parents[1]
LABS = (
    "verifier-son-installation", "pve-suivre-tache", "pve-creer-vm",
    "pve-creer-lxc", "pve-raccorder-instance", "pve-reparer-agent",
)


def cases():
    result = []
    for lab in LABS:
        module = runpy.run_path(str(ROOT / "labs" / lab / "challenge/tests/test_functional.py"))
        for name, function in module.items():
            if not name.startswith("test_") or not callable(function):
                continue
            marks = [m for m in getattr(function, "pytestmark", []) if m.name == "parametrize"]
            values = marks[0].args[1] if marks else [()]
            for value in values:
                args = value if isinstance(value, tuple) else (value,)
                result.append((lab, name, args, function))
    return result


CASES = cases()


class Clock:
    def __init__(self):
        self.now = 0

    def monotonic(self):
        self.now += 1
        return self.now

    def sleep(self, _):
        self.now += 100


class Host:
    """État observé, sans connexion à une machine ni commande implicite."""

    def __init__(self, lab, name, args):
        self.lab, self.name, self.args = lab, name, args
        self.bad = False
        self.commands = []
        self.state = "running"
        self.marker = ""
        self.restarted = False
        self.nic_down = False
        self.external_service = False
        self.registre = {"demarrage-191": "UPID:pve:a:qmstart:191:", "demarrage-192": "UPID:pve:b:qmstart:192:", "conf-190": "sha190"}
        self.vm = {"name": "web-temoin", "machine": "q35", "bios": "ovmf", "cpu": "host", "scsihw": "virtio-scsi-single", "scsi0": "local:disk", "efidisk0": "local:efi", "net0": "virtio=AA:BB:CC:DD:EE:FF,bridge=vmbr0", "memory": "2048", "cores": "2", "boot": "order=scsi0", "agent": "enabled=1", "smbios1": "uuid=original"}
        self.ct = {"hostname": "ct-web", "unprivileged": "1", "memory": "512", "swap": "0", "cores": "1", "rootfs": "local:rootfs", "net0": "name=eth0,bridge=vmbr0,ip=10.10.113.170/24,gw=10.10.113.1", "nameserver": "10.10.113.1"}

    def file(self, _):
        return SimpleNamespace(content_string="nonce-session", exists=True)

    def run(self, command):
        self.commands.append(command)
        bad, name = self.bad, self.name
        out, rc = "", 0
        if command == "pveversion":
            out = "pve-manager/8.4.0/x" if bad and name == "test_la_version_est_bien_une_9" else "pve-manager/9.2.2/x"
            if bad and name == "test_proxmox_est_installe":
                rc = 127
        elif command.startswith("systemctl is-active"):
            out = "inactive" if bad else "active"
            rc = 3 if bad else 0
        elif "https://127.0.0.1:8006/" in command:
            out, rc = ("503", 22) if bad else ("200", 0)
        elif command.startswith("ss -H"):
            out = 'users:(("nginx",pid=12,fd=1))' if bad else 'users:(("pveproxy",pid=12,fd=1))'
        elif command == "hostname --ip-address":
            out = "10.10.113.11"
        elif command.startswith("ip -j link show dev"):
            out = json.dumps([{"ifname": command.split()[-1], "flags": [] if self.nic_down else ["UP"]}])
        elif command.startswith("ip link set dev"):
            self.nic_down = command.endswith(" down")
        elif command.startswith("ip -j"):
            out = json.dumps([{"addr_info": [{"local": "192.0.2.9" if bad else "10.10.113.11"}]}])
        elif command.startswith("find /etc/apt"):
            out = "# deb https://download.proxmox.com/debian/pve trixie pve-no-subscription" if bad else "deb https://download.proxmox.com/debian/pve trixie pve-no-subscription"
        elif command.startswith("apt-get update"):
            rc = 100 if bad else 0
        elif command.startswith("qm config") or command.startswith("pct config"):
            values = dict(self.ct if command.startswith("pct") else self.vm)
            if bad:
                if name in {"test_une_propriete_materielle", "test_une_propriete_du_conteneur"}:
                    values[self.args[0]] = "wrong"
                elif name == "test_un_disque_est_sur_local":
                    values[self.args[0]] = "other:disk"
                elif name == "test_le_stockage_est_local":
                    values["rootfs"] = "other:rootfs"
                elif name == "test_la_carte_est_virtio":
                    values["net0"] = "e1000=AA,bridge=vmbr0"
                elif name in {"test_le_pont_est_vmbr0", "test_net0_designe_exactement_vmbr0"}:
                    values["net0"] = "virtio=AA,bridge=vmbr00"
                elif name == "test_une_propriete_reseau":
                    values["net0"] = values["net0"].replace(f"{self.args[0]}={self.args[1]}", f"{self.args[0]}=wrong")
                elif name == "test_le_dns_est_celui_du_manifeste":
                    values["nameserver"] = "192.0.2.9"
                elif name == "test_le_plafond_memoire":
                    values["memory"] = "4096"
                elif name == "test_le_plafond_cpu":
                    values["cores"] = "4"
                elif name == "test_aucune_iso_inseree":
                    values["ide2"] = "local:iso/debian.iso,media=cdrom"
                elif name == "test_scsi0_est_premier":
                    values["boot"] = "order=ide2;scsi0"
                elif name == "test_la_sentinelle_existe":
                    rc = 2
                elif name == "test_le_peripherique_agent_est_active":
                    values["agent"] = "enabled=0"
                elif name == "test_la_vm_n_a_pas_ete_recreee":
                    values["smbios1"] = "uuid=recreated"
            out = "\n".join(f"{k}: {v}" for k, v in values.items())
        elif command.startswith(("qm status", "pct status")):
            out = "status: stopped" if command == "qm status 190" else f"status: {self.state}"
            if bad and name in {"test_la_vm_tourne", "test_le_conteneur_tourne"}:
                out = "status: stopped"
        elif " shutdown " in command:
            if bad and "survit" in name:
                rc = 1
            else:
                self.state = "stopped"
        elif command.startswith(("qm start", "pct start")):
            self.state, self.restarted = "running", True
            if bad and name == "test_les_donnees_survivent_au_redemarrage":
                self.marker = ""
        elif command.startswith("curl "):
            vmid = {"pve-creer-vm": 150, "pve-creer-lxc": 170, "pve-raccorder-instance": 160, "pve-reparer-agent": 180}[self.lab]
            out = f'temoin nonce-session {"ctid" if vmid == 170 else "vmid"} {vmid}'
            if bad and name in {"test_la_page_temoin_repond", "test_la_charge_temoin_est_preservee"}:
                out = "wrong session"
            if self.nic_down and not self.external_service:
                out, rc = "", 7
            if "--write-out" in command:
                out = "000" if rc in (7, 28) else "200"
        elif command.startswith("cat /root/rapport"):
            upid191 = "wrong-upid" if bad and name == "test_l_upid_designe_la_bonne_tache" and self.args == (191,) else self.registre["demarrage-191"]
            upid192 = "wrong-upid" if bad and name == "test_l_upid_designe_la_bonne_tache" and self.args == (192,) else self.registre["demarrage-192"]
            result191 = "error" if bad and name == "test_le_resultat_final_est_exact" and self.args == (191,) else "OK"
            result192 = "disk" if bad and name == "test_le_resultat_final_est_exact" and self.args == (192,) else "missing disk"
            state = "running" if bad and name == "test_l_etat_rapporte_est_courant" else "stopped"
            out = f"demarrage-191: {upid191} {result191}\ndemarrage-192: {upid192} {result192}\netat-190: {state}"
        elif command.startswith("cat /var/lib/lab-proxmox"):
            out = json.dumps(self.registre)
        elif command.startswith("pvesh get"):
            if "/status " in command:
                out = json.dumps({"status": "stopped", "exitstatus": "OK" if ":191:" in command else "missing disk"})
            elif "/cluster/resources" in command:
                out = json.dumps([{"vmid": self.args[0]}] if bad else [])
            else:
                out = "[]"
                if bad and name == "test_aucun_arret_force_n_a_eu_lieu":
                    out = '[{"upid": "forced-stop"}]'
        elif command.startswith("sha256sum"):
            out = "wrong" if bad else "sha190"
        elif command.startswith("lxc-info"):
            out = "123"
        elif command == "cat /proc/123/cgroup":
            out = "0::/lxc/170"
        elif command.startswith("cat /sys/fs/cgroup"):
            filename = command.rsplit("/", 1)[1]
            out = {"memory.max": str(512 * 1024 * 1024), "memory.swap.max": "0", "cpuset.cpus.effective": "0"}[filename]
            if bad and name == "test_une_limite_memoire_effective":
                out = "max"
            elif bad and name == "test_un_seul_cpu_est_effectif":
                out = "0-1"
        elif command.startswith(("test -d /sys/fs/cgroup", "test -e /sys/fs/cgroup")):
            pass
        elif command.startswith("pct exec"):
            if "uid_map" in command:
                out = "0 0 65536" if bad else "0 100000 65536"
            elif "os-release" in command:
                out = 'ID=debian\nVERSION_ID="12"' if bad else 'ID=debian\nVERSION_ID="13"'
            elif "python3 --version" in command:
                out, rc = ("", 127) if bad else ("Python 3.13", 0)
            elif "id -u web" in command:
                out = "0" if bad else "999"
            elif "login.defs" in command:
                out = "UID_MIN 1000"
            elif "ss -H" in command:
                out = 'LISTEN 0 128 *:8080 users:(("python3",pid=42,fd=3))'
            elif "ps -o user=" in command:
                out = "root" if bad else "web"
            elif "printf %s" in command:
                self.marker = command.split("printf %s ", 1)[1].split()[0]
            elif " -- cat /root/marqueur" in command:
                out = self.marker
            elif " -- rm -f /root/marqueur" in command:
                self.marker = ""
            else:
                raise AssertionError(f"Unmodelled CT command: {command}")
        elif command.startswith("bridge -j"):
            if "vmbr0" in command:
                out = json.dumps([{"ifname": "tap1600i0" if bad else "tap160i0"}])
            else:
                out = json.dumps([{"ifname": "eth0"}] if bad else [])
        elif command.startswith("readlink -f /sys/class/net/"):
            out = "/sys/devices/pci0000:00/net/eth0"
        elif command.endswith("/identite.json"):
            out = json.dumps({"smbios1": "uuid=original", "creation_tasks": []})
        elif command.endswith("/debut"):
            out = "1234"
        elif command == "hostname --short":
            out = "pve"
        elif command.startswith("qm agent"):
            if command.endswith(" ping"):
                rc = 1 if bad and name == "test_le_ping_de_l_agent_repond" else 0
            else:
                out = json.dumps([{"name": "ens18", "ip-addresses": [{"ip-address": "192.0.2.9" if bad else "10.10.113.180"}]}])
        elif command.startswith("qm guest exec"):
            out = json.dumps({"exitcode": 1 if bad else 0})
        elif command.startswith("mkdir -p /run/network"):
            rc = 1 if bad else 0
        else:
            raise AssertionError(f"Unmodelled command: {command}")
        return SimpleNamespace(rc=rc, stdout=out, stderr="controlled failure" if rc else "")


@pytest.mark.parametrize("lab,name,args,function", CASES, ids=[f"{lab}:{name}:{args}" for lab, name, args, _ in CASES])
def test_chaque_propriete_accepte_puis_refuse_deux_fois(monkeypatch, lab, name, args, function):
    for bad in (False, True, True):
        host = Host(lab, name, args)
        host.bad = bad
        assert host.bad is bad, "La dégradation doit être établie avant le verdict."
        monkeypatch.setattr(proxmox_checks, "time", Clock())
        if bad:
            with pytest.raises(AssertionError):
                function(host, *args)
        else:
            function(host, *args)
        if name == "test_les_donnees_survivent_au_redemarrage":
            assert not host.marker, "Le marqueur de mesure doit être retiré même après un refus."
        assert not host.nic_down, "L'interface de mesure doit être restaurée même après refus."


def test_la_collecte_ne_perd_aucun_lab():
    assert {lab for lab, *_ in CASES} == set(LABS), "La mesure a perdu un lab."
    assert len(CASES) >= 60, "La mesure a perdu des propriétés."


@pytest.mark.parametrize("lab", LABS)
def test_chaque_consigne_correspond_a_un_seul_cas(lab):
    path = ROOT / "labs" / lab / "requirements.yaml"
    requirements = yaml.safe_load(path.read_text(encoding="utf-8"))["requirements"]
    actual = {(name, json.dumps(args)) for candidate, name, args, _ in CASES if candidate == lab}
    declared = [(r["test"], json.dumps(tuple(r["arguments"]))) for r in requirements]
    assert len(declared) == len(set(declared)), "Deux consignes désignent le même contrôle."
    assert set(declared) == actual, "Consignes et tests ne correspondent pas dans les deux sens."
    for requirement in requirements:
        for language in ("en", "fr"):
            assert requirement[language].strip(), "Chaque consigne doit exister dans les deux langues."
            brief = ROOT / "labs" / lab / "challenge" / ("README.fr.md" if language == "fr" else "README.md")
            assert requirement[language] in brief.read_text(encoding="utf-8"), "Une consigne manque dans l'énoncé."
            scenario = ROOT / "labs" / lab / ("scenario.fr.md" if language == "fr" else "scenario.md")
            assert requirement[language] in scenario.read_text(encoding="utf-8"), "Une consigne manque dans le scénario."


@pytest.mark.parametrize("rc,output", [(1, ""), (0, "not-json"), (0, "{}")])
def test_une_lecture_impossible_ne_devient_pas_une_liste_vide(rc, output):
    host = SimpleNamespace(run=lambda _: SimpleNamespace(rc=rc, stdout=output, stderr="read failed"))
    with pytest.raises(AssertionError):
        proxmox_checks.read_json(host, "read state", list)


@pytest.mark.parametrize("language,expected", [("en", "could not complete"), ("fr", "n'a pas pu aboutir")])
def test_un_code_255_du_backend_devient_un_refus_bilingue(monkeypatch, language, expected):
    monkeypatch.setenv("DSOXLAB_LANG", language)

    def run(_):
        raise RuntimeError("exit_status=255: VM is locked (backup)")

    with pytest.raises(AssertionError, match=expected) as error:
        proxmox_checks.read(SimpleNamespace(run=run), "qm shutdown 150 --timeout 120")
    assert "VM is locked" in str(error.value), "La cause technique doit être conservée."


@pytest.mark.parametrize("text,expected", [
    ("# deb https://example/pve trixie pve-no-subscription", False),
    ("deb pve-no-subscription", False),
    ("deb https://example/pve trixie pve-no-subscription", True),
    ("Types: deb\nURIs: https://example/pve\nSuites: trixie\nComponents: pve-no-subscription\nEnabled: no", False),
    ("Types: deb\nURIs: https://example/pve\nSuites: trixie\nComponents: pve-no-subscription\nEnabled: false", False),
    ("Types: deb\nURIs: https://example/pve\nSuites: trixie\nComponents: pve-no-subscription", True),
])
def test_le_depot_est_actif_et_complet(text, expected):
    assert proxmox_checks.active_repository(text) is expected, "Le dépôt doit être actif et complet."


def test_un_arret_non_observe_ne_devient_pas_un_redemarrage(monkeypatch):
    commands = []

    def run(command):
        commands.append(command)
        return SimpleNamespace(rc=0, stdout="status: running", stderr="")

    monkeypatch.setattr(proxmox_checks, "time", Clock())
    with pytest.raises(AssertionError, match="stopped"):
        proxmox_checks.restart(SimpleNamespace(run=run), "qm", 150)
    assert "qm start 150" not in commands, "Un arrêt doit être constaté avant le démarrage."


def test_le_nettoyage_ne_masque_pas_la_cause():
    host = SimpleNamespace(run=lambda _: SimpleNamespace(rc=1, stderr="cleanup failure"))
    with pytest.warns(UserWarning, match="cleanup"), pytest.raises(AssertionError, match="original failure"):
        try:
            raise AssertionError("original failure")
        finally:
            proxmox_checks.cleanup(host, "cleanup")


def test_un_timeout_de_nettoyage_ne_masque_pas_la_cause():
    def run(_):
        raise subprocess.TimeoutExpired("cleanup", 1)

    with pytest.warns(UserWarning, match="cleanup"), pytest.raises(AssertionError, match="original failure"):
        try:
            raise AssertionError("original failure")
        finally:
            proxmox_checks.cleanup(SimpleNamespace(run=run), "cleanup")


def test_la_limite_effective_est_heritee_du_parent():
    observed = {
        "lxc-info -n 170 -pH": "123",
        "cat /proc/123/cgroup": "0::/lxc/170/ns",
        "cat /sys/fs/cgroup/lxc/170/ns/memory.max": "max",
        "cat /sys/fs/cgroup/lxc/170/memory.max": "536870912",
        "cat /sys/fs/cgroup/lxc/memory.max": "max",
    }
    host = SimpleNamespace(run=lambda command: SimpleNamespace(rc=0, stdout="" if command.startswith("test ") else observed[command], stderr=""))
    assert proxmox_checks.cgroup(host, 170, "memory.max") == "536870912", "La limite parent doit être appliquée."


def test_le_controleur_cpu_est_cherche_au_parent_de_init_scope():
    observed = {
        "lxc-info -n 170 -pH": "123",
        "cat /proc/123/cgroup": "0::/lxc/170/ns/init.scope",
        "cat /sys/fs/cgroup/lxc/170/cpuset.cpus.effective": "2",
    }

    def run(command):
        if command.startswith("test -d "):
            return SimpleNamespace(rc=0, stdout="", stderr="")
        if command.startswith("test -e "):
            return SimpleNamespace(rc=0 if command.endswith("/170/cpuset.cpus.effective") else 1, stdout="", stderr="")
        return SimpleNamespace(rc=0, stdout=observed[command], stderr="")

    assert proxmox_checks.cgroup(SimpleNamespace(run=run), 170, "cpuset.cpus.effective") == "2", "Le contrôleur parent doit être trouvé."


def test_un_service_exterieur_a_l_invite_est_refuse(monkeypatch):
    host = Host("pve-creer-vm", "test_la_page_temoin_repond", ())
    host.external_service = True
    assert host.external_service, "Le service extérieur doit exister avant le verdict."
    monkeypatch.setattr(proxmox_checks, "time", Clock())
    with pytest.raises(AssertionError, match=r"survives|survit"):
        proxmox_checks.require_guest_page(host, "qm", 150, "10.10.113.150", "temoin nonce-session vmid 150")
    assert not host.nic_down, "L'interface doit être restaurée après refus du relais."


def test_une_sonde_http_cassee_ne_prouve_pas_l_isolement(monkeypatch):
    host = Host("pve-creer-vm", "test_la_page_temoin_repond", ())
    original = host.run

    def run(command):
        if host.nic_down and command.startswith("curl "):
            return SimpleNamespace(rc=127, stdout="", stderr="curl missing")
        return original(command)

    host.run = run
    monkeypatch.setattr(proxmox_checks, "time", Clock())
    with pytest.raises(AssertionError):
        proxmox_checks.require_guest_page(host, "qm", 150, "10.10.113.150", "temoin nonce-session vmid 150")
    assert not host.nic_down, "La sonde cassée doit refuser et restaurer l'interface."


def test_un_port_virtuel_n_est_pas_accuse_comme_physique():
    observed = {
        "bridge -j link show master vmbr9": '[{"ifname":"dummy0"}]',
        "readlink -f /sys/class/net/dummy0": "/sys/devices/virtual/net/dummy0",
    }
    host = SimpleNamespace(run=lambda command: SimpleNamespace(rc=0, stdout=observed[command], stderr=""))
    assert not proxmox_checks.physical_bridge_ports(host, "vmbr9"), "Un port virtuel n'est pas un port physique."
