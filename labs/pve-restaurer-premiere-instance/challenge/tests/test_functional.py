"""One scored case per observable requirement."""

import re
import shlex

import pytest

from conftest import lab_host, lab_target_host, message
from shared.deploiement_checks import (
    archive_command,
    disk_path,
    guest,
    manifest,
    restore_service,
    restored_page,
    wait_guest,
)
from shared.proxmox_checks import (
    config,
    options,
    physical_bridge_ports,
    read,
    read_json,
    require_equal,
    require_page,
    restart,
    run_command,
    wait_page,
)


@pytest.fixture(scope="module")
def pve():
    return lab_host(lab_target_host("pve.lab"))


LAB = "pve-restaurer-premiere-instance"


def ready(pve):
    config(pve, "qm", 199)


def test_le_marqueur_de_propriete(pve):
    require_equal(config(pve, "qm", 199).get("description"), f"dsoxlab-lab={LAB}", "lab ownership")


def test_l_archive_est_un_vma_complet_lisible(pve):
    archive_command(pve, "verify")


def test_l_archive_contient_le_disque_systeme(pve):
    output = archive_command(pve, "list")
    match = re.search(r"(?m)^DEV:.*\bsize:\s*(\d+)\s+devname:\s*drive-scsi0\s*$", output)
    assert match and int(match[1]) == 4 * 1024**3, message(en="Include the complete 4 GiB scsi0 system disk in the vzdump backup.", fr="Incluez le disque système scsi0 complet de 4 Gio dans la sauvegarde vzdump.")


def test_une_tache_de_restauration_a_reussi(pve):
    ready(pve)
    node = read(pve, "hostname --short")
    data = manifest(pve, LAB)
    tasks = read_json(pve, f"pvesh get /nodes/{node}/tasks --vmid 199 --typefilter qmrestore --since {data['begin']} --limit 500 --output-format json", list)
    assert any(task.get("status") == "OK" for task in tasks), message(en="Restore the archive to VMID 199 with qmrestore or the equivalent UI action.", fr="Restaurez l'archive vers le VMID 199 avec qmrestore ou l'action équivalente de l'interface.")


def test_le_disque_restaure_est_independant(pve):
    restored = disk_path(pve, 199)
    assert restored != disk_path(pve, 198), message(en="Use a distinct restored disk.", fr="Utilisez un disque restauré distinct.")
    chain = read_json(pve, "qemu-img info -U --backing-chain --output=json " + shlex.quote(restored), list)
    assert len(chain) == 1 and not chain[0].get("backing-filename"), message(en="Restore a complete independent disk without a backing file.", fr="Restaurez un disque complet indépendant sans fichier de base partagé.")


def test_la_vm_restauree_tourne(pve):
    ready(pve)
    require_equal(read(pve, "qm status 199"), "status: running", "restored VM")


def test_la_vm_restauree_est_sur_le_reseau_isole(pve):
    require_equal(options(config(pve, "qm", 199).get("net0", "")).get("bridge"), "vmbr9", "restored bridge")


def test_la_vm_restauree_n_a_pas_de_seconde_carte(pve):
    cfg = config(pve, "qm", 199)
    require_equal([key for key in cfg if key.startswith("net") and key != "net0"], [], "additional restored interfaces")


def test_les_adresses_mac_sont_distinctes(pve):
    values = [config(pve, "qm", identifier).get("net0", "").split(",")[0].partition("=")[2] for identifier in (198, 199)]
    assert all(values) and values[0] != values[1], message(en="Generate a new MAC address for the restored VM.", fr="Générez une nouvelle adresse MAC pour la VM restaurée.")


def test_le_marqueur_anterieur_est_restaure(pve):
    ready(pve)
    require_equal(guest(pve, 199, "cat /srv/temoin/index.html"), f"temoin {manifest(pve, LAB)['nonce']} vmid 198", "restored data")


def test_le_client_isole_lit_le_service_restaure(pve):
    ready(pve)
    restored_page(pve)


def test_la_restauration_fonctionne_source_arretee(pve):
    ready(pve)
    nonce = manifest(pve, LAB)["nonce"]
    require_equal(read(pve, "qm status 198"), "status: running", "source before measurement")
    try:
        read(pve, "qm shutdown 198 --timeout 120")
        require_equal(read(pve, "qm status 198"), "status: stopped", "isolated source")
        restart(pve, "qm", 199)
        wait_guest(pve, 199)
        restored_page(pve)
    finally:
        restore_service(pve, 198, "10.10.113.198", f"temoin {nonce} vmid 198")
    wait_guest(pve, 198)
    wait_page(pve, "10.10.113.198", f"temoin {nonce} vmid 198")


def test_la_configuration_source_est_preservee(pve):
    ready(pve)
    require_equal(read(pve, "sha256sum /etc/pve/qemu-server/198.conf").split()[0], manifest(pve, LAB)["source_config_sha256"], "source configuration")


def test_le_service_source_est_preserve(pve):
    ready(pve)
    require_page(pve, "10.10.113.198", f"temoin {manifest(pve, LAB)['nonce']} vmid 198")


def test_le_pont_restauration_reste_sans_port_physique(pve):
    ready(pve)
    require_equal(physical_bridge_ports(pve, "vmbr9"), [], "isolated bridge physical ports")


def test_le_client_ne_joint_pas_la_gestion(pve):
    ready(pve)
    interfaces = read_json(pve, "ip -j -4 addr show dev vmbr0", list)
    addresses = [address["local"] for interface in interfaces for address in interface.get("addr_info", []) if address.get("family") == "inet"]
    assert addresses, message(en="Cannot locate the node's management IPv4 address.", fr="Impossible de localiser l'adresse IPv4 de gestion du nœud.")
    command = f"curl --noproxy '*' --insecure --silent --show-error --max-time 5 --output /dev/null --write-out '%{{http_code}}' https://{addresses[0]}:8006/"
    require_equal(read(pve, command), "200", "management service before isolation probe")
    result = run_command(pve, "ip netns exec dsox-restore " + command)
    assert result.rc in (7, 28) and result.stdout.strip() == "000", message(
        en="Keep the restore client isolated: it must not reach the node's HTTPS management service on port 8006.",
        fr="Gardez le client de restauration isolé : il ne doit pas joindre le service HTTPS de gestion du nœud sur le port 8006.",
    )
