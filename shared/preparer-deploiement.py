"""Prepare owned deployment witnesses; never perform the learner's work."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

LAB = sys.argv[1]
IDS = {
    "pve-gerer-cycle-vie": [195],
    "pve-construire-template": [196, 197, 198, 199],
    "pve-restaurer-premiere-instance": [198, 199],
}
DIRECTORY = Path("/opt/lab-proxmox") / LAB
STORAGE = Path("/etc/pve/storage.cfg")
NETNS = Path("/run/netns")


def run(*args):
    return subprocess.check_output(args, text=True).strip()


def guest(identifier, *args):
    result = json.loads(run("qm", "guest", "exec", str(identifier), "--", *args))
    if result.get("exitcode") != 0:
        raise RuntimeError(result)
    return result.get("out-data", "").strip()


def wait_guest(identifier):
    for _ in range(120):
        try:
            if guest(identifier, "systemctl", "is-active", "temoin.service") == "active":
                return
        except (subprocess.CalledProcessError, ValueError, RuntimeError):
            pass
        time.sleep(5)
    raise RuntimeError("Guest witness did not become ready")


def download_image(path):
    url = "https://cloud.debian.org/images/cloud/trixie/latest/"
    name = "debian-13-genericcloud-amd64.qcow2"
    with urllib.request.urlopen(url + "SHA512SUMS", timeout=90) as response:
        rows = response.read().decode().splitlines()
    matches = [row.split()[0] for row in rows if row.split()[-1].lstrip("*") == name]
    if len(matches) != 1:
        raise RuntimeError("No unique published checksum for the cloud image")
    with urllib.request.urlopen(url + name, timeout=180) as response, path.open("wb") as target:
        shutil.copyfileobj(response, target)
    with path.open("rb") as source:
        digest = hashlib.file_digest(source, "sha512").hexdigest()
    if digest != matches[0]:
        raise RuntimeError("Cloud image checksum mismatch")
    return digest


def cloud_config(nonce, identifier=None):
    if identifier is None:
        program = (
            "from http.server import BaseHTTPRequestHandler, HTTPServer\n"
            "import socket\n"
            "class Handler(BaseHTTPRequestHandler):\n"
            "    def do_GET(self):\n"
            "        identifier = {'clone-a': 198, 'clone-b': 199}[socket.gethostname()]\n"
            f"        body = ('temoin {nonce} vmid %s\\n' % identifier).encode()\n"
            "        self.send_response(200)\n"
            "        self.end_headers()\n"
            "        self.wfile.write(body)\n"
            "HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()\n"
        )
        files = [{"path": "/usr/local/bin/temoin.py", "permissions": "0644", "content": program}]
        start = "/usr/bin/python3 /usr/local/bin/temoin.py"
    else:
        files = [
            {"path": "/srv/temoin/index.html", "permissions": "0644", "content": f"temoin {nonce} vmid {identifier}\n"},
            {"path": "/srv/temoin/retour.txt", "permissions": "0644", "content": nonce + "\n"},
        ]
        start = "/usr/bin/python3 -m http.server 8080 --directory /srv/temoin"
    files.append({"path": "/etc/systemd/system/temoin.service", "permissions": "0644", "content": (
        "[Unit]\nDescription=Deployment witness\nAfter=network-online.target\n"
        f"[Service]\nExecStart={start}\n[Install]\nWantedBy=multi-user.target\n"
    )})
    return "#cloud-config\n" + json.dumps({
        "packages": ["python3", "qemu-guest-agent", "cloud-guest-utils"],
        "write_files": files,
        "runcmd": [["systemctl", "daemon-reload"], ["systemctl", "enable", "--now", "qemu-guest-agent", "temoin.service"]],
    }) + "\n"


def prepare_storage():
    local = json.loads(run("pvesh", "get", "/storage/local", "--output-format", "json"))
    before = {"exists": STORAGE.exists(), "content": local["content"]}
    (DIRECTORY / "storage.before.json").write_text(json.dumps(before))
    run("pvesm", "set", "local", "--content", "iso,vztmpl,backup,images,rootdir,snippets")


def restore_storage():
    before = json.loads((DIRECTORY / "storage.before.json").read_text())
    run("pvesm", "set", "local", "--content", before["content"])
    if not before["exists"]:
        storages = json.loads(run("pvesh", "get", "/storage", "--output-format", "json"))
        if {item["storage"] for item in storages} == {"local"}:
            STORAGE.unlink(missing_ok=True)


def resource_paths(lab):
    return {"image": Path("/var/lib/vz/template/cache") / f"{lab}.qcow2",
            "snippet": Path("/var/lib/vz/snippets") / f"{lab}.yaml",
            "backup": Path("/var/lib/vz/dump") / lab}


def is_mountpoint(path):
    if not path.exists():
        return False
    result = subprocess.run(["mountpoint", "-q", str(path)], check=False)
    if result.returncode not in (0, 32):
        raise RuntimeError(f"Cannot inspect mountpoint {path}")
    return result.returncode == 0


def parent_state():
    parents = [DIRECTORY.parent, resource_paths(LAB)["snippet"].parent]
    if LAB == "pve-restaurer-premiere-instance":
        parents.append(NETNS)
    return {"created": [str(path) for path in parents if not path.exists()],
            "netns_mounted": is_mountpoint(NETNS) if LAB == "pve-restaurer-premiere-instance" else True}


def restore_parents(state):
    if not state["netns_mounted"] and NETNS.exists() and not list(NETNS.iterdir()) and is_mountpoint(NETNS):
        run("umount", str(NETNS))
    for name in state["created"]:
        path = Path(name)
        if path.is_dir():
            if list(path.iterdir()):
                print(f"Preserving shared directory {path}: another resource now uses it")
            else:
                path.rmdir()


def manifest_text(values):
    lab, nonce = values["lab"], values["nonce"]
    lines = [f"# {lab}", "", f"VMID: {values['vmids']}", f"Nonce: {nonce}",
             f"Image: {values['image']}", f"SHA-512: {values['sha512']}",
             f"Cloud-init vendor: local:snippets/{lab}.yaml", "",
             "Gateway / passerelle: 10.10.113.1", "DNS: 10.10.113.1"]
    if lab == "pve-construire-template":
        lines += ["Template: 197, debian13-cloud-v1", "Client user / utilisateur: debian", "RAM: 768 MiB/Mio; vCPU: 1 per clone / par clone"]
        for identifier, name in ((198, "clone-a"), (199, "clone-b")):
            lines += [f"VM {identifier}: {name}, 10.10.113.{identifier}/24, vmbr0",
                      f"Public key / clé publique: {DIRECTORY}/keys/{name}.pub",
                      f"Private key / clé privée: {DIRECTORY}/keys/{name}",
                      f"HTTP: http://10.10.113.{identifier}:8080/", f"Expected line / ligne attendue: temoin {nonce} vmid {identifier}"]
        lines += ["Evaluator VM / VM évaluateur: 196 (keep free / garder libre)",
                  "Keep private keys on this node / gardez les clés privées sur ce nœud."]
    else:
        identifier = 195 if lab == "pve-gerer-cycle-vie" else 198
        lines += [f"HTTP source: http://10.10.113.{identifier}:8080/", f"Expected line / ligne attendue: temoin {nonce} vmid {identifier}",
                  "Initial disk / disque initial: scsi0, 4 GiB/Gio", "Data / données: /srv/temoin/index.html"]
        if identifier == 195:
            lines += ["Initial: vCPU=1, RAM=1024 MiB/Mio; target / cible: vCPU=2, RAM=2048 MiB/Mio, scsi0=8 GiB/Gio",
                      "Snapshot: avant-changement", "Snapshot data / données du snapshot: /srv/temoin/retour.txt", f"Initial value / valeur initiale: {nonce}",
                      "Startup / démarrage: onboot=1, order=20"]
        else:
            lines += ["Restore VM / VM restaurée: 199, vmbr9, guest IPv4 / IPv4 invitée: 10.10.113.198/24",
                      "Client: dsox-restore, 10.10.113.240/24", f"Backup directory / répertoire de sauvegarde: /var/lib/vz/dump/{lab}"]
    return "\n".join(lines) + "\n"


def main():
    occupied = {int(item["vmid"]) for item in json.loads(run("pvesh", "get", "/cluster/resources", "--type", "vm", "--output-format", "json"))}
    if occupied.intersection(IDS[LAB]):
        raise RuntimeError("A reserved guest ID is occupied; clean this lab or resolve the collision first")
    if DIRECTORY.exists():
        raise RuntimeError("Lab directory already exists; run the lab cleanup first")
    paths = resource_paths(LAB)
    for path in paths.values():
        if path.exists():
            raise RuntimeError(f"Reserved resource {path} already exists; no existing file will be replaced")
    if LAB == "pve-restaurer-premiere-instance" and (
        Path("/sys/class/net/vmbr9").exists() or Path("/var/run/netns/dsox-restore").exists()
        or Path("/sys/class/net/dsox-r-host").exists() or Path("/sys/class/net/dsox-r-client").exists()
    ):
        raise RuntimeError("Restore bridge or namespace already exists; no existing network will be replaced")
    parents = parent_state()
    DIRECTORY.mkdir(parents=True, mode=0o700)
    (DIRECTORY / "owner").write_text(LAB + "\n")
    (DIRECTORY / "parents.before.json").write_text(json.dumps(parents))
    nonce = run("openssl", "rand", "-hex", "16")
    (DIRECTORY / "nonce").write_text(nonce + "\n")
    prepare_storage()
    image = paths["image"]
    digest = download_image(image)
    snippet = paths["snippet"]
    snippet.parent.mkdir(exist_ok=True)
    snippet.write_text(cloud_config(nonce, None if LAB == "pve-construire-template" else IDS[LAB][0]))
    values = {"lab": LAB, "nonce": nonce, "image": str(image), "sha512": digest,
              "begin": int(time.time()), "vmids": IDS[LAB]}
    if LAB == "pve-construire-template":
        keys = DIRECTORY / "keys"
        keys.mkdir(mode=0o700)
        for name in ("clone-a", "clone-b"):
            run("ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(keys / name))
    else:
        identifier = IDS[LAB][0]
        run("qm", "create", str(identifier), "--name", "cycle-vie-temoin" if identifier == 195 else "restore-source",
            "--description", f"dsoxlab-lab={LAB}", "--machine", "q35", "--cpu", "host", "--cores", "1",
            "--memory", "1024" if identifier == 195 else "768", "--net0", "virtio,bridge=vmbr0",
            "--scsihw", "virtio-scsi-single", "--scsi0", f"local:0,import-from={image},format=qcow2",
            "--ide2", "local:cloudinit", "--cicustom", f"vendor=local:snippets/{LAB}.yaml",
            "--ipconfig0", f"ip=10.10.113.{identifier}/24,gw=10.10.113.1", "--nameserver", "10.10.113.1",
            "--boot", "order=scsi0", "--agent", "enabled=1")
        run("qm", "disk", "resize", str(identifier), "scsi0", "4G")
        run("qm", "start", str(identifier))
        wait_guest(identifier)
        guest(identifier, "cloud-init", "status", "--wait")
        values["source_config_sha256"] = hashlib.sha256(Path(f"/etc/pve/qemu-server/{identifier}.conf").read_bytes()).hexdigest()
    if LAB == "pve-restaurer-premiere-instance":
        run("ip", "link", "add", "vmbr9", "type", "bridge")
        run("ip", "link", "set", "vmbr9", "up")
        run("ip", "netns", "add", "dsox-restore")
        run("ip", "link", "add", "dsox-r-host", "type", "veth", "peer", "name", "dsox-r-client")
        run("ip", "link", "set", "dsox-r-host", "master", "vmbr9")
        run("ip", "link", "set", "dsox-r-host", "up")
        run("ip", "link", "set", "dsox-r-client", "netns", "dsox-restore")
        run("ip", "-n", "dsox-restore", "address", "add", "10.10.113.240/24", "dev", "dsox-r-client")
        run("ip", "-n", "dsox-restore", "link", "set", "dsox-r-client", "up")
        run("ip", "-n", "dsox-restore", "link", "set", "lo", "up")
        paths["backup"].mkdir(mode=0o700)
    (DIRECTORY / "manifest.json").write_text(json.dumps(values, indent=2) + "\n")
    (DIRECTORY / "manifeste.md").write_text(manifest_text(values))


def clean():
    if not DIRECTORY.is_dir():
        return
    owner = DIRECTORY / "owner"
    manifest = DIRECTORY / "manifest.json"
    owned_directory = owner.is_file() and owner.read_text().strip() == LAB
    if not owned_directory and manifest.is_file():
        owned_directory = json.loads(manifest.read_text()).get("lab") == LAB
    if not owned_directory:
        raise RuntimeError("The directory is not owned by this lab; cleanup refused")
    parents_file = DIRECTORY / "parents.before.json"
    parents = json.loads(parents_file.read_text()) if parents_file.exists() else None
    occupied = {int(item["vmid"]) for item in json.loads(run("pvesh", "get", "/cluster/resources", "--type", "vm", "--output-format", "json"))}
    owned = [identifier for identifier in IDS[LAB] if identifier in occupied]
    for identifier in owned:
        cfg = run("qm", "config", str(identifier))
        if f"description: dsoxlab-lab={LAB}" not in cfg.splitlines():
            raise RuntimeError(f"Guest {identifier} is not owned by this lab; cleanup refused")
    for identifier in sorted(owned, reverse=True):
        if run("qm", "status", str(identifier)) == "status: running":
            subprocess.run(["qm", "shutdown", str(identifier), "--timeout", "60", "--forceStop", "1"], check=True)
        run("qm", "destroy", str(identifier), "--purge", "1", "--destroy-unreferenced-disks", "1")
    if LAB == "pve-restaurer-premiere-instance":
        if Path("/var/run/netns/dsox-restore").exists():
            run("ip", "netns", "delete", "dsox-restore")
        if Path("/sys/class/net/vmbr9").exists():
            run("ip", "link", "delete", "vmbr9")
        backup = Path("/var/lib/vz/dump") / LAB
        if backup.exists():
            shutil.rmtree(backup)
    if (DIRECTORY / "storage.before.json").exists():
        restore_storage()
    (Path("/var/lib/vz/snippets") / f"{LAB}.yaml").unlink(missing_ok=True)
    (Path("/var/lib/vz/template/cache") / f"{LAB}.qcow2").unlink(missing_ok=True)
    shutil.rmtree(DIRECTORY)
    if parents is not None:
        restore_parents(parents)


if __name__ == "__main__":
    clean() if "--clean" in sys.argv else main()
