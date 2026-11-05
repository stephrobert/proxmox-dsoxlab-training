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

def test_ansible_inventory_matches_live_tagged_vms(pve):
    data = json.loads(_run(pve, "ansible-inventory -i /root/lab-proxmox/pve-fiabiliser-inventaire/inventory.yml --list --flush-cache"))
    all_hosts = set(data.get("_meta", {}).get("hostvars", {}))
    tagged = json.loads(_run(pve, "pvesh get /cluster/resources --type vm --output-format json"))
    expected = {r["name"] for r in tagged if "pve-fiabiliser-inventaire" in r.get("tags", "").split(";")}
    assert expected == {"pve-fiabiliser-inventaire-1739", "pve-fiabiliser-inventaire-1740"}, message(en=f"The live fixture set is not exact: {expected}", fr=f"L'ensemble réel des VM fixtures n'est pas exact : {expected}")
    assert all_hosts == expected, message(en=f"Dynamic inventory differs from Proxmox: {all_hosts} vs {expected}", fr=f"L'inventaire dynamique diffère de Proxmox : {all_hosts} vs {expected}")

def test_inventory_hosts_resolve_live_management_node_and_no_fake_guest_ip(pve):
    data = json.loads(_run(pve, "ansible-inventory -i /root/lab-proxmox/pve-fiabiliser-inventaire/inventory.yml --list --flush-cache"))
    hosts = data.get("_meta", {}).get("hostvars", {})
    bridge = json.loads(_run(pve, "ip -j -4 addr show vmbr0"))
    management_ips = {
        address["local"]
        for interface in bridge
        for address in interface.get("addr_info", [])
    }
    assert management_ips, message(
        en="BLOCKED: the Proxmox management bridge has no IPv4 address.",
        fr="BLOQUÉ : le pont de gestion Proxmox n'a pas d'adresse IPv4.",
    )
    for name in ("pve-fiabiliser-inventaire-1739", "pve-fiabiliser-inventaire-1740"):
        vars_ = hosts.get(name, {})
        assert vars_.get("proxmox_vmid") in (1739, 1740), message(en=f"{name} has no live VMID mapping.", fr=f"{name} n'a pas de correspondance VMID réelle.")
        assert vars_.get("proxmox_node") and vars_.get("ansible_host") in management_ips, message(en=f"{name} lacks its live management node/address.", fr=f"{name} n'a pas son nœud/adresse de gestion réelle.")
        assert not vars_.get("guest_ip") or vars_.get("guest_agent_available") is True, message(en=f"{name} invents a guest IP without confirmed agent data.", fr=f"{name} invente une IP invitée sans données d'agent confirmées.")
