from __future__ import annotations

import pytest

from conftest import lab_host, lab_target_host, message

HOTE = lab_target_host("pve.lab")
TEMPLATE, CLONE = 197, 198


@pytest.fixture(scope="module")
def pve():
    return lab_host(HOTE)


def test_le_template_cloud_init_est_converti_et_arrete(pve):
    cfg = pve.run(f"qm config {TEMPLATE}")
    assert cfg.rc == 0 and "template: 1" in cfg.stdout, message(
        en=f"VM {TEMPLATE} is not registered as a Proxmox template.",
        fr=f"La VM {TEMPLATE} n'est pas enregistrée comme template Proxmox.",
    )
    assert "cloudinit" in cfg.stdout.lower(), message(
        en="The template has no cloud-init drive.", fr="Le template n'a pas de disque cloud-init."
    )
    assert "running" not in pve.run(f"qm status {TEMPLATE}").stdout, message(
        en="A template must not be running.", fr="Un template ne doit pas tourner."
    )


def test_le_clone_recoit_sa_configuration_cloud_init(pve):
    cfg = pve.run(f"qm config {CLONE}")
    assert cfg.rc == 0, message(en=f"Clone {CLONE} is missing.", fr=f"Le clone {CLONE} manque.")
    assert "ipconfig0:" in cfg.stdout and "ciuser:" in cfg.stdout, message(
        en="The clone has no per-instance cloud-init user and network settings.",
        fr="Le clone n'a pas de paramètres utilisateur et réseau cloud-init propres.",
    )
    assert pve.run(f"qm status {CLONE}").stdout.strip().endswith("running"), message(
        en="The cloud-init clone is not running.", fr="Le clone cloud-init ne tourne pas."
    )
