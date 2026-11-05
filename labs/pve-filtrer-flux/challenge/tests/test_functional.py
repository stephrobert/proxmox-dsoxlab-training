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

def test_vm_firewall_is_enabled_with_default_deny(pve):
    config = _vm_config(pve, 203)
    assert "firewall=1" in config.get("net0", ""), message(en="PVE firewall is not enabled on VM 203's NIC.", fr="Le pare-feu PVE n’est pas activé sur la carte réseau de la VM 203.")
    rules = pve.file("/etc/pve/firewall/203.fw")
    assert rules.exists, message(en="The per-VM PVE firewall rule file is missing.", fr="Le fichier de règles pare-feu PVE de la VM est absent.")
    content = rules.content_string
    assert "policy_in: DROP" in content and "IN ACCEPT" in content, message(en="The VM firewall must have default-deny input and an explicit allow rule.", fr="Le pare-feu de la VM doit refuser par défaut et comporter une règle d’autorisation explicite.")
    active = pve.run("pve-firewall status")
    assert active.rc == 0 and "running" in active.stdout.lower(), message(en="The PVE firewall service is not running.", fr="Le service de pare-feu PVE n’est pas actif.")
