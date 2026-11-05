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

def test_service_runs_on_the_actual_guest(pve):
    vmid = 1750
    assert "running" in _run(pve, f"qm status {vmid}"), message(en="The delivered guest is not running.", fr="L'invité livré n'est pas en marche.")
    network = json.loads(_run(pve, f"qm guest cmd {vmid} network-get-interfaces"))
    ips = [a["ip-address"] for i in network if i.get("name") != "lo" for a in i.get("ip-addresses", []) if a.get("ip-address-type") == "ipv4" and not a["ip-address"].startswith("169.254.")]
    assert ips, message(en="The live guest agent reports no usable IPv4 address.", fr="L'agent invité réel ne rapporte aucune adresse IPv4 utilisable.")
    nonce = pve.file("/opt/lab-proxmox/pve-livrer-plateforme/nonce").content_string.strip()
    response = _run(pve, f"curl --fail --silent --show-error --max-time 5 http://{ips[0]}:8080/")
    assert nonce in response, message(en="The actual guest service does not return this run's nonce.", fr="Le service réel de l'invité ne renvoie pas le nonce de cette exécution.")

def test_real_backup_and_restored_service(pve):
    backups = _run(pve, "pvesm list local --content backup --output-format json")
    data = json.loads(backups)
    assert any(str(item.get("vmid")) == str(1750) for item in data), message(en="No actual Proxmox backup exists for the delivered VM.", fr="Aucune sauvegarde Proxmox réelle n'existe pour la VM livrée.")
    restored = 1751
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
    nonce = pve.file("/opt/lab-proxmox/pve-livrer-plateforme/nonce").content_string.strip()
    response = _run(pve, f"curl --fail --silent --show-error --max-time 5 http://{ips[0]}:8080/")
    assert nonce in response, message(
        en="The restored service does not return the same challenge nonce.",
        fr="Le service restauré ne renvoie pas le même nonce du défi.",
    )

def test_template_and_unrelated_resources_remain_untouched(pve):
    template = _vm_config(pve, 9000)
    expected = pve.file("/opt/lab-proxmox/pve-livrer-plateforme/template.sha256").content_string.split()[0]
    actual = _run(pve, "sha256sum /etc/pve/qemu-server/9000.conf").split()[0]
    assert "template: 1" in template and actual == expected, message(
        en="The approved template was changed during delivery.",
        fr="Le template autorisé a été modifié pendant la livraison.",
    )
