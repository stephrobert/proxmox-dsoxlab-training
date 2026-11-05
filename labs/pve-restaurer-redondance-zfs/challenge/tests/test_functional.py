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

def test_named_mirror_is_online_and_resilver_is_complete(pve):
    result = pve.run("zpool status -P labmirror-n2-214")
    assert result.rc == 0, message(en="Dedicated disposable ZFS mirror labmirror-n2-214 is missing; no other pool may be substituted.", fr="Le miroir ZFS jetable dédié labmirror-n2-214 est absent ; aucun autre pool ne peut le remplacer.")
    output = result.stdout
    assert "state: ONLINE" in output, message(en="The assigned ZFS pool is not ONLINE.", fr="Le pool ZFS attribué n’est pas ONLINE.")
    assert "mirror-" in output and output.count("ONLINE") >= 3, message(en="The mirror does not show two online members plus an online pool.", fr="Le miroir n’affiche pas deux membres et un pool en état ONLINE.")
    assert "resilvered" in output.lower() and "with 0 errors" in output.lower(), message(en="A completed, error-free resilver is not visible in live ZFS state.", fr="Aucun resilver terminé sans erreur n’est visible dans l’état ZFS réel.")
    assert "errors: No known data errors" in output, message(en="ZFS reports data errors on the assigned pool.", fr="ZFS signale des erreurs de données sur le pool attribué.")
