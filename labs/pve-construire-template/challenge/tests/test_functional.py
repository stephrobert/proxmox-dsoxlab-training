"""One scored case per observable requirement."""

import shlex
from urllib.parse import unquote

import pytest

from conftest import lab_host, lab_target_host, message
from shared.deploiement_checks import (
    configured_vcpus,
    disk_path,
    manifest,
    require_cloud_init,
    ssh,
    ssh_command,
    ssh_host_key,
    wait_guest,
)
from shared.proxmox_checks import (
    cleanup,
    config,
    options,
    read,
    read_json,
    require_equal,
    require_guest_page,
    run_command,
    wait_page,
)


@pytest.fixture(scope="module")
def pve():
    return lab_host(lab_target_host("pve.lab"))


LAB = "pve-construire-template"
CLONES = [(198, "clone-a"), (199, "clone-b")]


@pytest.mark.parametrize("identifier", [197, 198, 199])
def test_le_marqueur_de_propriete(pve, identifier):
    require_equal(config(pve, "qm", identifier).get("description"), f"dsoxlab-lab={LAB}", "lab ownership")


@pytest.mark.parametrize("identifier,key,expected", [
    (identifier, key, expected)
    for identifier in (198, 199)
    for key, expected in [("memory", "768"), ("cores", "1"), ("ciuser", "debian"),
                          ("nameserver", "10.10.113.1"), ("bridge", "vmbr0"), ("gw", "10.10.113.1")]
])
def test_un_parametre_cloud_init_du_clone(pve, identifier, key, expected):
    cfg = config(pve, "qm", identifier)
    if key == "cores":
        value = configured_vcpus(cfg)
    elif key == "bridge":
        value = options(cfg.get("net0", "")).get(key)
    elif key == "gw":
        value = options(cfg.get("ipconfig0", "")).get(key)
    else:
        value = cfg.get(key)
    require_equal(value, expected, key)


def test_le_template_est_converti(pve):
    require_equal(config(pve, "qm", 197).get("template"), "1", "template flag")


def test_la_recette_est_versionnee(pve):
    require_equal(config(pve, "qm", 197).get("name"), "debian13-cloud-v1", "template recipe name")


def test_le_template_est_arrete(pve):
    config(pve, "qm", 197)
    require_equal(read(pve, "qm status 197"), "status: stopped", "template state")


def test_le_disque_cloud_init_est_present(pve):
    drive = config(pve, "qm", 197).get("ide2", "")
    assert "cloudinit" in drive.split(",")[0] and options(drive).get("media") == "cdrom", message(en="Attach the template cloud-init drive as ide2.", fr="Raccordez le disque cloud-init du template sur ide2.")


def test_le_disque_correspond_a_l_image_verifiee(pve):
    data = manifest(pve, LAB)
    require_equal(read(pve, "sha512sum " + shlex.quote(data["image"])).split()[0], data["sha512"], "source image SHA-512")
    read(pve, "qemu-img compare -U " + shlex.quote(data["image"]) + " " + shlex.quote(disk_path(pve, 197)))


def test_la_recette_vendor_est_transmise(pve):
    require_equal(options(config(pve, "qm", 197).get("cicustom", "")).get("vendor"), f"local:snippets/{LAB}.yaml", "cloud-init vendor data")


@pytest.mark.parametrize("identifier,name", CLONES)
def test_le_clone_porte_son_nom(pve, identifier, name):
    require_equal(config(pve, "qm", identifier).get("name"), name, "clone name")


@pytest.mark.parametrize("identifier,name", CLONES)
def test_le_clone_a_son_adresse(pve, identifier, name):
    require_equal(options(config(pve, "qm", identifier).get("ipconfig0", "")).get("ip"), f"10.10.113.{identifier}/24", "clone IPv4")


