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

def _state(pve):
    return json.loads(_run(pve, "terraform -chdir=/root/lab-proxmox/pve-provisionner-terraform show -json"))

def test_terraform_state_owns_exact_live_vm(pve):
    state = _state(pve)
    ids = [str(r.get("values", {}).get("vm_id", r.get("values", {}).get("id", ""))) for r in state.get("values", {}).get("root_module", {}).get("resources", [])]
    assert str(1737) in ids, message(en="Terraform state does not own the exact prepared VM.", fr="L'état Terraform ne gère pas exactement la VM préparée.")
    assert "running" in _run(pve, "qm status 1737"), message(
        en="The provisioned VM is not usable because it is not running.",
        fr="La VM provisionnée n'est pas utilisable car elle ne fonctionne pas.",
    )
    config = _vm_config(pve, 1737)
    assert "cores: 2" in config and "memory: 1024" in config and "bridge=vmbr0" in config, message(en="The actual VM config does not match the declared usable configuration.", fr="La configuration réelle de la VM ne correspond pas à la configuration utilisable déclarée.")

def test_saved_final_plan_is_real_and_empty(pve):
    plan = json.loads(_run(pve, "terraform -chdir=/root/lab-proxmox/pve-provisionner-terraform show -json final.plan"))
    changes = [r for r in plan.get("resource_changes", []) if r.get("change", {}).get("actions") != ["no-op"]]
    assert not changes, message(en=f"The saved second plan still proposes changes: {changes}", fr=f"Le second plan sauvegardé propose encore des changements : {changes}")
    assert plan.get("format_version"), message(en="The saved plan is not valid Terraform plan JSON.", fr="Le plan sauvegardé n'est pas un JSON de plan Terraform valide.")
