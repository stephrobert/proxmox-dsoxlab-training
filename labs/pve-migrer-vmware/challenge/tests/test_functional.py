from __future__ import annotations

import json
import re

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

def test_imported_vm_has_disks_and_live_guest_network(pve):
    config = _vm_config(pve, 1780)
    disks = [line for line in config.splitlines() if line.startswith(("scsi", "sata", "virtio"))]
    ovf = pve.file("/opt/lab-proxmox/import/source.ovf").content_string
    source_disks = re.findall(r"<(?:[\w.-]+:)?Disk(?:\s|>)", ovf)
    assert source_disks and len(disks) >= len(source_disks), message(
        en=f"Imported disk count does not cover the source OVF inventory ({len(disks)} vs {len(source_disks)}).",
        fr=f"Le nombre de disques importés ne couvre pas l'inventaire OVF source ({len(disks)} contre {len(source_disks)}).",
    )
    assert "running" in _run(pve, "qm status 1780"), message(en="Imported workload is not running.", fr="La charge importée n'est pas en marche.")
    network = json.loads(_run(pve, "qm guest cmd 1780 network-get-interfaces"))
    ips = [a["ip-address"] for i in network if i.get("name") != "lo" for a in i.get("ip-addresses", []) if a.get("ip-address-type") == "ipv4" and not a["ip-address"].startswith("169.254.")]
    assert ips, message(en="Guest agent reports no usable network address.", fr="L'agent invité ne rapporte aucune adresse réseau utilisable.")

def test_cutover_source_is_really_off_and_rollback_exists(pve):
    source_path = pve.file("/etc/lab-proxmox/vmware-source-path").content_string.strip()
    assert source_path, message(en="BLOCKED: VMware source path for live status verification is missing.", fr="BLOQUÉ : chemin source VMware pour la vérification d'état absent.")
    raw = _run(
        pve,
        "bash -lc 'set -a; . /etc/lab-proxmox/govc.env; set +a; "
        'govc vm.info -json "$(cat /etc/lab-proxmox/vmware-source-path)"\'',
    )
    source = json.loads(raw)
    states = [vm.get("runtime", {}).get("powerState") for vm in source.get("virtualMachines", [])]
    assert states == ["poweredOff"], message(en=f"Source is not actually powered off at cutover: {states}", fr=f"La source n'est pas réellement arrêtée à la bascule : {states}")
    snapshots = _run(pve, "qm listsnapshot 1780")
    assert "rollback" in snapshots.lower(), message(en="No named rollback snapshot exists before accepting writes.", fr="Aucun instantané de retour nommé n'existe avant acceptation des écritures.")
