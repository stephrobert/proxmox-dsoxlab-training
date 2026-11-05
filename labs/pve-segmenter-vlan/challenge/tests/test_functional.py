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

def test_vm_vlan_and_bridge_configuration_are_effective(pve):
    config = _vm_config(pve, 205)
    nic = config.get("net0", "")
    assert "bridge=vmbr205" in nic and "tag=285" in nic, message(en="VM 205 must use the assigned lab bridge and VLAN 285.", fr="La VM 205 doit utiliser le pont de lab attribué et le VLAN 285.")
    network = pve.run("cat /etc/network/interfaces")
    assert network.rc == 0 and "vmbr205" in network.stdout, message(en="The lab bridge is not present in the PVE node network configuration.", fr="Le pont de lab n’apparaît pas dans la configuration réseau du nœud PVE.")
    block = network.stdout.split("iface vmbr205", 1)[-1].split("\n\n", 1)[0] if "iface vmbr205" in network.stdout else ""
    assert "bridge-vlan-aware yes" in block and "285" in block and "286" in block, message(en="The bridge must be VLAN-aware and allow only the two assigned VLANs.", fr="Le pont doit être VLAN-aware et n’autoriser que les deux VLAN attribués.")
