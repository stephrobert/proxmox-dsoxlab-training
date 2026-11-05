"""Un verdict par propriété annoncée ; les lectures impossibles refusent."""


import pytest

from conftest import lab_host, lab_target_host, message
from shared.proxmox_checks import (
    config,
    options,
    read,
    read_json,
    require_equal,
    require_guest_page,
    witness,
)


@pytest.fixture(scope="module")
def pve():
    return lab_host(lab_target_host("pve.lab"))


DIRECTORY = "/opt/lab-proxmox/pve-reparer-agent"


def _ready(pve):
    config(pve, "qm", 180)
    read(pve, "qm agent 180 ping")


def test_le_ping_de_l_agent_repond(pve):
    _ready(pve)


def test_le_peripherique_agent_est_active(pve):
    _ready(pve)
    value = config(pve, "qm", 180).get("agent", "")
    enabled = options(value).get("enabled", value.split(",")[0])
    require_equal(enabled, "1", "guest agent device")


def test_le_canal_est_present(pve):
    _ready(pve)
    result = read_json(pve, "qm guest exec 180 -- test -e /dev/virtio-ports/org.qemu.guest_agent.0", dict)
    require_equal(result.get("exitcode"), 0, "guest agent channel")


def test_l_adresse_remontee_est_celle_du_lab(pve):
    _ready(pve)
    interfaces = read_json(pve, "qm agent 180 network-get-interfaces", list)
    addresses = {a.get("ip-address") for i in interfaces if i.get("name") != "lo" for a in i.get("ip-addresses", [])}
    assert "10.10.113.180" in addresses, message(
        en="Configure guest address 10.10.113.180 and report it through the agent.",
        fr="Configurez l'adresse invitée 10.10.113.180 et remontez-la par l'agent.",
    )


def test_aucun_arret_force_n_a_eu_lieu(pve):
    _ready(pve)
    start = read(pve, f"cat {DIRECTORY}/debut")
    assert start.isdigit(), message(en="Run lab preparation again: start time missing.", fr="Rejouez la préparation : l'heure de début est absente.")
    node = read(pve, "hostname --short")
    tasks = read_json(pve, f"pvesh get /nodes/{node}/tasks --vmid 180 --typefilter qmstop --since {start} --limit 500 --output-format json", list)
    assert not tasks, message(
        en="Use a clean shutdown; a forced stop was recorded.", fr="Utilisez un arrêt propre ; un arrêt forcé a été enregistré.",
    )


def test_la_charge_temoin_est_preservee(pve):
    _ready(pve)
    require_guest_page(pve, "qm", 180, "10.10.113.180", witness(pve, DIRECTORY, "vmid", 180))
