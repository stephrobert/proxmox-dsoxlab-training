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

def test_node_metrics_and_notification_route_are_persisted(pve):
    node = pve.run("hostname -s")
    assert node.rc == 0 and node.stdout.strip(), message(en="Cannot identify the PVE node for its metric query.", fr="Impossible d’identifier le nœud PVE pour interroger ses métriques.")
    metrics = pve.run(f"pvesh get /nodes/{node.stdout.strip()}/rrddata --timeframe hour --output-format json")
    assert metrics.rc == 0 and len(json.loads(metrics.stdout)) > 0, message(en="PVE has no actual node metric samples for the last hour.", fr="PVE ne dispose d’aucun échantillon réel de métrique du nœud pour la dernière heure.")
    cfg = pve.file("/etc/pve/notifications.cfg")
    assert cfg.exists and "lab-n2-210" in cfg.content_string, message(en="The named local notification target/matcher is not persisted in PVE.", fr="La cible/règle de notification locale nommée n’est pas persistée dans PVE.")
    assert "matcher" in cfg.content_string, message(en="No notification matcher routes the alert to the receiver.", fr="Aucune règle de notification ne route l’alerte vers le récepteur.")
