"""Guest-side and archive measurements for the next deployment labs."""

from __future__ import annotations

import json
import secrets
import shlex
import time
import warnings

from conftest import message
from shared.cloud_init_status import cloud_init_complete
from shared.proxmox_checks import (
    cleanup,
    config,
    read,
    read_json,
    require_equal,
    require_guest_page,
    wait_page,
)


def manifest(host, lab):
    data = read_json(host, f"cat /opt/lab-proxmox/{lab}/manifest.json", dict)
    assert isinstance(data.get("nonce"), str) and data["nonce"].strip(), message(
        en="Run the lab preparation again: its witness nonce is missing.",
        fr="Rejouez la préparation du lab : son nonce témoin est absent.",
    )
    return data


def guest(host, identifier, command):
    value = read_json(host, f"qm guest exec {identifier} -- {command}", dict)
    require_equal(value.get("exitcode"), 0, f"guest {identifier}: {command}")
    return value.get("out-data", "").strip()


def wait_guest(host, identifier, seconds=180):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        try:
            guest(host, identifier, "true")
            return
        except AssertionError:
            time.sleep(3)
    raise AssertionError(message(en=f"Start the guest agent in VM {identifier}.", fr=f"Démarrez l'agent invité dans la VM {identifier}."))


def cleanup_guest(host, identifier, command):
    try:
        guest(host, identifier, command)
    except AssertionError as exc:
        warnings.warn(f"Guest measurement cleanup failed: {exc}", stacklevel=2)


def restore_service(host, identifier, address, expected):
    """Await restoration even when the measured operation has already failed."""
    try:
        if read(host, f"qm status {identifier}") == "status: stopped":
            read(host, f"qm start {identifier}")
        wait_guest(host, identifier)
        wait_page(host, address, expected)
    except Exception as exc:  # noqa: BLE001 - cleanup must preserve the original failure.
        warnings.warn(f"Guest service restoration failed: {exc}", stacklevel=2)


def disk_path(host, identifier):
    volume = config(host, "qm", identifier).get("scsi0", "").split(",")[0]
    assert volume, message(en="Attach the system disk as scsi0.", fr="Raccordez le disque système sur scsi0.")
    return read(host, "pvesm path " + shlex.quote(volume))


def configured_vcpus(cfg):
    cores, sockets = cfg.get("cores", "1"), cfg.get("sockets", "1")
    if not cores.isdigit() or not sockets.isdigit():
        return "invalid"
    return str(int(cores) * int(sockets))


def ssh_command(identifier, key, command):
    return (
        f"ssh -i /opt/lab-proxmox/pve-construire-template/keys/{key} "
        "-o BatchMode=yes -o IdentitiesOnly=yes -o IdentityAgent=none "
        "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5 "
        f"debian@10.10.113.{identifier} {shlex.quote(command)}"
    )


def ssh(host, identifier, key, command):
    return read(host, ssh_command(identifier, key, command))


def ssh_host_key(host, identifier):
    output = read(host, f"ssh-keyscan -T 5 -t ed25519 10.10.113.{identifier} 2>/dev/null")
    rows = [row.split() for row in output.splitlines() if row and not row.startswith("#")]
    keys = {tuple(row[1:]) for row in rows if len(row) == 3 and row[1] == "ssh-ed25519"}
    assert len(keys) == 1, message(
        en=f"Expose one readable SSH Ed25519 host key from VM {identifier}.",
        fr=f"Exposez une clé hôte SSH Ed25519 lisible depuis la VM {identifier}.",
    )
    return next(iter(keys))


def require_cloud_init(host, identifier):
    result = read_json(host, f"qm guest exec {identifier} -- cloud-init status --format json", dict)
    try:
        report = json.loads(result.get("out-data", ""))
    except (ValueError, TypeError) as exc:
        raise AssertionError(message(
            en="Read a complete cloud-init JSON status from the guest.",
            fr="Obtenez un état JSON cloud-init complet depuis l'invité.",
        )) from exc
    assert cloud_init_complete(report, result.get("exitcode")), message(
        en=f"Finish cloud-init without errors in VM {identifier}; only the documented PVE scalar-user deprecation is accepted: {report}",
        fr=f"Terminez cloud-init sans erreur dans la VM {identifier} ; seule la dépréciation documentée du champ user généré par PVE est admise : {report}",
    )


