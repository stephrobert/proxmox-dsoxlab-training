"""Functional checks read live Proxmox state; they never accept typed evidence."""
from __future__ import annotations

import json
import re

import pytest

from conftest import lab_host, lab_target_host, message

PVE = lab_target_host("pve.lab")

@pytest.fixture(scope="module")
def pve():
    return lab_host(PVE)

def _json(host, command):
    result = host.run(command)
    assert result.rc == 0, message(en=f"Cannot read Proxmox state with: {command}", fr=f"Impossible de lire l’état Proxmox avec : {command}")
    return json.loads(result.stdout)

def _parse_config(output):
    config = {}
    for line in output.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            config[key.strip()] = value.strip()
    return config

def _vm_config(host, vmid):
    result = host.run(f"qm config {vmid}")
    assert result.rc == 0, message(en=f"Assigned VM {vmid} is missing from live PVE state.", fr=f"La VM {vmid} attribuée est absente de l’état PVE réel.")
    return _parse_config(result.stdout)

def _storage_block(host, storage):
    result = host.run("cat /etc/pve/storage.cfg")
    assert result.rc == 0, message(en="PVE storage configuration is unavailable.", fr="La configuration de stockage PVE est indisponible.")
    match = re.search(rf"(?ms)^{re.escape(storage)}:.*?(?=^[^\s#][^:]*:|\Z)", result.stdout)
    return match.group(0) if match else ""

def test_fault_injected_vm_is_repaired_without_losing_disk_or_controls(pve):
    config = _vm_config(pve, 211)
    assert "net0" in config and "bridge=vmbr0" in config["net0"], message(en="VM 211 is still attached to the injected bad bridge instead of vmbr0.", fr="La VM 211 est toujours raccordée au pont erroné injecté au lieu de vmbr0.")
    assert any(k.startswith(("scsi", "virtio", "sata")) for k in config), message(en="VM 211 lost its persistent disk during repair.", fr="La VM 211 a perdu son disque persistant pendant la réparation.")
    assert "firewall=1" in config.get("net0", "") and "enabled=1" in config.get("agent", ""), message(en="The VM firewall and guest-agent controls must remain enabled.", fr="Le pare-feu de la VM et l’agent invité doivent rester activés.")
    status = pve.run("qm status 211")
    assert status.rc == 0 and "status: running" in status.stdout, message(en="VM 211 is not running after repair.", fr="La VM 211 n’est pas démarrée après réparation.")
    assert pve.run("qm agent 211 ping").rc == 0, message(en="The repaired guest agent is not responding.", fr="L’agent invité réparé ne répond pas.")
