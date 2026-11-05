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

def test_api_report_resolves_to_observed_completed_task(pve):
    report = json.loads(pve.file("/root/lab-proxmox/pve-piloter-api/result.json").content_string)
    upid = report.get("upid", "")
    assert upid.startswith("UPID:"), message(en="No real task UPID was recorded.", fr="Aucun vrai UPID de tâche n'a été enregistré.")
    node = upid.split(":")[1]
    status = json.loads(_run(pve, f"pvesh get /nodes/{node}/tasks/{upid}/status --output-format json"))
    assert status.get("status") == "stopped" and status.get("exitstatus") == "OK", message(
        en=f"The reported UPID is not a successful completed task: {status}", fr=f"L'UPID rapporté n'est pas une tâche terminée avec succès : {status}")
    assert status.get("id") == "vm/1736", message(
        en="The observed task does not belong to the assigned VM.",
        fr="La tâche observée ne concerne pas la VM attribuée.",
    )

def test_exactly_one_assigned_vm_is_running(pve):
    resources = json.loads(_run(pve, "pvesh get /cluster/resources --type vm --output-format json"))
    matches = [r for r in resources if int(r.get("vmid", -1)) == 1736]
    assert len(matches) == 1 and matches[0].get("status") == "running", message(
        en="The assigned VM must exist exactly once and be running; a report alone is not proof.", fr="La VM attribuée doit exister une seule fois et être en marche ; un rapport seul n'est pas une preuve.")

def test_secret_is_not_present_in_report_or_client_logs(pve):
    secret_file = pve.file("/root/.config/lab-proxmox/api-token")
    assert secret_file.exists, message(en="BLOCKED: root-only API token file is missing.", fr="BLOQUÉ : fichier root-only du jeton API absent.")
    secret = secret_file.content_string.strip()
    for path in ("/root/lab-proxmox/pve-piloter-api/result.json", "/var/log/lab-proxmox/pve-piloter-api.log"):
        if pve.file(path).exists:
            assert secret not in pve.file(path).content_string, message(en=f"API secret leaked in {path}.", fr=f"Secret API divulgué dans {path}.")