class IsolatedClient:
    def __init__(self, host):
        self.host = host

    def run(self, command):
        if command.startswith("curl "):
            command = "ip netns exec dsox-restore " + command
        return self.host.run(command)


def restored_page(host):
    nonce = manifest(host, "pve-restaurer-premiere-instance")["nonce"]
    require_guest_page(IsolatedClient(host), "qm", 199, "10.10.113.198", f"temoin {nonce} vmid 198")


def archive(host):
    paths = read(host, "find /var/lib/vz/dump/pve-restaurer-premiere-instance -maxdepth 1 -type f -name 'vzdump-qemu-198-*.vma.zst' -print").splitlines()
    assert len(paths) == 1, message(
        en="Keep exactly one complete vzdump archive of source VM 198 in the assigned backup directory.",
        fr="Conservez une seule archive vzdump complète de la VM source 198 dans le répertoire de sauvegarde attribué.",
    )
    return paths[0]


def archive_command(host, action):
    # vma list reads only the header. Drain the stream afterwards so zstd
    # can validate its trailer without an artificial SIGPIPE. Preserve both
    # the VMA status and the decompressor status through pipefail.
    pipeline = archive_pipeline(archive(host), action)
    return read(host, "bash -o pipefail -c " + shlex.quote(pipeline))


def archive_pipeline(path, action):
    return (
        f"zstd -q -d -c -- {shlex.quote(path)} | "
        f'{{ vma {action} -; vma_rc=$?; cat > /dev/null; exit "$vma_rc"; }}'
    )


def snapshot_rollback(host):
    """Test the named snapshot, then restore the learner's complete current state."""
    nonce = manifest(host, "pve-gerer-cycle-vie")["nonce"]
    require_equal(config(host, "qm", 195).get("memory"), "2048", "memory")
    require_equal(read(host, "qm status 195"), "status: running", "VM 195")
    temporary = "evaluation-" + secrets.token_hex(6)
    created = False
    try:
        read(host, "qm shutdown 195 --timeout 120")
        require_equal(read(host, "qm status 195"), "status: stopped", "VM before measurement snapshot")
        read(host, f"qm snapshot 195 {temporary}")
        created = True
        read(host, "qm start 195")
        wait_guest(host, 195)
        probe = secrets.token_hex(16)
        guest(host, 195, f"sh -c 'printf %s {probe} > /srv/temoin/retour.txt'")
        require_equal(guest(host, 195, "cat /srv/temoin/retour.txt"), probe, "observed pre-rollback change")
        read(host, "qm rollback 195 avant-changement --start 1")
        wait_guest(host, 195)
        require_equal(guest(host, 195, "cat /srv/temoin/retour.txt"), nonce, "snapshot data")
    finally:
        if created:
            cleanup(host, f"qm rollback 195 {temporary} --start 1")
            cleanup(host, f"qm delsnapshot 195 {temporary}")
        else:
            cleanup(host, "qm start 195")
    wait_guest(host, 195)


def snapshot_config(host):
    output = read(host, "qm config 195 --snapshot avant-changement")
    return {key.strip(): value.strip() for key, value in (line.split(":", 1) for line in output.splitlines() if ":" in line)}


def cpu_memory(host, filename):
    process = read(host, "cat /var/run/qemu-server/195.pid")
    assert process.isdigit(), message(en="Start VM 195 before inspecting its process.", fr="Démarrez la VM 195 avant d'inspecter son processus.")
    arguments = read(host, f"cat /proc/{process}/cmdline").split("\x00")
    index = arguments.index(filename) + 1 if filename in arguments else len(arguments)
    return arguments[index] if index < len(arguments) else ""
