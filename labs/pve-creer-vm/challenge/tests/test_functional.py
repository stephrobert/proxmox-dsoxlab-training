"""Note la VM 150 que l'apprenant a créée, installée et mise en service.

Le contrat du TP `pve-creer-vm` (src/data/parcours/proxmox.yaml du site) fixe
ce qui est prouvé : la VM respecte le contrat matériel de la leçon, elle
démarre sur son disque sans ISO, et son service répond depuis un client qui
n'est pas l'invité. Les tests jouent ce client depuis le nœud Proxmox.

Ils interrogent l'ÉTAT, jamais les commandes : une VM installée depuis l'ISO à
la main, comme le fait la leçon, et une VM posée depuis une image cloud
passent de la même façon si elles atteignent le même état.

Le dernier test REDÉMARRE la VM. C'est voulu : une VM qui ne répond qu'avant
son premier redémarrage, parce qu'elle démarre encore sur l'installateur ou
que son service n'est pas activé, n'est pas en service.
"""

from __future__ import annotations

import re
import time

import pytest

from conftest import lab_host, lab_target_host, message

CIBLE = lab_target_host("pve.lab")
VMID = 150
ADRESSE = "10.10.113.150"
PORT = 8080
NONCE = "/opt/lab-proxmox/pve-creer-vm/nonce"
RAM_MAX_MO = 2048
COEURS_MAX = 2


@pytest.fixture(scope="module")
def pve():
    return lab_host(CIBLE)


def _config(hote) -> dict[str, str]:
    """La configuration de la VM, telle que Proxmox la tient."""
    res = hote.run(f"qm config {VMID}")
    if res.rc != 0:
        return {}
    config = {}
    for ligne in res.stdout.splitlines():
        cle, _, valeur = ligne.partition(":")
        config[cle.strip()] = valeur.strip()
    return config


def _exiger_vm(hote) -> dict[str, str]:
    config = _config(hote)
    assert config, message(
        en=f"VM {VMID} does not exist. Create it with the VMID given in the lab manifest.",
        fr=f"La VM {VMID} n'existe pas. Créez-la avec le VMID donné par le manifeste du lab.",
    )
    return config


def _ligne_attendue(hote) -> str:
    nonce = hote.file(NONCE).content_string.strip()
    return f"temoin {nonce} vmid {VMID}"


def _page(hote) -> str:
    res = hote.run(f"curl -s --max-time 5 http://{ADRESSE}:{PORT}/")
    return res.stdout if res.rc == 0 else ""


def test_la_vm_respecte_le_contrat_materiel(pve) -> None:
    config = _exiger_vm(pve)
    ecarts = []
    if config.get("machine", "") != "q35":
        ecarts.append(f"machine={config.get('machine', 'i440fx (défaut)')}, attendu q35")
    if config.get("bios") != "ovmf":
        ecarts.append(f"bios={config.get('bios', 'seabios (défaut)')}, attendu ovmf")
    if "efidisk0" not in config:
        ecarts.append("pas de disque EFI (efidisk0), obligatoire avec OVMF")
    if config.get("cpu", "").split(",")[0] != "host":
        ecarts.append(f"cpu={config.get('cpu', 'x86-64-v2-AES (défaut)')}, attendu host")
    if config.get("scsihw") != "virtio-scsi-single":
        ecarts.append(f"scsihw={config.get('scsihw', 'lsi (défaut)')}, attendu virtio-scsi-single")
    if not config.get("scsi0"):
        ecarts.append("pas de disque scsi0")
    reseau = config.get("net0", "")
    if not reseau.startswith("virtio") or "bridge=vmbr0" not in reseau:
        ecarts.append(f"net0={reseau or 'absent'}, attendu une carte virtio sur vmbr0")
    if int(config.get("memory", "512")) > RAM_MAX_MO:
        ecarts.append(f"memory={config['memory']} Mo, plafond {RAM_MAX_MO}")
    if int(config.get("cores", "1")) * int(config.get("sockets", "1")) > COEURS_MAX:
        ecarts.append(f"{config.get('cores')} cœurs, plafond {COEURS_MAX}")
    assert not ecarts, message(
        en=f"VM {VMID} does not match the lesson's hardware contract:\n  " + "\n  ".join(ecarts),
        fr=f"La VM {VMID} ne respecte pas le contrat matériel de la leçon :\n  " + "\n  ".join(ecarts),
    )


def test_la_vm_demarre_sur_son_disque_sans_iso(pve) -> None:
    config = _exiger_vm(pve)
    isos = [cle for cle, valeur in config.items() if "iso/" in valeur]
    assert not isos, message(
        en=(
            f"An installation ISO is still attached ({', '.join(isos)}). "
            "Once Debian is installed, remove the medium (CD/DVD: do not use any media)."
        ),
        fr=(
            f"Une ISO d'installation est encore insérée ({', '.join(isos)}). "
            "Une fois Debian installé, retirez le média (CD/DVD : Do not use any media)."
        ),
    )
    ordre = re.search(r"order=([^,\s]+)", config.get("boot", ""))
    premier = ordre.group(1).split(";")[0] if ordre else ""
    assert premier == "scsi0", message(
        en=f"The VM does not boot first on its disk: boot={config.get('boot', 'absent')}. Put scsi0 first.",
        fr=f"La VM ne démarre pas d'abord sur son disque : boot={config.get('boot', 'absent')}. Placez scsi0 en tête.",
    )
    etat = pve.run(f"qm status {VMID}").stdout
    assert "running" in etat, message(
        en=f"VM {VMID} is not running ({etat.strip()}).",
        fr=f"La VM {VMID} ne tourne pas ({etat.strip()}).",
    )


def test_le_service_repond_depuis_le_client(pve) -> None:
    _exiger_vm(pve)
    attendu = _ligne_attendue(pve)
    page = _page(pve)
    assert page, message(
        en=(
            f"Nothing answers on http://{ADRESSE}:{PORT}/ from the node. Check, in order: "
            "the VM address, its gateway, then that the service listens (ss -tlnp)."
        ),
        fr=(
            f"Rien ne répond sur http://{ADRESSE}:{PORT}/ depuis le nœud. Vérifiez dans l'ordre : "
            "l'adresse de la VM, sa passerelle, puis que le service écoute (ss -tlnp)."
        ),
    )
    assert attendu in page, message(
        en=f"The page answers but does not contain the expected line:\n  {attendu}",
        fr=f"La page répond, mais ne contient pas la ligne attendue :\n  {attendu}",
    )


def test_le_service_revient_apres_un_redemarrage(pve) -> None:
    _exiger_vm(pve)
    attendu = _ligne_attendue(pve)
    assert attendu in _page(pve), message(
        en="The service does not answer before the reboot: fix the previous test first.",
        fr="Le service ne répond pas avant le redémarrage : corrigez d'abord le test précédent.",
    )
    pve.run(f"qm reboot {VMID} --timeout 120")
    # On attend un état réel, borné, jamais une durée fixe prise pour une preuve.
    limite = time.monotonic() + 240
    while time.monotonic() < limite:
        if attendu in _page(pve):
            return
        time.sleep(5)
    raise AssertionError(
        message(
            en=(
                "After a reboot, the service no longer answers. Either the VM boots on "
                "something other than its disk, or the service is not enabled (systemctl enable)."
            ),
            fr=(
                "Après un redémarrage, le service ne répond plus. Soit la VM démarre sur "
                "autre chose que son disque, soit le service n'est pas activé (systemctl enable)."
            ),
        )
    )
