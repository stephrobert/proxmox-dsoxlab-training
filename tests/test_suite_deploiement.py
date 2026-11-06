"""Exercise each new deployment requirement against a controlled bad state."""

from __future__ import annotations

import io
import json
import runpy
import shlex
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from shared import deploiement_checks, proxmox_checks
from shared.cloud_init_status import PVE_USER_DEPRECATION, cloud_init_complete

ROOT = Path(__file__).resolve().parents[1]
LABS = ("pve-gerer-cycle-vie", "pve-construire-template", "pve-restaurer-premiere-instance")


def cases():
    found = []
    for lab in LABS:
        module = runpy.run_path(str(ROOT / "labs" / lab / "challenge/tests/test_functional.py"))
        for name, function in module.items():
            if not name.startswith("test_") or not callable(function):
                continue
            marks = [mark for mark in getattr(function, "pytestmark", []) if mark.name == "parametrize"]
            for value in marks[0].args[1] if marks else [()]:
                found.append((lab, name, value if isinstance(value, tuple) else (value,), function))
    return found


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
    def __init__(self, lab, name, args):
        self.lab, self.name, self.args = lab, name, args
        self.bad = False
        self.nic_down = False
        self.temporary = False
        self.root_probe = ""
        self.data = "learner-current-data"
        self.saved = self.data
        self.states = {195: "running", 197: "stopped", 198: "running", 199: "running"}
        self.commands = []

    def cfg(self, identifier, snapshot=False):
        data = {"description": f"dsoxlab-lab={self.lab}", "name": "debian13-cloud-v1" if identifier == 197 else "clone-a" if identifier == 198 else "clone-b",
                "memory": "1024" if snapshot else "2048" if identifier == 195 else "768", "cores": "1" if snapshot or identifier != 195 else "2",
                "onboot": "1", "startup": "order=20", "template": "1", "ide2": "local:197/vm-197-cloudinit.qcow2,media=cdrom",
                "scsi0": f"local:{identifier}/disk.qcow2,size={'4G' if snapshot else '8G'}", "ciuser": "debian", "nameserver": "10.10.113.1",
                "net0": f"virtio=AA:BB:CC:DD:EE:{identifier:02X},bridge={'vmbr9' if self.lab == LABS[2] and identifier == 199 else 'vmbr0'}",
                "ipconfig0": f"ip=10.10.113.{identifier}/24,gw=10.10.113.1", "sshkeys": "ssh-ed25519 KEYA" if identifier == 198 else "ssh-ed25519 KEYB",
                "cicustom": "vendor=local:snippets/pve-construire-template.yaml"}
        if self.bad:
            if self.name == "test_une_allocation_declaree":
                data[self.args[0]] = "wrong"
            elif self.name == "test_le_disque_declare_fait_huit_gio":
                data["scsi0"] = "local:disk,size=4G"
            elif self.name == "test_le_snapshot_garde_une_allocation_initiale" and snapshot:
                data[self.args[0]] = "wrong"
            elif self.name == "test_le_snapshot_garde_le_disque_initial" and snapshot:
                data["scsi0"] = "local:disk,size=8G"
            elif self.name == "test_le_marqueur_de_propriete":
                data["description"] = "unrelated"
            elif self.name == "test_le_template_est_converti":
                data["template"] = "0"
            elif self.name == "test_la_recette_est_versionnee":
                data["name"] = "wrong"
            elif self.name == "test_le_disque_cloud_init_est_present":
                data["ide2"] = "local:iso/debian.iso,media=cdrom"
            elif self.name == "test_la_recette_vendor_est_transmise":
                data["cicustom"] = "user=local:snippets/manual.yaml"
            elif self.name == "test_le_clone_porte_son_nom":
                data["name"] = "wrong"
            elif self.name == "test_le_clone_a_son_adresse":
                data["ipconfig0"] = "ip=dhcp"
            elif self.name == "test_la_cle_autorisee_est_propre_au_clone":
                data["sshkeys"] = "ssh-ed25519 OTHER"
            elif self.name == "test_un_parametre_cloud_init_du_clone":
                key = self.args[1]
                if key == "bridge":
                    data["net0"] = data["net0"].replace("vmbr0", "vmbr00")
                elif key == "gw":
                    data["ipconfig0"] = data["ipconfig0"].replace("gw=10.10.113.1", "gw=192.0.2.1")
                else:
                    data[key] = "wrong"
            elif self.name == "test_la_vm_restauree_est_sur_le_reseau_isole":
                data["net0"] = data["net0"].replace("vmbr9", "vmbr0")
            elif self.name == "test_la_vm_restauree_n_a_pas_de_seconde_carte":
                data["net1"] = "virtio=AA,bridge=vmbr0"
            elif self.name == "test_les_adresses_mac_sont_distinctes" or (self.name == "test_une_identite_est_distincte" and self.args == ("mac",)):
                data["net0"] = "virtio=AA:BB:CC:DD:EE:01,bridge=vmbr0"
        return data

    def run(self, command):
        self.commands.append(command)
        out, rc = "", 0
        bad, name = self.bad, self.name
        tokens = shlex.split(command)
        if command.startswith("qm config "):
            data = self.cfg(int(tokens[2]), "--snapshot" in tokens)
            out = "\n".join(f"{key}: {value}" for key, value in data.items())
        elif command.endswith("/manifest.json"):
            out = json.dumps({"nonce": "nonce", "image": "/image.qcow2", "sha512": "hash", "source_config_sha256": "original", "begin": 1})
        elif command == "cat /var/run/qemu-server/195.pid":
            out = "123"
        elif command == "cat /proc/123/cmdline":
            flag = self.args[0]
            out = "qemu\x00-m\x002048\x00-smp\x002,cores=2\x00"
            if bad and name == "test_une_allocation_effective":
                out = out.replace("2048", "1024") if flag == "-m" else out.replace("2,cores=2", "1,cores=1")
        elif command.startswith("qm status "):
            out = "status: " + self.states[int(tokens[2])]
            if bad and name == "test_le_template_est_arrete":
                out = "status: running"
            if bad and name == "test_la_vm_restauree_tourne":
                out = "status: stopped"
        elif command.startswith("qm shutdown "):
            blocked = name == "test_le_service_survit_a_un_redemarrage" or (name == "test_la_restauration_fonctionne_source_arretee" and tokens[2] == "199")
            rc = 1 if bad and blocked else 0
            if rc == 0:
                self.states[int(tokens[2])] = "stopped"
        elif command.startswith("qm start "):
            self.states[int(tokens[2])] = "running"
        elif command.startswith("qm snapshot "):
            self.saved = self.data
            self.temporary = True
        elif command.startswith("qm rollback "):
            self.data = ("wrong" if bad else "nonce") if "avant-changement" in command else self.saved
            self.states[195] = "running"
        elif command.startswith("qm delsnapshot "):
            self.temporary = False
        elif command.startswith("qm clone "):
            self.temporary = True
        elif command.startswith("qm destroy "):
            self.temporary = False
        elif command.startswith(("qm set ", "qm stop ")):
            pass
        elif command.startswith("qm guest exec "):
            identifier = int(tokens[3])
            sub = tokens[5:]
            value, code = "", 0
            if sub == ["true"]:
                pass
            elif sub[:2] == ["cloud-init", "status"]:
                value = json.dumps({"status": "error" if bad else "done", "errors": ["failed module"] if bad else [], "recoverable_errors": {}})
                code = 1 if bad else 0
            elif sub[:2] == ["blockdev", "--getsize64"]:
                value = str((4 if bad else 8) * 1024**3)
            elif sub[0] == "findmnt":
                value = str((3 if bad else 7) * 1024**3)
            elif sub[0] == "dd":
                self.root_probe = next(part[3:] for part in sub if part.startswith("of="))
                code = 1 if bad else 0
            elif sub[0] == "stat":
                value = str(8 * 1024**2)
            elif sub[0] == "rm":
                self.root_probe = ""
            elif sub[0] == "sh":
                self.data = sub[-1].split()[2]
            elif sub == ["cat", "/srv/temoin/retour.txt"]:
                value = self.data
            elif sub == ["cat", "/srv/temoin/index.html"]:
                value = "wrong" if bad else "temoin nonce vmid 198"
            else:
                raise AssertionError("Unknown guest probe: " + command)
            out = json.dumps({"exitcode": code, "out-data": value})
        elif command.startswith("pvesm path "):
            out = "/disks/" + tokens[2].split(":")[1]
        elif command.startswith("sha512sum "):
            out = "hash /image.qcow2"
        elif command.startswith("qemu-img compare "):
            rc = 1 if bad else 0
        elif command.startswith("qemu-img info "):
            out = json.dumps([{"backing-filename": "/source"}] if bad else [{}])
        elif command.startswith("cat /opt/lab-proxmox/pve-construire-template/keys/"):
            out = "ssh-ed25519 KEYA" if "clone-a.pub" in command else "ssh-ed25519 KEYB"
        elif command.startswith("ssh-keyscan "):
            identifier = tokens[-2].rsplit(".", 1)[1]
            out = "node ssh-ed25519 " + ("duplicate" if bad else identifier)
        elif command.startswith("ssh "):
            identifier = int(next(part for part in tokens if part.startswith("debian@")).rsplit(".", 1)[1])
            if "SSH_RC" in command:
                out = "SSH_RC=0" if bad else "Permission denied (publickey).\nSSH_RC=255"
            else:
                sub = tokens[-1]
                if sub == "true":
                    pass
                elif sub == "id -un":
                    out = "wrong" if bad else "debian"
                elif sub == "hostname --short":
                    out = "wrong" if bad else "clone-a" if identifier == 198 else "clone-b"
                elif sub == "cloud-init status":
                    out = "status: error" if bad else "status: done"
                elif sub.startswith("cat /etc/"):
                    out = "same" if bad else str(identifier)
                else:
                    raise AssertionError("Unknown SSH probe: " + command)
        elif command.startswith("find /var/lib/vz/dump/"):
            out = "/var/lib/vz/dump/pve-restaurer-premiere-instance/vzdump-qemu-198-one.vma.zst"
        elif command.startswith("bash -o pipefail "):
            if "vma verify" in command:
                rc = 1 if bad else 0
            elif "vma list" in command:
                out = "drive-ide2" if bad else "DEV: dev_id=1 size: 4294967296 devname: drive-scsi0"
            else:
                raise AssertionError("Unknown archive probe: " + command)
        elif command == "hostname --short":
            out = "pve"
        elif command.startswith("pvesh get "):
            out = "[]" if "/cluster/resources" in command or bad else '[{"status":"OK"}]'
        elif command.startswith("sha256sum "):
            out = ("modified" if bad else "original") + " config"
        elif command == "ip -j -4 addr show dev vmbr0":
            out = '[{"addr_info":[{"family":"inet","local":"10.10.113.11"}]}]'
        elif command.startswith("ip -j link "):
            out = json.dumps([{"flags": [] if self.nic_down else ["UP"]}])
        elif command.startswith("ip link set "):
            self.nic_down = command.endswith(" down")
        elif command.startswith("bridge -j "):
            out = '[{"ifname":"eno1"}]' if bad else '[]'
        elif command.startswith("readlink -f "):
            out = "/sys/devices/pci0000:00/net/eno1"
        elif command.startswith(("curl ", "ip netns exec dsox-restore curl ")):
            if ":8006/" in command:
                isolated = command.startswith("ip netns exec")
                denied = isolated and not bad
                return SimpleNamespace(rc=28 if denied else 0, stdout="000" if denied else "200", stderr="")
            identifier = 195 if self.lab == LABS[0] else 198 if self.lab == LABS[2] else int(command.split("http://10.10.113.")[1].split(":")[0])
            if identifier == 196:
                identifier = 199
            out = f"temoin nonce vmid {identifier}"
            if bad and name in {"test_la_page_repond_depuis_la_vm", "test_le_service_identifie_le_clone", "test_le_service_source_est_preserve", "test_un_nouveau_clone_rejoue_la_recette", "test_le_client_isole_lit_le_service_restaure"}:
                out = "wrong"
            if self.nic_down:
                out, rc = "", 7
            if "--write-out" in command:
                out = "000" if rc else "200"
        else:
            raise AssertionError("Unknown measurement command: " + command)
        return SimpleNamespace(rc=rc, stdout=out, stderr="controlled failure" if rc else "")


