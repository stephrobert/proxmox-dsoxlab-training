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

def _terraform_json(pve, suffix):
    return json.loads(_run(pve, f"terraform -chdir=/root/lab-proxmox/pve-reconcilier-etat show -json {suffix}"))

def test_import_uses_exact_existing_vm_without_recreation(pve):
    state = _terraform_json(pve, "")
    resources = state.get("values", {}).get("root_module", {}).get("resources", [])
    assert any(str(r.get("values", {}).get("vm_id", r.get("values", {}).get("id", ""))) == str(1738) for r in resources), message(en="Terraform state does not import the exact pre-existing VM.", fr="L'état Terraform n'importe pas la VM préexistante exacte.")

def test_drift_plan_is_observed_but_non_destructive(pve):
    plan = _terraform_json(pve, "drift.plan")
    changes = plan.get("resource_changes", [])
    target = [r for r in changes if str(r.get("change", {}).get("after", {}).get("vm_id", r.get("change", {}).get("after", {}).get("id", ""))) == str(1738)]
    assert target and any(r["change"].get("actions") != ["no-op"] for r in target), message(en="The captured drift plan does not show a real observed change.", fr="Le plan de dérive capturé ne montre aucun changement réel observé.")
    assert all("delete" not in r["change"].get("actions", []) for r in target), message(en="The drift plan would destroy the VM; do not apply it.", fr="Le plan de dérive détruirait la VM ; ne l'appliquez pas.")

def test_safe_plan_and_live_vm_preserve_identity(pve):
    plan = _terraform_json(pve, "safe.plan")
    config = _vm_config(pve, 1738)
    assert "scsi0:" in config and "name: pve-reconcilier-etat-1738" in config, message(en="The exact VM identity or persistent disk is missing.", fr="L'identité exacte de la VM ou son disque persistant manque.")
    changes = [r for r in plan.get("resource_changes", []) if r.get("change", {}).get("actions") != ["no-op"]]
    assert not any("delete" in r.get("change", {}).get("actions", []) for r in changes), message(en="The safe plan still contains a destructive action.", fr="Le plan sûr contient encore une action destructive.")
