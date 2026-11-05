from __future__ import annotations

import json

import pytest

from conftest import lab_host, message


@pytest.fixture(scope="module")
def pve():
    return lab_host("pve.lab")

def _run(host, command):
    result = host.run(command)
    assert result.rc == 0, message(
        en=f"BLOCKED: required live capability/command is unavailable: {command}\n{result.stderr}",
        fr=f"BLOQUÉ : capacité/commande réelle requise indisponible : {command}\n{result.stderr}",
    )
    return result.stdout

def _vm_config(host, vmid):
    return _run(host, f"qm config {vmid}")

def test_only_authorized_target_is_stopped(pve):
    target = _run(pve, "qm status 1741").strip()
    sentinel = _run(pve, "qm status 1742").strip()
    assert "stopped" in target and "running" in sentinel, message(en=f"Target/sentinel state is wrong: {target} / {sentinel}", fr=f"État cible/sentinelle incorrect : {target} / {sentinel}")

def test_proxmox_records_one_real_stop_and_no_repeat(pve):
    config = _vm_config(pve, 1741)
    node = _run(pve, "hostname -s").strip()
    tasks = json.loads(_run(pve, f"pvesh get /nodes/{node}/tasks --vmid 1741 --typefilter qmstop --limit 50 --output-format json"))
    completed = [t for t in tasks if t.get("status") == "stopped" and t.get("exitstatus") == "OK"]
    assert len(completed) == 1 and "name: pve-operer-ansible-1741" in config, message(en=f"Expected one successful stop task for the lab target, found {len(completed)}.", fr=f"Une seule tâche d'arrêt réussie était attendue pour la cible ; {len(completed)} trouvée(s).")

def test_live_acl_keeps_reader_and_operator_scopes_distinct(pve):
    acls = json.loads(_run(pve, "pveum acl list --output-format json"))
    scoped = [acl for acl in acls if acl.get("path") == "/vms/1741"]
    reader = [acl for acl in scoped if "lab-ansible-reader@pve" in acl.get("ugid", "")]
    operator = [acl for acl in scoped if "lab-ansible-operator@pve" in acl.get("ugid", "")]
    assert reader and operator, message(
        en="BLOCKED: separate live reader/operator ACLs scoped to VM 1741 are required.",
        fr="BLOQUÉ : des ACL réelles distinctes lecture/opérateur, limitées à la VM 1741, sont requises.",
    )
    read_roles = {role for acl in reader for role in acl.get("roleid", "").split(",")}
    operator_roles = {role for acl in operator for role in acl.get("roleid", "").split(",")}
    assert "PVEAuditor" in read_roles and "PVEVMUser" in operator_roles, message(
        en="The live ACL does not separate audit-only and VM power-management rights.",
        fr="L'ACL réelle ne sépare pas les droits d'audit seul et de gestion d'alimentation de la VM.",
    )
