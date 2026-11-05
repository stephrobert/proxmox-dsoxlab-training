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

def test_maintenance_target_is_a_live_pve_node_with_backup_storage(pve):
    version = pve.run("pveversion --verbose")
    assert version.rc == 0 and "pve-manager" in version.stdout, message(en="This target is not an installed PVE node; maintenance cannot be attested here.", fr="Cette cible n’est pas un nœud PVE installé ; la maintenance ne peut pas être évaluée ici.")
    status = pve.run("pvesh get /nodes/$(hostname -s)/status --output-format json")
    assert status.rc == 0 and "uptime" in status.stdout, message(en="PVE node status is unavailable after the planned maintenance.", fr="L’état du nœud PVE est indisponible après la maintenance prévue.")
    stores = pve.run("pvesm status --output-format json")
    assert stores.rc == 0 and any(s.get("status") == "active" and s.get("content") for s in json.loads(stores.stdout)), message(en="No active PVE storage is available for post-maintenance acceptance.", fr="Aucun stockage PVE actif n’est disponible pour la recette après maintenance.")
