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

def test_api_task_is_observed_for_the_assigned_guest(pve):
    report = json.loads(pve.file("/root/lab-proxmox/pve-epreuve-automatisation/result.json").content_string)
    upid = report.get("upid", "")
    assert upid.startswith("UPID:"), message(
        en="The API client did not record an actual task UPID.",
        fr="Le client API n'a pas enregistré un véritable UPID de tâche.",
    )
    node = upid.split(":")[1]
    status = json.loads(_run(pve, f"pvesh get /nodes/{node}/tasks/{upid}/status --output-format json"))
    assert status.get("status") == "stopped" and status.get("exitstatus") == "OK" and status.get("id") == "vm/1760", message(
        en="The API operation did not complete successfully for VM 1760.",
        fr="L'opération API n'a pas réussi pour la VM 1760.",
    )

def test_terraform_state_and_saved_noop_plan_are_real(pve):
    state = json.loads(_run(pve, "terraform -chdir=/root/lab-proxmox/pve-epreuve-automatisation show -json"))
    resources = state.get("values", {}).get("root_module", {}).get("resources", [])
    assert any(str(resource.get("values", {}).get("vm_id", resource.get("values", {}).get("id", ""))) == "1760" for resource in resources), message(
        en="Terraform state does not own the exact challenge VM.",
        fr="L'état Terraform ne gère pas exactement la VM de l'épreuve.",
    )
    plan = json.loads(_run(pve, "terraform -chdir=/root/lab-proxmox/pve-epreuve-automatisation show -json final.plan"))
    changes = [resource for resource in plan.get("resource_changes", []) if resource.get("change", {}).get("actions") != ["no-op"]]
    assert not changes, message(
        en=f"The final saved Terraform plan is not a no-op: {changes}",
        fr=f"Le plan Terraform final sauvegardé n'est pas vide : {changes}",
    )

def test_refreshed_inventory_contains_only_the_lab_guest(pve):
    inventory = json.loads(_run(pve, "ansible-inventory -i /root/lab-proxmox/pve-epreuve-automatisation/inventory.yml --list --flush-cache"))
    hostvars = inventory.get("_meta", {}).get("hostvars", {})
    tagged = json.loads(_run(pve, "pvesh get /cluster/resources --type vm --output-format json"))
    expected = {
        resource["name"]
        for resource in tagged
        if "pve-epreuve-automatisation" in resource.get("tags", "").split(";")
    }
    assert expected == {"pve-epreuve-automatisation-1760"} and set(hostvars) == expected, message(
        en=f"The refreshed inventory does not match the live tagged guest: {set(hostvars)} / {expected}",
        fr=f"L'inventaire rafraîchi ne correspond pas à l'invité balisé réel : {set(hostvars)} / {expected}",
    )

def test_recipe_repeat_did_not_restart_guest_or_mutate_template(pve):
    node = _run(pve, "hostname -s").strip()
    tasks = json.loads(_run(pve, f"pvesh get /nodes/{node}/tasks --vmid 1760 --typefilter qmstart --limit 50 --output-format json"))
    successful = [task for task in tasks if task.get("status") == "stopped" and task.get("exitstatus") == "OK"]
    assert len(successful) == 1, message(
        en=f"Expected one real guest start across the repeat; found {len(successful)}.",
        fr=f"Un seul démarrage réel de l'invité était attendu malgré la répétition ; {len(successful)} trouvé(s).",
    )
    expected = pve.file("/opt/lab-proxmox/pve-epreuve-automatisation/template.sha256").content_string.split()[0]
    actual = _run(pve, "sha256sum /etc/pve/qemu-server/9000.conf").split()[0]
    assert actual == expected, message(
        en="The approved template configuration changed during the assessment.",
        fr="La configuration du template autorisé a changé pendant l'épreuve.",
    )

def test_service_runs_on_the_actual_guest(pve):
    vmid = 1760
    assert "running" in _run(pve, f"qm status {vmid}"), message(en="The delivered guest is not running.", fr="L'invité livré n'est pas en marche.")
    network = json.loads(_run(pve, f"qm guest cmd {vmid} network-get-interfaces"))
    ips = [a["ip-address"] for i in network if i.get("name") != "lo" for a in i.get("ip-addresses", []) if a.get("ip-address-type") == "ipv4" and not a["ip-address"].startswith("169.254.")]
    assert ips, message(en="The live guest agent reports no usable IPv4 address.", fr="L'agent invité réel ne rapporte aucune adresse IPv4 utilisable.")
    nonce = pve.file("/opt/lab-proxmox/pve-epreuve-automatisation/nonce").content_string.strip()
    response = _run(pve, f"curl --fail --silent --show-error --max-time 5 http://{ips[0]}:8080/")
    assert nonce in response, message(en="The actual guest service does not return this run's nonce.", fr="Le service réel de l'invité ne renvoie pas le nonce de cette exécution.")

def test_real_backup_and_restored_service(pve):
    backups = _run(pve, "pvesm list local --content backup --output-format json")
    data = json.loads(backups)
    assert any(str(item.get("vmid")) == str(1760) for item in data), message(en="No actual Proxmox backup exists for the delivered VM.", fr="Aucune sauvegarde Proxmox réelle n'existe pour la VM livrée.")
    restored = 1761
    assert "running" in _run(pve, f"qm status {restored}"), message(en="The restored lab VM is not running.", fr="La VM restaurée du lab n'est pas en marche.")
    restored_config = _vm_config(pve, restored)
    assert "scsi0:" in restored_config, message(en="The restored VM has no persistent disk.", fr="La VM restaurée n'a pas de disque persistant.")
    network = json.loads(_run(pve, f"qm guest cmd {restored} network-get-interfaces"))
    ips = [
        address["ip-address"]
        for interface in network
        if interface.get("name") != "lo"
        for address in interface.get("ip-addresses", [])
        if address.get("ip-address-type") == "ipv4"
        and not address["ip-address"].startswith("169.254.")
    ]
    assert ips, message(
        en="The restored guest has no live network address.",
        fr="L'invité restauré n'a pas d'adresse réseau réelle.",
    )
    nonce = pve.file("/opt/lab-proxmox/pve-epreuve-automatisation/nonce").content_string.strip()
    response = _run(pve, f"curl --fail --silent --show-error --max-time 5 http://{ips[0]}:8080/")
    assert nonce in response, message(
        en="The restored service does not return the same challenge nonce.",
        fr="Le service restauré ne renvoie pas le même nonce du défi.",
    )

def test_template_and_unrelated_resources_remain_untouched(pve):
    template = _vm_config(pve, 9000)
    assert "template: 1" in template, message(en="The approved template must remain a template.", fr="Le template autorisé doit rester un template.")
