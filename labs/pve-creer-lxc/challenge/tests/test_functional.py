"""Un verdict par propriété annoncée ; les lectures impossibles refusent."""

import re
import secrets

import pytest

from conftest import lab_host, lab_target_host, message
from shared.proxmox_checks import (
    cgroup,
    cleanup,
    config,
    cpu_count,
    options,
    read,
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


DIRECTORY = "/opt/lab-proxmox/pve-creer-lxc"
ADDRESS = "10.10.113.170"


@pytest.mark.parametrize("key,expected", [
    ("hostname", "ct-web"), ("unprivileged", "1"), ("memory", "512"),
    ("swap", "0"), ("cores", "1"),
])
def test_une_propriete_du_conteneur(pve, key, expected):
    require_equal(config(pve, "pct", 170).get(key), expected, key)


def test_le_stockage_est_local(pve):
    assert config(pve, "pct", 170).get("rootfs", "").startswith("local:"), message(
        en="Create the container root disk on local.", fr="Créez le disque racine du conteneur sur local.",
    )


@pytest.mark.parametrize("key,expected", [("bridge", "vmbr0"), ("ip", "10.10.113.170/24"), ("gw", "10.10.113.1")])
def test_une_propriete_reseau(pve, key, expected):
    require_equal(options(config(pve, "pct", 170).get("net0", "")).get(key), expected, key)


def test_le_dns_est_celui_du_manifeste(pve):
    require_equal(config(pve, "pct", 170).get("nameserver"), "10.10.113.1", "DNS")


def test_le_conteneur_tourne(pve):
    config(pve, "pct", 170)
    require_equal(read(pve, "pct status 170"), "status: running", "CT 170")


def test_root_est_effectivement_decale(pve):
    config(pve, "pct", 170)
    rows = read(pve, "pct exec 170 -- cat /proc/self/uid_map").splitlines()
    mappings = [list(map(int, row.split())) for row in rows]
    assert any(len(row) == 3 and row[0] == 0 and row[1] >= 100000 and row[2] > 0 for row in mappings), message(
        en="Map container root to an unprivileged host UID.", fr="Projetez root du conteneur sur un UID non privilégié de l'hôte.",
    )


def test_la_distribution_est_debian_13(pve):
    config(pve, "pct", 170)
    output = read(pve, "pct exec 170 -- cat /etc/os-release")
    values = dict(line.split("=", 1) for line in output.splitlines() if "=" in line)
    require_equal((values.get("ID", "").strip('"'), values.get("VERSION_ID", "").strip('"')), ("debian", "13"), "distribution")


def test_python3_est_installe(pve):
    config(pve, "pct", 170)
    read(pve, "pct exec 170 -- python3 --version")


def test_web_est_un_compte_systeme(pve):
    config(pve, "pct", 170)
    uid = int(read(pve, "pct exec 170 -- id -u web"))
    limit = read(pve, "pct exec 170 -- cat /etc/login.defs")
    match = re.search(r"^UID_MIN\s+(\d+)", limit, re.M)
    assert match and 0 < uid < int(match[1]), message(
        en="Create web as a non-root system account.", fr="Créez web comme compte système non root.",
    )


def test_la_page_temoin_repond(pve):
    config(pve, "pct", 170)
    require_guest_page(pve, "pct", 170, ADDRESS, witness(pve, DIRECTORY, "ctid", 170))


def test_le_processus_qui_ecoute_appartient_a_web(pve):
    config(pve, "pct", 170)
    sockets = read(pve, "pct exec 170 -- ss -H -ltnp 'sport = :8080'")
    pids = sorted(set(re.findall(r"pid=(\d+)", sockets)))
    assert pids, message(en="Start the HTTP listener on port 8080.", fr="Démarrez le serveur HTTP sur le port 8080.")
    owners = read(pve, f"pct exec 170 -- ps -o user= -p {','.join(pids)}").split()
    require_equal(set(owners), {"web"}, "HTTP listener owner")


@pytest.mark.parametrize("filename,expected", [("memory.max", str(512 * 1024 * 1024)), ("memory.swap.max", "0")])
def test_une_limite_memoire_effective(pve, filename, expected):
    config(pve, "pct", 170)
    require_equal(cgroup(pve, 170, filename), expected, filename)


def test_un_seul_cpu_est_effectif(pve):
    config(pve, "pct", 170)
    require_equal(cpu_count(cgroup(pve, 170, "cpuset.cpus.effective")), 1, "effective CPU count")


def test_les_donnees_survivent_au_redemarrage(pve):
    config(pve, "pct", 170)
    marker = secrets.token_hex(16)
    filename = f"/root/marqueur-lab-{marker}"
    try:
        read(pve, f"pct exec 170 -- sh -c 'printf %s {marker} > {filename}'")
        restart(pve, "pct", 170)
        require_equal(read(pve, f"pct exec 170 -- cat {filename}"), marker, "persistent data")
    finally:
        cleanup(pve, f"pct exec 170 -- rm -f {filename}")


def test_le_service_survit_au_redemarrage(pve):
    config(pve, "pct", 170)
    expected = witness(pve, DIRECTORY, "ctid", 170)
    require_page(pve, ADDRESS, expected)
    restart(pve, "pct", 170)
    wait_page(pve, ADDRESS, expected)