@pytest.mark.parametrize("lab,name,args,function", CASES, ids=[f"{lab}:{name}:{args}" for lab, name, args, _ in CASES])
def test_chaque_exigence_accepte_et_refuse_deux_fois(monkeypatch, lab, name, args, function):
    for bad in (False, True, True):
        host = Host(lab, name, args)
        host.bad = bad
        assert host.bad is bad, "L'état dégradé doit exister avant le verdict."
        monkeypatch.setattr(proxmox_checks, "time", Clock())
        monkeypatch.setattr(deploiement_checks, "time", Clock())
        if bad:
            with pytest.raises(AssertionError):
                function(host, *args)
        else:
            function(host, *args)
        assert not host.nic_down, "La sonde doit rétablir l'interface invitée."
        assert not host.temporary, "La sonde doit retirer sa VM ou son snapshot temporaire."
        assert not host.root_probe, "La sonde doit retirer son fichier d'écriture."
        assert host.states[198] == "running", "La source doit être remise en fonctionnement."
        if name == "test_le_snapshot_restitue_les_donnees_initiales":
            assert host.data == "learner-current-data", "Le retour doit rendre les données courantes à l'apprenant."


def test_la_decouverte_ne_perd_pas_de_labs():
    assert {lab for lab, *_ in CASES} == set(LABS), "Un lab a disparu de la collecte."
    assert len(CASES) >= 73, "Des propriétés ont disparu de la collecte."


