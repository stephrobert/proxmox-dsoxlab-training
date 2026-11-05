"""Un verdict par propriété annoncée ; les lectures impossibles refusent."""


import pytest

from conftest import lab_host, lab_target_host, message
from shared.proxmox_checks import (
    config,
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


DIRECTORY = "/opt/lab-proxmox/pve-creer-vm"
ADDRESS = "10.10.113.150"


@pytest.mark.parametrize("key,expected", [
    ("name", "web-temoin"), ("machine", "q35"), ("bios", "ovmf"),
    ("cpu", "host"), ("scsihw", "virtio-scsi-single"),
])
def test_une_propriete_materielle(pve, key, expected):
    value = config(pve, "qm", 150).get(key, "").split(",")[0]
    require_equal(value, expected, key)


@pytest.mark.parametrize("disk", ["efidisk0", "scsi0"])
def test_un_disque_est_sur_local(pve, disk):
    value = config(pve, "qm", 150).get(disk, "")
    assert value.startswith("local:"), message(
        en=f"Create {disk} on local storage.", fr=f"Créez {disk} sur le stockage local.",
    )


def test_la_carte_est_virtio(pve):
    require_equal(config(pve, "qm", 150).get("net0", "").split("=")[0], "virtio", "net0 model")


def test_le_pont_est_vmbr0(pve):
    require_equal(options(config(pve, "qm", 150).get("net0", "")).get("bridge"), "vmbr0", "net0 bridge")


def test_le_plafond_memoire(pve):
    memory = int(config(pve, "qm", 150).get("memory", "0"))
    assert 0 < memory <= 2048, message(
        en="Allocate between 1 and 2048 MB to VM 150.", fr="Attribuez entre 1 et 2048 Mo à la VM 150.",
    )


def test_le_plafond_cpu(pve):
    values = config(pve, "qm", 150)
    count = int(values.get("cores", "1")) * int(values.get("sockets", "1"))
    assert 0 < count <= 2, message(
        en="Allocate at most two virtual CPUs to VM 150.", fr="Attribuez au plus deux CPU virtuels à la VM 150.",
    )


def test_aucune_iso_inseree(pve):
    values = config(pve, "qm", 150)
    assert not any("iso/" in value for value in values.values()), message(
        en="Remove the installation ISO.", fr="Retirez l'ISO d'installation.",
    )


def test_scsi0_est_premier(pve):
    order = options(config(pve, "qm", 150).get("boot", "")).get("order", "")
    require_equal(order.split(";")[0], "scsi0", "boot order")


def test_la_vm_tourne(pve):
    config(pve, "qm", 150)
    require_equal(read(pve, "qm status 150"), "status: running", "VM 150")


def test_la_page_temoin_repond(pve):
    config(pve, "qm", 150)
    require_guest_page(pve, "qm", 150, ADDRESS, witness(pve, DIRECTORY, "vmid", 150))


def test_le_service_survit_a_un_redemarrage_effectif(pve):
    config(pve, "qm", 150)
    expected = witness(pve, DIRECTORY, "vmid", 150)
    require_page(pve, ADDRESS, expected)
    restart(pve, "qm", 150)
    wait_page(pve, ADDRESS, expected)
