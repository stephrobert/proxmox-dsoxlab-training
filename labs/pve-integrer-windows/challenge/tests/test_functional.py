from __future__ import annotations

import json

import pytest

from conftest import lab_host, message


@pytest.fixture(scope="module")
def pve():
    return lab_host("pve.lab")

def _run(host, command):
    result = host.run(command)
    assert result.rc == 0, message(
        en=f"BLOCKED: required live capability/command is unavailable: {command}\n{result.stderr}",
        fr=f"BLOQUÉ : capacité/commande réelle requise indisponible : {command}\n{result.stderr}",
    )
    return result.stdout

def _vm_config(host, vmid):
    return _run(host, f"qm config {vmid}")

def test_blocked_media_and_license_are_explicit(pve):
    config_file = pve.file("/etc/lab-proxmox/windows-license-authorized")
    assert config_file.exists, message(en="BLOCKED: administrator license authorization is missing.", fr="BLOQUÉ : autorisation de licence administrateur absente.")
    for media in ("windows-authorized.iso", "virtio-win.iso"):
        assert pve.file(f"/var/lib/vz/template/iso/{media}").exists, message(en=f"BLOCKED: required licensed/official ISO is absent: {media}", fr=f"BLOQUÉ : ISO autorisée/officielle requise absente : {media}")

def test_live_windows_vm_has_supported_virtio_firmware_devices(pve):
    config = _vm_config(pve, 1770)
    required = ("ostype: win11", "bios: ovmf", "efidisk0:", "tpmstate0:", "scsi0:", "virtio", "bridge=vmbr0")
    missing = [line for line in required if line not in config]
    assert not missing, message(en=f"Live Windows VM is missing required devices/settings: {missing}", fr=f"La VM Windows réelle ne possède pas les périphériques/paramètres requis : {missing}")
    assert not any(line.startswith(("ide2:", "sata0:")) and "iso/" in line for line in config.splitlines()), message(en="Installation media is still attached.", fr="Le média d'installation est toujours attaché.")

def test_guest_agent_and_restored_efi_tpm_state(pve):
    assert "running" in _run(pve, "qm status 1770"), message(
        en="BLOCKED: boot the installed Windows guest after removing installation media.",
        fr="BLOQUÉ : démarrez l'invité Windows installé après retrait des médias.",
    )
    agent = json.loads(_run(pve, "qm guest cmd 1770 network-get-interfaces"))
    addresses = [
        address["ip-address"]
        for interface in agent
        if interface.get("name") != "lo"
        for address in interface.get("ip-addresses", [])
        if address.get("ip-address-type") == "ipv4"
        and not address["ip-address"].startswith("169.254.")
    ]
    assert addresses, message(en="Guest agent did not return a usable network address after reboot.", fr="L'agent invité n'a pas renvoyé d'adresse réseau utilisable après redémarrage.")
    node = _run(pve, "hostname -s").strip()
    reboots = json.loads(_run(pve, f"pvesh get /nodes/{node}/tasks --vmid 1770 --typefilter qmreboot --limit 50 --output-format json"))
    assert any(task.get("status") == "stopped" and task.get("exitstatus") == "OK" for task in reboots), message(
        en="Proxmox task history does not show a real successful guest reboot.",
        fr="L'historique Proxmox ne montre pas de redémarrage réel réussi de l'invité.",
    )
    backups = json.loads(_run(pve, "pvesm list local --content backup --output-format json"))
    assert any(str(item.get("vmid")) == "1770" for item in backups), message(
        en="No real Proxmox backup exists for the Windows guest.",
        fr="Aucune sauvegarde Proxmox réelle n'existe pour l'invité Windows.",
    )
    restored = _vm_config(pve, 1771)
    assert "running" in _run(pve, "qm status 1771"), message(
        en="The restored Windows guest is not running.",
        fr="L'invité Windows restauré n'est pas en marche.",
    )
    assert all(x in restored for x in ("efidisk0:", "tpmstate0:", "scsi0:")), message(en="Restored VM is missing EFI, TPM or system disk state.", fr="La VM restaurée ne contient pas l'état EFI, TPM ou disque système.")