@pytest.mark.parametrize("lab", LABS)
def test_les_consigne_et_les_cas_sont_apparies(lab):
    requirements = yaml.safe_load((ROOT / "labs" / lab / "requirements.yaml").read_text())["requirements"]
    declared = [(r["test"], json.dumps(r["arguments"])) for r in requirements]
    actual = {(name, json.dumps(args)) for candidate, name, args, _ in CASES if candidate == lab}
    assert len(set(declared)) == len(declared), "Deux consignes désignent le même cas."
    assert set(declared) == actual, "Consignes et cas doivent se correspondre dans les deux sens."
    for requirement in requirements:
        for key, suffix in [("en", ""), ("fr", ".fr")]:
            for path in [ROOT / "labs" / lab / f"scenario{suffix}.md", ROOT / "labs" / lab / "challenge" / f"README{suffix}.md"]:
                assert requirement[key] in path.read_text(), "Une consigne manque dans le texte apprenant."


@pytest.fixture
def preparation(monkeypatch):
    monkeypatch.setattr("sys.argv", ["preparer-deploiement.py", LABS[0]])
    return runpy.run_path(str(ROOT / "shared/preparer-deploiement.py"))


@pytest.mark.parametrize("lab,identifier", [(LABS[0], 195), (LABS[1], 196), (LABS[2], 199)])
def test_une_collision_refuse_avant_toute_ecriture(preparation, monkeypatch, tmp_path, lab, identifier):
    function = preparation["main"]
    scope = function.__globals__
    commands = []

    def run(*args):
        commands.append(args)
        return json.dumps([{"vmid": identifier}])

    directory = tmp_path / "never-created"
    monkeypatch.setitem(scope, "LAB", lab)
    monkeypatch.setitem(scope, "DIRECTORY", directory)
    monkeypatch.setitem(scope, "run", run)
    with pytest.raises(RuntimeError, match="occupied"):
        function()
    assert not directory.exists(), "La préparation ne doit rien écrire après une collision."
    assert len(commands) == 1 and commands[0][0] == "pvesh", "Aucune mutation ne doit suivre la mesure de collision."


