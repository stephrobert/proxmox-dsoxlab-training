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

def test_unprivileged_container_mounts_are_explicit_and_backed_up(pve):
    result = pve.run("pct config 384")
    assert result.rc == 0, message(en="Assigned unprivileged CT 384 is missing; the lab prerequisite was not provisioned.", fr="Le CT non privilégié 384 attribué est absent ; le prérequis du lab n’a pas été préparé.")
    config = _parse_config(result.stdout)
    assert config.get("unprivileged") == "1", message(en="CT 384 must remain unprivileged.", fr="Le CT 384 doit rester non privilégié.")
    mounts = [v for k, v in config.items() if k.startswith("mp")]
    assert any("lab-n2-volumes" in m and "backup=1" in m for m in mounts), message(en="The managed data volume is not explicitly included in backups.", fr="Le volume de données géré n’est pas explicitement inclus dans les sauvegardes.")
    assert any("/srv/lab-n2-share" in m and "backup=1" in m for m in mounts), message(en="The assigned bind mount is missing or excluded from backups.", fr="Le bind mount attribué est absent ou exclu des sauvegardes.")
    for path in ("/srv/app-data/marker-managed", "/srv/shared-data/marker-bind"):
        marker = pve.run(f"pct exec 384 -- test -f {path}")
        assert marker.rc == 0, message(en=f"Restored CT data marker is missing: {path}", fr=f"Le marqueur de données du CT restauré est absent : {path}")
        owner = pve.run(f"pct exec 384 -- stat -c %u {path}")
        assert owner.rc == 0 and owner.stdout.strip() == "1000", message(en=f"The application UID does not own the restored marker: {path}", fr=f"L’UID applicatif n’est pas propriétaire du marqueur restauré : {path}")
    status = pve.run("pct status 384")
    assert status.rc == 0, message(en="The assigned CT cannot be queried through PVE.", fr="Le CT attribué ne peut pas être interrogé par PVE.")
