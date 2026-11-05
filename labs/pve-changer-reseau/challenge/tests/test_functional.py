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

def test_network_change_keeps_management_and_has_one_persistent_rule_set(pve):
    network = pve.run("cat /etc/network/interfaces")
    assert network.rc == 0 and "vmbr206" in network.stdout, message(en="The dedicated PVE lab bridge is missing.", fr="Le pont PVE dédié au lab est absent.")
    routes = pve.run("ip -4 route show default")
    assert routes.rc == 0 and routes.stdout.strip(), message(en="The node has no IPv4 default route; do not claim a safe network-change result.", fr="Le nœud n’a pas de route IPv4 par défaut ; ne concluez pas à un changement réseau sûr.")
    rules = pve.run("nft list chain inet filter N2LAB206")
    assert rules.rc == 0, message(en="The dedicated nftables chain N2LAB206 is absent.", fr="La chaîne nftables dédiée N2LAB206 est absente.")
    assert rules.stdout.count("tcp dport 8206") == 1, message(en="The published lab service rule must exist exactly once.", fr="La règle de publication du service de lab doit exister une seule fois.")
