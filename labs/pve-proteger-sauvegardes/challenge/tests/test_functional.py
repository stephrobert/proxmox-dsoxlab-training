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

def test_retention_and_verification_jobs_are_configured(pve):
    jobs = pve.run("cat /etc/pve/jobs.cfg")
    assert jobs.rc == 0, message(en="The PVE job configuration is unavailable.", fr="La configuration des jobs PVE est indisponible.")
    assert "vmid 208" in jobs.stdout and "storage lab-pbs-n2-208" in jobs.stdout, message(en="No scheduled backup job targets VM 208 and the assigned PBS storage.", fr="Aucun job planifié ne sauvegarde la VM 208 vers le stockage PBS attribué.")
    assert re.search(r"(?m)^\s*(?:maxfiles|prune-backups)\s+", jobs.stdout), message(en="The backup job has no bounded retention policy.", fr="Le job de sauvegarde n’a pas de politique de rétention bornée.")
    backups = pve.run("pvesm list lab-pbs-n2-208 --content backup --output-format json")
    assert backups.rc == 0 and len(json.loads(backups.stdout)) >= 1, message(en="No actual backup snapshot is present in the assigned PBS inventory.", fr="Aucun snapshot réel n’est présent dans l’inventaire PBS attribué.")
    tasks = _json(pve, "pvesh get /nodes/$(hostname -s)/tasks --limit 50 --output-format json")
    assert any("vzdump" in str(task).lower() for task in tasks), message(en="PVE has no observed backup task for the assigned workload.", fr="PVE n’a observé aucune tâche de sauvegarde pour la charge attribuée.")