def test_le_nettoyage_verifie_tous_les_proprietaires_avant_suppression(preparation, monkeypatch, tmp_path):
    function = preparation["clean"]
    scope = function.__globals__
    commands = []
    (tmp_path / "owner").write_text(LABS[1])

    def run(*args):
        commands.append(args)
        if args[0] == "pvesh":
            return '[{"vmid":198},{"vmid":199}]'
        return "description: dsoxlab-lab=" + LABS[1] if args[-1] == "198" else "description: another-owner"

    monkeypatch.setitem(scope, "LAB", LABS[1])
    monkeypatch.setitem(scope, "DIRECTORY", tmp_path)
    monkeypatch.setitem(scope, "run", run)
    with pytest.raises(RuntimeError, match="not owned"):
        function()
    assert not any("destroy" in args or "shutdown" in args for args in commands), "Une collision interdit toute suppression, même d'une autre VM du lab."


@pytest.mark.parametrize("valid", [True, False])
def test_l_image_telechargee_est_vraiment_comparee_au_sha512(preparation, monkeypatch, tmp_path, valid):
    import hashlib

    content = b"cloud-image-content"
    digest = hashlib.sha512(content).hexdigest()

    def urlopen(url, **_):
        if url.endswith("SHA512SUMS"):
            return io.BytesIO((digest + "  debian-13-genericcloud-amd64.qcow2\n").encode())
        return io.BytesIO(content if valid else b"corrupt-image")

    monkeypatch.setattr(preparation["urllib"].request, "urlopen", urlopen)
    target = tmp_path / "image.qcow2"
    if valid:
        assert preparation["download_image"](target) == digest, "Le téléchargement conforme doit être accepté."
    else:
        with pytest.raises(RuntimeError, match="checksum mismatch"):
            preparation["download_image"](target)


