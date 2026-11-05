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

def test_acl_effective_is_scoped_to_the_assigned_pool(pve):
    pools = _json(pve, "pvesh get /pools --output-format json")
    assert {"lab-n2-deleguer", "lab-n2-voisin"} <= {p.get("poolid") for p in pools}, message(en="Both assigned pools must exist in Proxmox.", fr="Les deux pools attribués doivent exister dans Proxmox." )
    assigned = _json(pve, "pvesh get /pools/lab-n2-deleguer --output-format json")
    neighbour = _json(pve, "pvesh get /pools/lab-n2-voisin --output-format json")
    assert "201" in str(assigned) and "216" not in str(assigned), message(en="The assigned pool must contain only sentinel VM 201.", fr="Le pool attribué ne doit contenir que la VM sentinelle 201.")
    assert "216" in str(neighbour) and "201" not in str(neighbour), message(en="The neighbouring pool must contain only sentinel VM 216.", fr="Le pool voisin ne doit contenir que la VM sentinelle 216.")
    acl = _json(pve, "pveum acl list --output-format json")
    entries = [a for a in acl if a.get("ugid") == "equipe-n2@pve"]
    assert any(a.get("path") == "/pool/lab-n2-deleguer" for a in entries), message(en="The delegated principal has no ACL on its assigned pool.", fr="Le principal délégué n’a pas d’ACL sur son pool attribué.")
    assert not any(a.get("path") in ("/", "/pool/lab-n2-voisin", "/vms/216") for a in entries), message(en="The delegated principal is granted access outside its pool.", fr="Le principal délégué reçoit des droits hors de son pool.")
    perms = _json(pve, "pvesh get /access/permissions --path /pool/lab-n2-deleguer --userid equipe-n2@pve --output-format json")
    assert any("VM.Audit" in str(v) or "VM.PowerMgmt" in str(v) for v in perms.values()), message(en="PVE does not report effective VM permissions on the assigned pool.", fr="PVE ne rapporte pas de permissions VM effectives sur le pool attribué.")
