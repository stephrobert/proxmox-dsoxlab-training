"""Un verdict par propriété annoncée ; les lectures impossibles refusent."""

import re

import pytest

from conftest import lab_host, lab_target_host, message
from shared.proxmox_checks import (
    active_repository,
    read,
    read_json,
    require_equal,
    run_command,
)


@pytest.fixture(scope="module")
def pve():
    return lab_host(lab_target_host("pve.lab"))


def _installation(pve):
    return read(pve, "pveversion")


def test_proxmox_est_installe(pve):
    assert "pve-manager/" in _installation(pve), message(
        en="Install Proxmox VE so pveversion reports pve-manager.",
        fr="Installez Proxmox VE pour que pveversion annonce pve-manager.",
    )


def test_la_version_est_bien_une_9(pve):
    found = re.search(r"pve-manager/(\d+)\.", _installation(pve))
    assert found and int(found[1]) >= 9, message(
        en="Install Proxmox VE version 9 or later.",
        fr="Installez Proxmox VE en version 9 ou ultérieure.",
    )


@pytest.mark.parametrize("service", ["pve-cluster", "pvedaemon", "pveproxy"])
def test_un_service_proxmox_est_actif(pve, service):
    _installation(pve)
    result = run_command(pve, f"systemctl is-active {service}")
    assert result.rc == 0 and result.stdout.strip() == "active", message(
        en=f"Start service {service}; observed {result.stdout.strip()!r}: {result.stderr}",
        fr=f"Démarrez le service {service} ; état observé : {result.stdout.strip()!r} : {result.stderr}",
    )


def test_l_interface_web_repond(pve):
    _installation(pve)
    require_equal(read(pve, "curl --fail -sk --max-time 15 -o /dev/null -w '%{http_code}' https://127.0.0.1:8006/"), "200", "HTTP 8006")


def test_le_port_web_appartient_a_pveproxy(pve):
    _installation(pve)
    output = read(pve, "ss -H -ltnp 'sport = :8006'")
    assert '"pveproxy"' in output, message(
        en="Serve port 8006 with pveproxy.", fr="Servez le port 8006 avec pveproxy.",
    )


def test_le_pont_porte_l_adresse_du_serveur(pve):
    _installation(pve)
    address = read(pve, "hostname --ip-address").split()
    links = read_json(pve, "ip -j -4 address show dev vmbr0", list)
    observed = {a.get("local") for link in links for a in link.get("addr_info", [])}
    assert address and set(address) & observed, message(
        en="Move the server IPv4 address onto vmbr0.",
        fr="Placez l'adresse IPv4 du serveur sur vmbr0.",
    )


def test_le_depot_sans_abonnement_est_actif(pve):
    _installation(pve)
    output = read(pve, r"find /etc/apt -maxdepth 2 -type f \( -name '*.list' -o -name '*.sources' \) -exec cat {} \; -exec echo \;")
    assert active_repository(output), message(
        en="Enable a complete pve-no-subscription repository entry.",
        fr="Activez une entrée complète du dépôt pve-no-subscription.",
    )


def test_les_index_apt_se_telechargent(pve):
    _installation(pve)
    read(pve, "apt-get update -qq -o APT::Update::Error-Mode=any 2>&1")