def test_un_refus_ssh_ne_se_confond_pas_avec_une_panne_reseau():
    module = runpy.run_path(str(ROOT / "labs" / LABS[1] / "challenge/tests/test_functional.py"))
    host = Host(LABS[1], "test_le_clone_refuse_l_autre_cle", (198, "clone-a"))
    original = host.run

    def run(command):
        if "SSH_RC" in command:
            return SimpleNamespace(rc=0, stdout="Connection timed out\nSSH_RC=255", stderr="")
        return original(command)

    host.run = run
    with pytest.raises(AssertionError):
        module["test_le_clone_refuse_l_autre_cle"](host, 198, "clone-a")


def test_scsi00_ne_prouve_pas_la_presence_de_scsi0():
    module = runpy.run_path(str(ROOT / "labs" / LABS[2] / "challenge/tests/test_functional.py"))
    host = Host(LABS[2], "test_l_archive_contient_le_disque_systeme", ())
    original = host.run

    def run(command):
        if "vma list" in command:
            return SimpleNamespace(rc=0, stdout="drive-scsi00", stderr="")
        return original(command)

    host.run = run
    with pytest.raises(AssertionError):
        module["test_l_archive_contient_le_disque_systeme"](host)


def test_un_petit_volume_vma_ne_prouve_pas_la_sauvegarde_du_disque_complet():
    module = runpy.run_path(str(ROOT / "labs" / LABS[2] / "challenge/tests/test_functional.py"))
    host = Host(LABS[2], "test_l_archive_contient_le_disque_systeme", ())
    original = host.run

    def run(command):
        if "vma list" in command:
            return SimpleNamespace(rc=0, stdout="DEV: dev_id=1 size: 1048576 devname: drive-scsi0", stderr="")
        return original(command)

    host.run = run
    with pytest.raises(AssertionError):
        module["test_l_archive_contient_le_disque_systeme"](host)


def test_le_client_isole_ne_deplace_pas_les_commandes_de_controle():
    commands = []
    client = deploiement_checks.IsolatedClient(SimpleNamespace(run=commands.append))
    client.run("curl http://10.10.113.198:8080/")
    client.run("ip link set dev tap199i0 down")
    assert commands == ["ip netns exec dsox-restore curl http://10.10.113.198:8080/", "ip link set dev tap199i0 down"], "Seule la requête HTTP doit être envoyée depuis le client isolé."


@pytest.mark.parametrize("initial_file,other_storage", [(False, False), (True, False), (False, True)])
def test_le_stockage_local_implicite_est_restaure_sans_effacer_un_autre_stockage(preparation, monkeypatch, tmp_path, initial_file, other_storage):
    prepare = preparation["prepare_storage"]
    scope = prepare.__globals__
    storage = tmp_path / "storage.cfg"
    if initial_file:
        storage.write_text("original")
    commands = []

    def run(*args):
        commands.append(args)
        if args[:3] == ("pvesh", "get", "/storage/local"):
            return '{"content":"iso,vztmpl,backup"}'
        if args[:3] == ("pvesh", "get", "/storage"):
            return '[{"storage":"local"},{"storage":"other"}]' if other_storage else '[{"storage":"local"}]'
        storage.write_text("configured")
        return ""

    monkeypatch.setitem(scope, "STORAGE", storage)
    monkeypatch.setitem(scope, "DIRECTORY", tmp_path)
    monkeypatch.setitem(scope, "run", run)
    prepare()
    assert storage.exists(), "Le stockage du lab doit être configuré pour la mesure."
    preparation["restore_storage"]()
    assert storage.exists() == (initial_file or other_storage), "Un stockage initialement implicite doit le redevenir, sans supprimer un autre stockage."
    assert commands[-1 if initial_file else -2][-1] == "iso,vztmpl,backup", "Les contenus initiaux du stockage doivent être rétablis."


def test_le_nettoyage_invite_verifie_le_code_interne_sans_masquer_la_cause():
    host = SimpleNamespace(run=lambda _: SimpleNamespace(rc=0, stdout='{"exitcode":1,"err-data":"read-only filesystem"}', stderr=""))
    with pytest.warns(UserWarning, match="cleanup"), pytest.raises(AssertionError, match="original failure"):
        try:
            raise AssertionError("original failure")
        finally:
            deploiement_checks.cleanup_guest(host, 195, "rm -f /root/probe")


def test_une_cle_hote_illisible_ne_devient_pas_une_identite_distincte():
    host = SimpleNamespace(run=lambda _: SimpleNamespace(rc=0, stdout="unreadable-keyscan", stderr=""))
    with pytest.raises(AssertionError):
        deploiement_checks.ssh_host_key(host, 198)