@pytest.mark.parametrize("identifier,name", CLONES)
def test_la_cle_autorisee_est_propre_au_clone(pve, identifier, name):
    lines = unquote(config(pve, "qm", identifier).get("sshkeys", "")).strip().splitlines()
    require_equal(len(lines), 1, "authorized cloud-init key count")
    value = lines[0].split()
    expected = read(pve, f"cat /opt/lab-proxmox/{LAB}/keys/{name}.pub").split()
    require_equal(value[:2], expected[:2], "cloud-init public key")
    require_equal(len(value[:2]), 2, "public key fields")


@pytest.mark.parametrize("identifier,name", CLONES)
def test_le_clone_accepte_sa_cle(pve, identifier, name):
    require_equal(ssh(pve, identifier, name, "id -un"), "debian", "SSH user")


@pytest.mark.parametrize("identifier,name", CLONES)
def test_le_clone_refuse_l_autre_cle(pve, identifier, name):
    ssh(pve, identifier, name, "true")
    other = "clone-b" if name == "clone-a" else "clone-a"
    result = run_command(pve, ssh_command(identifier, other, "true") + " 2>&1; printf '\nSSH_RC=%s\n' $?")
    assert "SSH_RC=255" in result.stdout and "Permission denied" in result.stdout, message(en="Authorize only this clone's assigned key; SSH must deny the other key.", fr="N'autorisez que la clé attribuée à ce clone ; SSH doit refuser l'autre clé.")


@pytest.mark.parametrize("identifier,name", CLONES)
def test_le_nom_invite_est_personnalise(pve, identifier, name):
    require_equal(ssh(pve, identifier, name, "hostname --short"), name, "guest hostname")


@pytest.mark.parametrize("identifier,name", CLONES)
def test_cloud_init_est_termine(pve, identifier, name):
    require_cloud_init(pve, identifier)


@pytest.mark.parametrize("identifier,name", CLONES)
def test_le_service_identifie_le_clone(pve, identifier, name):
    config(pve, "qm", identifier)
    require_guest_page(pve, "qm", identifier, f"10.10.113.{identifier}", f"temoin {manifest(pve, LAB)['nonce']} vmid {identifier}")


@pytest.mark.parametrize("property_", ["mac", "machine-id", "host-key"])
def test_une_identite_est_distincte(pve, property_):
    if property_ == "mac":
        values = [config(pve, "qm", identifier).get("net0", "").split(",")[0].partition("=")[2] for identifier, _ in CLONES]
    elif property_ == "host-key":
        values = [ssh_host_key(pve, identifier) for identifier, _ in CLONES]
    else:
        values = [ssh(pve, identifier, name, "cat /etc/machine-id") for identifier, name in CLONES]
    assert all(values) and values[0] != values[1], message(en=f"Regenerate independent clone identity: {property_}.", fr=f"Régénérez une identité indépendante par clone : {property_}.")


def test_un_nouveau_clone_rejoue_la_recette(pve):
    resources = read_json(pve, "pvesh get /cluster/resources --type vm --output-format json", list)
    assert all(int(row["vmid"]) != 196 for row in resources), message(en="Free the evaluator's reserved VMID 196.", fr="Libérez le VMID 196 réservé à l'évaluateur.")
    try:
        read(pve, "qm clone 197 196 --full 1 --name clone-b")
        read(pve, f"qm set 196 --description dsoxlab-lab={LAB} --memory 512 --cores 1 --ipconfig0 ip=10.10.113.196/24,gw=10.10.113.1 --ciuser debian --sshkeys /opt/lab-proxmox/{LAB}/keys/clone-b.pub")
        read(pve, "qm start 196")
        wait_guest(pve, 196, seconds=360)
        wait_page(pve, "10.10.113.196", f"temoin {manifest(pve, LAB)['nonce']} vmid 199", seconds=360)
        require_guest_page(pve, "qm", 196, "10.10.113.196", f"temoin {manifest(pve, LAB)['nonce']} vmid 199")
    finally:
        cleanup(pve, "qm stop 196")
        cleanup(pve, "qm destroy 196 --purge 1 --destroy-unreferenced-disks 1")
