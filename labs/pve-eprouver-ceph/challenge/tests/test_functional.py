from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

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
    return {
        "pve01": lab_host(PRIMARY),
        "pve02": lab_host(ROLE_HOSTS["node2"]),
        "pve03": lab_host(ROLE_HOSTS["node3"]),
    }


def _run(host, command: str) -> str:
    result = host.run(command)
    assert result.rc == 0, message(
        en=f"BLOCKED: required live capability/command is unavailable: {command}\n{result.stderr}",
        fr=f"BLOQUÉ : capacité/commande réelle requise indisponible : {command}\n{result.stderr}",
    )
    return result.stdout


def test_cluster_is_three_node_and_quorate(cluster_hosts):
    for node, host in cluster_hosts.items():
        assert _run(host, "hostname -s").strip() == node, message(
            en=f"BLOCKED: {node} does not resolve to the requested proxmox-cluster node.",
            fr=f"BLOQUÉ : {node} ne correspond pas au nœud demandé de proxmox-cluster.",
        )
        status = _run(host, "pvecm status")
        assert "Quorate: Yes" in status and "Nodes: 3" in status, message(
            en="BLOCKED: Ceph fault testing requires the existing three-node cluster to be quorate.",
            fr="BLOQUÉ : l'épreuve de panne Ceph exige un cluster existant à trois nœuds et avec quorum.",
        )


def test_isolation_and_osd_identity_are_explicit(cluster_hosts):
    pve = cluster_hosts["pve01"]
    assert pve.file("/etc/lab-proxmox/ceph-isolated").exists, message(
        en="BLOCKED: Ceph cluster is not marked isolated.",
        fr="BLOQUÉ : le cluster Ceph n'est pas marqué isolé.",
    )
    assert pve.file("/etc/lab-proxmox/pve-eprouver-ceph.yml").exists, message(
        en="BLOCKED: dedicated disposable OSD id is not configured.",
        fr="BLOQUÉ : l'identifiant d'OSD jetable dédié n'est pas configuré.",
    )
    ownership = _run(
        pve, "ceph osd pool application get n4-lab rbd dsoxlab_lab"
    )
    assert ownership.strip() == "pve-eprouver-ceph", message(
        en="The lab pool lacks its ownership marker; cleanup will not remove it.",
        fr="Le pool du lab n'a pas son marqueur de propriété ; le nettoyage ne le supprimera pas.",
    )


def test_actual_degraded_and_recovered_ceph_state(cluster_hosts):
    pve = cluster_hosts["pve01"]
    health = json.loads(_run(pve, "ceph status --format json"))
    osd = json.loads(_run(pve, "ceph osd dump --format json"))
    pg = json.loads(_run(pve, "ceph pg stat --format json"))
    image = _run(pve, "rbd info n4-lab/probe")
    assert "n4-lab/probe" in image, message(
        en="The dedicated RBD witness image is missing.",
        fr="L'image témoin RBD dédiée manque.",
    )
    _run(
        pve,
        "rbd bench --io-type read --io-size 4096 --io-total 4096 --io-threads 1 n4-lab/probe",
    )
    assert health.get("health", {}).get("status") == "HEALTH_OK", message(
        en=f"Ceph is not currently healthy: {health.get('health')}",
        fr=f"Ceph n'est pas actuellement sain : {health.get('health')}",
    )
    assert all(
        osd_state.get("up") == 1 and osd_state.get("in") == 1
        for osd_state in osd.get("osds", [])
        if osd_state.get("osd", -1) >= 0
    ), message(
        en="Not all OSDs are recovered up/in.",
        fr="Tous les OSD ne sont pas rétablis up/in.",
    )
    assert "active+clean" in json.dumps(pg), message(
        en="Placement groups have not returned to active+clean.",
        fr="Les groupes de placement ne sont pas revenus à active+clean.",
    )
    pool = json.loads(_run(pve, "ceph osd pool get n4-lab all --format json"))
    assert pool.get("size") == 3 and pool.get("min_size") == 2, message(
        en="The lab pool durability policy changed; do not lower min_size to hide an incident.",
        fr="La politique de durabilité du pool a changé ; n'abaissez pas min_size pour masquer un incident.",
    )
    osd_id = str(
        yaml.safe_load(
            pve.file("/etc/lab-proxmox/pve-eprouver-ceph.yml").content_string
        )["disposable_osd"]
    )
    events = _run(pve, "ceph log last 200").lower()
    assert f"osd.{osd_id} marked out" in events and f"osd.{osd_id} marked in" in events, message(
        en="Ceph monitor history does not show the designated lab OSD being out and restored in.",
        fr="L'historique du moniteur Ceph ne montre pas la mise out puis le rétablissement in de l'OSD dédié au lab.",
    )