def test_une_seconde_cle_cloud_init_n_est_pas_ignoree():
    module = runpy.run_path(str(ROOT / "labs" / LABS[1] / "challenge/tests/test_functional.py"))
    host = Host(LABS[1], "test_la_cle_autorisee_est_propre_au_clone", (198, "clone-a"))
    original = host.run

    def run(command):
        result = original(command)
        if command == "qm config 198":
            result.stdout = result.stdout.replace("sshkeys: ssh-ed25519 KEYA", "sshkeys: ssh-ed25519 KEYA%0Assh-ed25519 KEYB")
        return result

    host.run = run
    with pytest.raises(AssertionError):
        module["test_la_cle_autorisee_est_propre_au_clone"](host, 198, "clone-a")


@pytest.mark.parametrize("zstd_rc,vma_rc,expected", [(0, 0, 0), (23, 0, 23), (0, 7, 7)])
def test_le_flux_vma_est_draine_sans_perdre_les_erreurs(tmp_path, zstd_rc, vma_rc, expected):
    zstd = tmp_path / "zstd"
    zstd.write_text(f"#!{sys.executable}\nimport sys\nsys.stdout.buffer.write(b'x' * 1048576)\nsys.stdout.buffer.flush()\nsys.exit({zstd_rc})\n")
    vma = tmp_path / "vma"
    vma.write_text(f"#!{sys.executable}\nimport sys\nsys.stdin.buffer.read(4)\nsys.exit({vma_rc})\n")
    zstd.chmod(0o755)
    vma.chmod(0o755)
    import os

    env = {**os.environ, "PATH": str(tmp_path) + ":" + os.environ["PATH"]}
    result = subprocess.run(["bash", "-o", "pipefail", "-c", deploiement_checks.archive_pipeline("archive.vma.zst", "list")], env=env, capture_output=True, check=False)
    assert result.returncode == expected, "Le lecteur d'en-tête ne doit ni casser le flux ni masquer une erreur du VMA ou de la décompression."


def test_une_collision_de_fichier_ne_modifie_pas_le_stockage(preparation, monkeypatch, tmp_path):
    function = preparation["main"]
    scope = function.__globals__
    collision = tmp_path / "existing.qcow2"
    collision.write_bytes(b"keep-existing-file")
    commands = []

    def run(*args):
        commands.append(args)
        return '[]'

    monkeypatch.setitem(scope, "DIRECTORY", tmp_path / "lab")
    monkeypatch.setitem(scope, "resource_paths", lambda _: {"image": collision})
    monkeypatch.setitem(scope, "run", run)
    with pytest.raises(RuntimeError, match="already exists"):
        function()
    assert len(commands) == 1 and commands[0][0] == "pvesh", "La collision doit précéder toute mutation."
    assert collision.read_bytes() == b"keep-existing-file", "Le fichier préexistant doit rester intact."
    assert not (tmp_path / "lab").exists(), "Aucun répertoire de travail ne doit être créé après la collision."


def test_un_repertoire_non_attribue_n_est_pas_nettoye(preparation, monkeypatch, tmp_path):
    function = preparation["clean"]
    scope = function.__globals__
    sentinel = tmp_path / "sentinel"
    sentinel.write_text("keep")
    commands = []
    monkeypatch.setitem(scope, "DIRECTORY", tmp_path)
    monkeypatch.setitem(scope, "run", lambda *args: commands.append(args))
    with pytest.raises(RuntimeError, match="not owned"):
        function()
    assert not commands and sentinel.read_text() == "keep", "Un répertoire non attribué ne doit subir aucune suppression."


def test_un_manifeste_sans_nonce_ne_produit_pas_un_temoin_valide():
    host = SimpleNamespace(run=lambda _: SimpleNamespace(rc=0, stdout='{"nonce":""}', stderr=""))
    with pytest.raises(AssertionError):
        deploiement_checks.manifest(host, LABS[0])


@pytest.mark.parametrize("code,status,errors,recoverable,expected", [
    (0, "done", [], {}, True),
    (2, "done", [], {"DEPRECATED": [PVE_USER_DEPRECATION]}, True),
    (2, "done", [], {"DEPRECATED": ["another deprecated field"]}, False),
    (2, "done", [], {"WARNING": ["package installation failed"]}, False),
    (2, "done", [], {}, False),
    (1, "done", [], {}, False),
    (False, "done", [], {}, False),
    (0, "running", [], {}, False),
    (2, "done", ["failed module"], {"DEPRECATED": [PVE_USER_DEPRECATION]}, False),
])
def test_seule_la_depreciation_pve_mesuree_est_admise(code, status, errors, recoverable, expected):
    report = {"status": status, "errors": errors, "recoverable_errors": recoverable}
    assert cloud_init_complete(report, code) is expected, "Une erreur réelle ne doit jamais être assimilée à la seule dépréciation PVE documentée."


