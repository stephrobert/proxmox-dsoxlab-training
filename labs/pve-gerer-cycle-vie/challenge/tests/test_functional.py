"""One scored case per observable requirement."""

import secrets

import pytest

from conftest import lab_host, lab_target_host, message
from shared.deploiement_checks import (
    cleanup_guest,
    configured_vcpus,
    cpu_memory,
    guest,
    manifest,
    snapshot_config,
    snapshot_rollback,
    wait_guest,
)
from shared.proxmox_checks import (
    config,
    options,
    require_equal,
    require_guest_page,
    restart,
    wait_page,
)


@pytest.fixture(scope="module")
def pve():
    return lab_host(lab_target_host("pve.lab"))


LAB = "pve-gerer-cycle-vie"


def ready(pve):
    require_equal(config(pve, "qm", 195).get("memory"), "2048", "memory")


@pytest.mark.parametrize("key,expected", [("memory", "2048"), ("cores", "2"), ("onboot", "1"), ("startup", "order=20")])
def test_une_allocation_declaree(pve, key, expected):
    cfg = config(pve, "qm", 195)
    if key == "cores":
        require_equal(configured_vcpus(cfg), expected, "configured vCPU count")
    elif key == "startup":
        require_equal(options(cfg.get(key, "")).get("order"), options(expected)["order"], "startup order")
    else:
        require_equal(cfg.get(key), expected, key)


@pytest.mark.parametrize("flag,expected", [("-m", "2048"), ("-smp", "2")])
def test_une_allocation_effective(pve, flag, expected):
    ready(pve)
    value = cpu_memory(pve, flag)
    value = options(value).get("size", value) if flag == "-m" else value.split(",")[0]
    require_equal(value, expected, flag)


def test_le_disque_declare_fait_huit_gio(pve):
    require_equal(options(config(pve, "qm", 195).get("scsi0", "")).get("size"), "8G", "scsi0 size")


def test_le_disque_invite_fait_huit_gio(pve):
    ready(pve)
    require_equal(guest(pve, 195, "blockdev --getsize64 /dev/sda"), str(8 * 1024**3), "guest disk bytes")


def test_la_racine_utilise_la_nouvelle_capacite(pve):
    ready(pve)
    size = guest(pve, 195, "findmnt --bytes --noheadings --output SIZE --target /")
    assert size.isdigit() and int(size) >= 7 * 1024**3, message(en="Extend the guest root filesystem to at least 7 GiB.", fr="Étendez le système de fichiers racine invité à au moins 7 Gio.")


def test_la_racine_accepte_une_ecriture(pve):
    ready(pve)
    name = "/root/evaluation-" + secrets.token_hex(6)
    try:
        guest(pve, 195, f"dd if=/dev/zero of={name} bs=1M count=8 conv=fsync")
        require_equal(guest(pve, 195, f"stat -c %s {name}"), str(8 * 1024**2), "bounded root write")
    finally:
        cleanup_guest(pve, 195, f"rm -f {name}")


@pytest.mark.parametrize("key,expected", [("memory", "1024"), ("cores", "1")])
def test_le_snapshot_garde_une_allocation_initiale(pve, key, expected):
    require_equal(snapshot_config(pve).get(key), expected, "snapshot " + key)


def test_le_snapshot_garde_le_disque_initial(pve):
    require_equal(options(snapshot_config(pve).get("scsi0", "")).get("size"), "4G", "snapshot disk size")


def test_le_snapshot_restitue_les_donnees_initiales(pve):
    snapshot_rollback(pve)


def test_la_page_repond_depuis_la_vm(pve):
    ready(pve)
    require_guest_page(pve, "qm", 195, "10.10.113.195", f"temoin {manifest(pve, LAB)['nonce']} vmid 195")


def test_le_service_survit_a_un_redemarrage(pve):
    ready(pve)
    restart(pve, "qm", 195)
    wait_guest(pve, 195)
    wait_page(pve, "10.10.113.195", f"temoin {manifest(pve, LAB)['nonce']} vmid 195")
