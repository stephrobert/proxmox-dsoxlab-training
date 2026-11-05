from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import lab_host, lab_target_host, lab_target_roles, message

LAB_ROOT = Path(__file__).resolve().parents[2]
PRIMARY = lab_target_host("pve01.lab")
ROLE_HOSTS = lab_target_roles(LAB_ROOT, PRIMARY)


@pytest.fixture(scope="module")
def cluster_hosts():
    assert ROLE_HOSTS == {"node2": "pve02.lab", "node3": "pve03.lab"}, message(
        en="BLOCKED: select the on-demand proxmox-cluster target with pve01/02/03.",
        fr="BLOQUÉ : sélectionnez la cible proxmox-cluster à la demande avec pve01/02/03.",
    )
    hosts = {
        "pve01": lab_host(PRIMARY),
        "pve02": lab_host(ROLE_HOSTS["node2"]),
        "pve03": lab_host(ROLE_HOSTS["node3"]),
    }
    return {
        "by_role": hosts,
        "by_node": {
            host.run("hostname -s").stdout.strip(): host
            for host in hosts.values()
        },
    }


def _run(host, command: str) -> str:
    result = host.run(command)
    assert result.rc == 0, message(
        en=f"BLOCKED: required live SDN capability is unavailable: {command}\n{result.stderr}",
        fr=f"BLOQUÉ : capacité SDN réelle requise indisponible : {command}\n{result.stderr}",
    )
    return result.stdout


def _vm_config(host, vmid: int) -> str:
    return _run(host, f"qm config {vmid}")


def _cluster_resources(primary):
    resources = json.loads(
        _run(primary, "pvesh get /cluster/resources --type vm --output-format json")
    )
    return {
        int(item["vmid"]): item
        for item in resources
        if item.get("vmid") is not None
    }


def test_vnet_is_live_and_applied_on_configured_nodes(cluster_hosts):
    primary = cluster_hosts["by_role"]["pve01"]
    settings = json.loads(
        primary.file("/etc/lab-proxmox/pve-deployer-sdn.json").content_string
    )
    node_names = set(cluster_hosts["by_node"])
    nodes = set(settings["nodes"])
    assert settings.get("lab_id") == "pve-deployer-sdn", message(
        en="BLOCKED: topology file does not identify this lab.",
        fr="BLOQUÉ : le fichier de topologie n'identifie pas ce lab.",
    )
    assert len(node_names) == 3 and node_names == nodes, message(
        en="BLOCKED: configure all three existing proxmox-cluster nodes in the topology input.",
        fr="BLOQUÉ : configurez les trois nœuds existants de proxmox-cluster dans la topologie.",
    )
    for host in cluster_hosts["by_role"].values():
        cluster_status = _run(host, "pvecm status")
        assert "Quorate: Yes" in cluster_status and "Nodes: 3" in cluster_status, message(
            en="BLOCKED: SDN migration tests require all three existing nodes and quorum.",
            fr="BLOQUÉ : les tests de migration SDN exigent les trois nœuds existants et le quorum.",
        )
    vnets = json.loads(_run(primary, "pvesh get /cluster/sdn/vnets --output-format json"))
    vnet = next((item for item in vnets if item.get("vnet") == "n4-lab"), None)
    assert vnet is not None, message(
        en="The dedicated VNet does not exist in live cluster state.",
        fr="Le VNet dédié n'existe pas dans l'état réel du cluster.",
    )
    status = json.loads(_run(primary, "pvesh get /cluster/sdn/status --output-format json"))
    live = json.dumps(status)
    assert "n4-lab" in live and all(node in live for node in nodes), message(
        en="The VNet has not been applied to every configured node.",
        fr="Le VNet n'a pas été appliqué à tous les nœuds configurés.",
    )
    assert str(settings["mtu"]) in json.dumps(vnet), message(
        en="The live VNet MTU does not match the declared contract.",
        fr="Le MTU du VNet réel ne correspond pas au contrat déclaré.",
    )


def test_guest_network_survives_migration_and_peer_reachability(cluster_hosts):
    primary = cluster_hosts["by_role"]["pve01"]
    settings = json.loads(
        primary.file("/etc/lab-proxmox/pve-deployer-sdn.json").content_string
    )
    resources = _cluster_resources(primary)
    guest = resources.get(1790)
    assert guest and guest.get("node") == settings["target_node"], message(
        en="The lab guest has not completed migration to the configured target node.",
        fr="L'invité du lab n'a pas terminé sa migration vers le nœud cible configuré.",
    )
    peer = resources.get(1791)
    assert peer and peer.get("node") == settings["peer_node"] and peer["node"] != guest["node"], message(
        en="The peer VM is not on the other configured node.",
        fr="La VM paire ne se trouve pas sur l'autre nœud configuré.",
    )
    guest_host = cluster_hosts["by_node"][guest["node"]]
    peer_host = cluster_hosts["by_node"][peer["node"]]
    for host, vmid in ((guest_host, 1790), (peer_host, 1791)):
        config = _vm_config(host, vmid)
        assert "bridge=n4-lab" in config, message(
            en=f"VM {vmid} is not attached to the dedicated VNet.",
            fr=f"La VM {vmid} n'est pas raccordée au VNet dédié.",
        )
        assert "tags: pve-deployer-sdn" in config, message(
            en=f"VM {vmid} is missing the lab ownership tag.",
            fr=f"Il manque à la VM {vmid} la balise de propriété du lab.",
        )
        assert "running" in _run(host, f"qm status {vmid}"), message(
            en=f"VM {vmid} is not running on the SDN network.",
            fr=f"La VM {vmid} ne fonctionne pas sur le réseau SDN.",
        )
    peer_network = json.loads(_run(peer_host, "qm guest cmd 1791 network-get-interfaces"))
    addresses = [
        address["ip-address"]
        for interface in peer_network
        if interface.get("name") != "lo"
        for address in interface.get("ip-addresses", [])
        if address.get("ip-address-type") == "ipv4"
        and not address["ip-address"].startswith("169.254.")
    ]
    assert addresses, message(
        en="The peer guest agent reports no usable IPv4 address.",
        fr="L'agent de l'invité pair ne rapporte aucune adresse IPv4 utilisable.",
    )
    result = json.loads(
        _run(guest_host, f"qm guest exec 1790 -- ping -c 2 -W 2 {addresses[0]}")
    )
    assert result.get("exitcode") == 0, message(
        en="Guest-to-guest reachability failed after migration.",
        fr="La communication entre invités échoue après migration.",
    )