def test_une_erreur_de_phase_cloud_init_ne_disparait_pas_derriere_done():
    report = {"status": "done", "errors": [], "modules-final": {"errors": ["failure"], "recoverable_errors": {}}}
    assert not cloud_init_complete(report, 0), "Les erreurs d'une phase doivent aussi refuser."


@pytest.mark.parametrize("phase", [{}, "unreadable"])
def test_une_phase_cloud_init_illisible_ne_devient_pas_un_succes(phase):
    report = {"status": "done", "errors": [], "modules-final": phase}
    assert not cloud_init_complete(report, 0), "Une phase présente mais illisible doit refuser."


def test_un_delai_de_demarrage_ne_change_pas_l_ordre_demande():
    module = runpy.run_path(str(ROOT / "labs" / LABS[0] / "challenge/tests/test_functional.py"))
    host = Host(LABS[0], "test_une_allocation_declaree", ("startup", "order=20"))
    original = host.run

    def run(command):
        result = original(command)
        if command == "qm config 195":
            result.stdout = result.stdout.replace("startup: order=20", "startup: order=20,up=15")
        return result

    host.run = run
    module["test_une_allocation_declaree"](host, "startup", "order=20")


@pytest.mark.parametrize("lab,identifier,cores", [(LABS[0], 195, "2"), (LABS[1], 198, "1")])
def test_les_sockets_sont_comptes_dans_le_total_vcpu(lab, identifier, cores):
    module = runpy.run_path(str(ROOT / "labs" / lab / "challenge/tests/test_functional.py"))
    host = Host(lab, "cpu-topology", ())
    original = host.run

    def run(command):
        result = original(command)
        if command == f"qm config {identifier}":
            result.stdout += "\nsockets: 4"
        return result

    host.run = run
    with pytest.raises(AssertionError):
        if lab == LABS[0]:
            module["test_une_allocation_declaree"](host, "cores", cores)
        else:
            module["test_un_parametre_cloud_init_du_clone"](host, identifier, "cores", cores)


def test_le_vcpu_par_defaut_de_pve_reste_valide():
    assert deploiement_checks.configured_vcpus({"name": "clone-a"}) == "1", "Le défaut PVE d'un cœur et d'un socket vaut bien un vCPU."


def test_un_service_de_gestion_arrete_ne_prouve_pas_l_isolement():
    module = runpy.run_path(str(ROOT / "labs" / LABS[2] / "challenge/tests/test_functional.py"))
    host = Host(LABS[2], "test_le_client_ne_joint_pas_la_gestion", ())
    original = host.run

    def run(command):
        if command.startswith("curl ") and ":8006/" in command:
            host.commands.append(command)
            return SimpleNamespace(rc=7, stdout="000", stderr="connection refused")
        return original(command)

    host.run = run
    with pytest.raises(AssertionError):
        module["test_le_client_ne_joint_pas_la_gestion"](host)
    assert not any(command.startswith("ip netns exec") for command in host.commands), "Le service témoin doit être vivant avant de mesurer le refus réseau."


@pytest.mark.parametrize("initial_mount,other_resource", [(False, False), (True, False), (False, True)])
def test_le_montage_netns_et_les_parents_crees_sont_restitues(preparation, monkeypatch, tmp_path, initial_mount, other_resource):
    function = preparation["restore_parents"]
    scope = function.__globals__
    netns = tmp_path / "netns"
    netns.mkdir()
    if other_resource:
        (netns / "another-namespace").write_text("keep")
    commands = []
    monkeypatch.setitem(scope, "NETNS", netns)
    monkeypatch.setitem(scope, "is_mountpoint", lambda _: True)
    monkeypatch.setitem(scope, "run", lambda *args: commands.append(args))
    function({"created": [] if initial_mount else [str(netns)], "netns_mounted": initial_mount})
    assert bool(commands) == (not initial_mount and not other_resource), "Seul un montage créé par le lab et devenu vide doit être retiré."
    assert netns.exists() == (initial_mount or other_resource), "Un parent initialement présent ou utilisé par une autre ressource doit être conservé."


