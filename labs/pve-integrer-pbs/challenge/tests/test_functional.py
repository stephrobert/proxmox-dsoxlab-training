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

def test_pbs_storage_is_active_and_backup_content_exists(pve):
    storage = _storage_block(pve, "lab-pbs-n2-207")
    assert storage and storage.startswith("pbs:"), message(en="Assigned PBS storage lab-pbs-n2-207 is not configured in PVE; provide the PBS prerequisite.", fr="Le stockage PBS attribué lab-pbs-n2-207 n’est pas configuré dans PVE ; fournissez le prérequis PBS.")
    for key in ("server", "datastore", "username", "fingerprint"):
        assert re.search(rf"(?m)^{key}\s+\S+", storage), message(en=f"PBS storage is missing its {key} setting.", fr=f"Il manque le paramètre {key} au stockage PBS.")
    status = pve.run("pvesm status --storage lab-pbs-n2-207 --output-format json")
    assert status.rc == 0 and any(x.get("status") == " active" or x.get("status") == "active" for x in json.loads(status.stdout)), message(en="The configured PBS datastore is not active.", fr="Le datastore PBS configuré n’est pas actif.")
    content = pve.run("pvesm list lab-pbs-n2-207 --content backup --output-format json")
    assert content.rc == 0 and len(json.loads(content.stdout)) >= 2, message(en="PBS has no actual backup inventory for both assigned workloads.", fr="PBS ne contient pas d’inventaire réel de sauvegarde pour les deux charges attribuées.")
