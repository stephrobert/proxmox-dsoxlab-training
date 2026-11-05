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

def test_token_and_acl_are_present_and_limited(pve):
    users = _json(pve, "pveum user list --output-format json")
    assert any(u.get("userid") == "automation-n2@pve" and u.get("enable", 1) != 0 for u in users), message(en="The automation identity is absent or disabled in PVE.", fr="L’identité d’automatisation est absente ou désactivée dans PVE.")
    tokens = _json(pve, "pveum user token list automation-n2@pve --output-format json")
    token = next((t for t in tokens if t.get("tokenid") == "lab-n2"), None)
    assert token is not None, message(en="The named API token does not exist.", fr="Le jeton API nommé n’existe pas.")
    assert str(token.get("privsep", "")).lower() in ("1", "true", "yes"), message(en="The API token must use privilege separation.", fr="Le jeton API doit utiliser la séparation de privilèges.")
    acl = _json(pve, "pveum acl list --output-format json")
    paths = {a.get("path") for a in acl if a.get("ugid") in ("automation-n2@pve", "automation-n2@pve!lab-n2")}
    assert "/vms/202" in paths and "/" not in paths, message(en="The automation ACL must be limited to VM 202, not the whole node.", fr="L’ACL d’automatisation doit se limiter à la VM 202, pas au nœud entier.")
    cert = pve.run("pvenode cert info")
    assert cert.rc == 0 and "fingerprint" in cert.stdout.lower(), message(en="PVE's active TLS certificate information is unavailable.", fr="Les informations du certificat TLS actif de PVE sont indisponibles.")