def test_les_parents_absents_sont_releves_avant_preparation(preparation, monkeypatch, tmp_path):
    function = preparation["parent_state"]
    scope = function.__globals__
    parents = [tmp_path / "labs", tmp_path / "snippets", tmp_path / "netns"]
    monkeypatch.setitem(scope, "LAB", LABS[2])
    monkeypatch.setitem(scope, "DIRECTORY", parents[0] / "exercise")
    monkeypatch.setitem(scope, "NETNS", parents[2])
    monkeypatch.setitem(scope, "resource_paths", lambda _: {"snippet": parents[1] / "witness.yaml"})
    monkeypatch.setitem(scope, "is_mountpoint", lambda _: False)
    state = function()
    assert set(state["created"]) == {str(path) for path in parents}, "Chaque parent absent doit être enregistré avant sa création."
    assert not state["netns_mounted"], "Le montage initial absent doit être enregistré."


def test_un_redemarrage_refuse_attend_la_source_avant_le_verdict_suivant(monkeypatch):
    module = runpy.run_path(str(ROOT / "labs" / LABS[2] / "challenge/tests/test_functional.py"))
    host = Host(LABS[2], "late-target-lock", ())
    original = host.run
    warming = False
    starts, ready_probes = [], []

    def run(command):
        nonlocal warming
        if command == "qm shutdown 199 --timeout 120":
            return SimpleNamespace(rc=1, stdout="", stderr="VM 199 locked")
        if command == "qm start 198":
            warming = True
            starts.append(command)
        if command == "qm guest exec 198 -- true":
            ready_probes.append(command)
            if warming:
                warming = False
                return SimpleNamespace(rc=0, stdout='{"exitcode":1}', stderr="")
        return original(command)

    host.run = run
    monkeypatch.setattr(deploiement_checks, "time", Clock())
    monkeypatch.setattr(proxmox_checks, "time", Clock())
    for _ in range(2):
        with pytest.raises(AssertionError, match="qm shutdown 199"):
            module["test_la_restauration_fonctionne_source_arretee"](host)
        assert host.states[198] == "running", "La source doit être relancée après le refus."
    assert len(starts) == 2 and len(ready_probes) >= 4, "Le contrôle doit attendre l'agent de la source à chaque restauration avant de rendre le verdict."


@pytest.mark.parametrize("lab,identifiers", [(LABS[0], [195]), (LABS[1], [198, 199]), (LABS[2], [198])])
def test_le_manifeste_donne_les_lignes_temoin_et_les_chemins_des_cles(preparation, monkeypatch, lab, identifiers):
    function = preparation["manifest_text"]
    monkeypatch.setitem(function.__globals__, "DIRECTORY", Path("/opt/lab-proxmox") / lab)
    text = function({"lab": lab, "nonce": "session-nonce", "vmids": identifiers, "image": "/image.qcow2", "sha512": "checksum"})
    for identifier in identifiers:
        assert f"temoin session-nonce vmid {identifier}" in text, "Le manifeste doit fournir la ligne exacte demandée par les contrôles."
    if lab == LABS[1]:
        assert f"/opt/lab-proxmox/{lab}/keys/clone-a.pub" in text, "La clé fournie doit être localisable sans deviner son chemin."
        assert f"/opt/lab-proxmox/{lab}/keys/clone-b.pub" in text, "Chaque clone doit avoir le chemin de sa clé."


def test_un_pont_preexistant_est_refuse_avant_toute_mutation(preparation, monkeypatch, tmp_path):
    function = preparation["main"]
    scope = function.__globals__
    original_exists = Path.exists
    commands = []

    def exists(path):
        return str(path) == "/sys/class/net/vmbr9" or original_exists(path)

    def run(*args):
        commands.append(args)
        return '[]'

    monkeypatch.setattr(Path, "exists", exists)
    monkeypatch.setitem(scope, "LAB", LABS[2])
    monkeypatch.setitem(scope, "DIRECTORY", tmp_path / "lab")
    monkeypatch.setitem(scope, "resource_paths", lambda _: {"image": tmp_path / "image.qcow2"})
    monkeypatch.setitem(scope, "run", run)
    with pytest.raises(RuntimeError, match="existing network"):
        function()
    assert len(commands) == 1 and commands[0][0] == "pvesh", "Un pont préexistant interdit toute modification de ressource ou du stockage."
    assert not (tmp_path / "lab").exists(), "Le répertoire du lab ne doit pas être créé après une collision réseau."
