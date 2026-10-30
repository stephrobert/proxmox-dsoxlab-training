"""Note le raccordement de la VM témoin 160 au réseau du lab.

Contrat du TP `pve-raccorder-instance` (src/data/parcours/proxmox.yaml du
site) : la carte invitée est reliée au bon pont, le client reçoit la réponse
de la BONNE instance, la panne est corrigée au bon étage, et la correction
survit à un redémarrage ciblé. Le nœud joue le client.

Le setup a branché la carte sur `vmbr9`, un pont isolé. Corriger « au bon
étage », c'est rebrancher la carte de CETTE VM sur `vmbr0` : ni recréer la VM,
dont le disque porte le nonce, ni donner une carte physique au pont isolé.
"""

from __future__ import annotations

import re
import time

import pytest

from conftest import lab_host, lab_target_host, message

CIBLE = lab_target_host("pve.lab")
VMID = 160
ADRESSE = "10.10.113.160"
PORT = 8080
NONCE = "/opt/lab-proxmox/pve-raccorder-instance/nonce"


@pytest.fixture(scope="module")
def pve():
    return lab_host(CIBLE)


def _net0(hote) -> str:
    res = hote.run(f"qm config {VMID}")
    m = re.search(r"^net0:\s*(\S+)", res.stdout, re.M)
    return m.group(1) if m else ""


def _ligne_attendue(hote) -> str:
    return f"temoin {hote.file(NONCE).content_string.strip()} vmid {VMID}"


def _page(hote) -> str:
    res = hote.run(f"curl -s --max-time 5 http://{ADRESSE}:{PORT}/")
    return res.stdout if res.rc == 0 else ""


def _attendre_page(hote, attendu: str, secondes: int) -> bool:
    limite = time.monotonic() + secondes
    while time.monotonic() < limite:
        if attendu in _page(hote):
            return True
        time.sleep(5)
    return False


def test_la_carte_est_reliee_au_pont_du_lab(pve) -> None:
    net0 = _net0(pve)
    assert net0, message(
        en=f"VM {VMID} has no net0 card. Do not recreate the VM: its disk carries the witness page.",
        fr=f"La VM {VMID} n'a pas de carte net0. Ne recréez pas la VM : son disque porte la page témoin.",
    )
    assert "bridge=vmbr0" in net0, message(
        en=f"The VM card is not on vmbr0, the lab network: net0={net0}.",
        fr=f"La carte de la VM n'est pas sur vmbr0, le réseau du lab : net0={net0}.",
    )
    # La configuration ne suffit pas : on lit le port EFFECTIF du pont.
    ports = pve.run("bridge link show master vmbr0").stdout
    assert f"tap{VMID}i0" in ports, message(
        en=(
            f"The configuration says vmbr0, but tap{VMID}i0 is not a port of vmbr0. "
            "The change was not applied to the running VM."
        ),
        fr=(
            f"La configuration dit vmbr0, mais tap{VMID}i0 n'est pas un port de vmbr0. "
            "Le changement n'a pas été appliqué à la VM en marche."
        ),
    )


def test_le_client_joint_la_bonne_instance(pve) -> None:
    attendu = _ligne_attendue(pve)
    page = _page(pve)
    assert page, message(
        en=(
            f"Nothing answers on http://{ADRESSE}:{PORT}/ from the node. "
            "Check which bridge the card is on, then whether the guest kept its address."
        ),
        fr=(
            f"Rien ne répond sur http://{ADRESSE}:{PORT}/ depuis le nœud. "
            "Vérifiez sur quel pont est la carte, puis si l'invité a gardé son adresse."
        ),
    )
    assert attendu in page, message(
        en=f"Something answers, but not the lab VM: the expected line is\n  {attendu}",
        fr=f"Quelque chose répond, mais pas la VM du lab : la ligne attendue est\n  {attendu}",
    )


def test_la_panne_est_corrigee_au_bon_etage(pve) -> None:
    net0 = _net0(pve)
    assert "bridge=vmbr0" in net0 and _ligne_attendue(pve) in _page(pve), message(
        en="The VM is not reachable yet on vmbr0: fix the first two tests first.",
        fr="La VM n'est pas encore joignable sur vmbr0 : corrigez d'abord les deux premiers tests.",
    )
    # Le pont isolé est un décor du lab : il doit rester isolé. Lui donner la
    # carte physique « réparerait » en cassant le réseau du nœud.
    ports_isoles = pve.run("bridge link show master vmbr9").stdout.strip()
    physiques = [p for p in re.findall(r"^\d+:\s+(\S+?)[:@]", ports_isoles, re.M) if not p.startswith("tap")]
    assert not physiques, message(
        en=f"vmbr9 received a physical port ({', '.join(physiques)}). The fix belongs to the VM card, not to the isolated bridge.",
        fr=f"vmbr9 a reçu un port physique ({', '.join(physiques)}). La correction porte sur la carte de la VM, pas sur le pont isolé.",
    )


def test_la_correction_survit_au_redemarrage(pve) -> None:
    attendu = _ligne_attendue(pve)
    assert attendu in _page(pve), message(
        en="The service does not answer before the reboot: fix the previous tests first.",
        fr="Le service ne répond pas avant le redémarrage : corrigez d'abord les tests précédents.",
    )
    pve.run(f"qm reboot {VMID} --timeout 120")
    pve.run("mkdir -p /run/network && ifreload -a")
    assert _attendre_page(pve, attendu, 240), message(
        en=(
            "After a guest reboot and a reload of the node network, the service no longer "
            "answers: the fix was not persisted in the VM configuration."
        ),
        fr=(
            "Après un redémarrage de l'invité et un rechargement du réseau du nœud, le service "
            "ne répond plus : la correction n'a pas été enregistrée dans la configuration de la VM."
        ),
    )
