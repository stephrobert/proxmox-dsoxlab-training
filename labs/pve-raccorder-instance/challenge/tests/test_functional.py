"""Un verdict par propriété annoncée ; les lectures impossibles refusent."""

import json

import pytest

from conftest import lab_host, lab_target_host, message
from shared.proxmox_checks import (
    config,
    options,
    physical_bridge_ports,
    read,
    read_json,
    require_equal,
    require_guest_page,
    require_page,
    restart,
    wait_page,
    witness,
)


@pytest.fixture(scope="module")
def pve():
    return lab_host(lab_target_host("pve.lab"))


DIRECTORY = "/opt/lab-proxmox/pve-raccorder-instance"
ADDRESS = "10.10.113.160"


def _ready(pve):
    values = config(pve, "qm", 160)
    require_equal(options(values.get("net0", "")).get("bridge"), "vmbr0", "net0 bridge")
    require_page(pve, ADDRESS, witness(pve, DIRECTORY, "vmid", 160))
    return values


def test_net0_designe_exactement_vmbr0(pve):
    require_equal(options(config(pve, "qm", 160).get("net0", "")).get("bridge"), "vmbr0", "net0 bridge")


def test_le_port_effectif_appartient_a_vmbr0(pve):
    _ready(pve)
    ports = read_json(pve, "bridge -j link show master vmbr0", list)
    assert any(p.get("ifname") == "tap160i0" for p in ports), message(
        en="Apply the VM card change so tap160i0 joins vmbr0.", fr="Appliquez la modification pour rattacher tap160i0 à vmbr0.",
    )


def test_la_page_temoin_repond(pve):
    _ready(pve)
    require_guest_page(pve, "qm", 160, ADDRESS, witness(pve, DIRECTORY, "vmid", 160))


def test_vmbr9_reste_sans_port_physique(pve):
    _ready(pve)
    assert not physical_bridge_ports(pve, "vmbr9"), message(
        en="Keep physical interfaces out of vmbr9.", fr="Gardez les interfaces physiques hors de vmbr9.",
    )


def test_la_vm_n_a_pas_ete_recreee(pve):
    values = _ready(pve)
    reference = json.loads(read(pve, f"cat {DIRECTORY}/identite.json"))
    node = read(pve, "hostname --short")
    current = read_json(pve, f"pvesh get /nodes/{node}/tasks --vmid 160 --typefilter qmcreate --limit 500 --output-format json", list)
    require_equal({t["upid"] for t in current}, set(reference["creation_tasks"]), "VM creation history")
    require_equal(values.get("smbios1"), reference["smbios1"], "VM identity")


def test_la_correction_survit_au_redemarrage(pve):
    _ready(pve)
    restart(pve, "qm", 160)
    wait_page(pve, ADDRESS, witness(pve, DIRECTORY, "vmid", 160))


def test_la_correction_survit_au_rechargement_reseau(pve):
    _ready(pve)
    read(pve, "mkdir -p /run/network && ifreload -a")
    wait_page(pve, ADDRESS, witness(pve, DIRECTORY, "vmid", 160))
