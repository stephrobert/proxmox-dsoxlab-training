"""Note le rétablissement de l'agent invité de la VM 180.

Contrat du TP `pve-reparer-agent` (src/data/parcours/proxmox.yaml du site) :
le canal et le service de l'agent répondent, l'adresse qu'il remonte est celle
du réseau attendu, et la correction respecte l'intégrité de la charge, sans
arrêt forcé. Le nœud joue le client.

L'arrêt se juge sur le JOURNAL DES TÂCHES de Proxmox, qui garde une trace de
chaque opération : un `qm stop` (tâche `qmstop`) coupe la VM comme on
débranche une prise, alors qu'un `qm shutdown` ou un `qm reboot` laissent
l'invité s'arrêter proprement. Activer le périphérique de l'agent demande de
redémarrer la VM, et c'est précisément le moment où l'on est tenté de forcer.
"""

from __future__ import annotations

import json

import pytest

from conftest import lab_host, lab_target_host, message

CIBLE = lab_target_host("pve.lab")
VMID = 180
ADRESSE = "10.10.113.180"
LAB = "/opt/lab-proxmox/pve-reparer-agent"


@pytest.fixture(scope="module")
def pve():
    return lab_host(CIBLE)


def _agent_repond(hote) -> bool:
    return hote.run(f"qm agent {VMID} ping").rc == 0


def _exiger_agent(hote) -> None:
    assert _agent_repond(hote), message(
        en="The agent still does not answer: fix the first test first.",
        fr="L'agent ne répond toujours pas : corrigez d'abord le premier test.",
    )


def test_le_canal_et_le_service_de_l_agent_repondent(pve) -> None:
    config = pve.run(f"qm config {VMID}").stdout
    active = any(
        ligne.startswith("agent:") and ("enabled=1" in ligne or ligne.split(":", 1)[1].strip().startswith("1"))
        for ligne in config.splitlines()
    )
    assert active, message(
        en="The agent device is not enabled in the VM configuration (Options, QEMU Guest Agent).",
        fr="Le périphérique de l'agent n'est pas activé dans la configuration de la VM (Options, QEMU Guest Agent).",
    )
    assert _agent_repond(pve), message(
        en=(
            "The device is enabled, but the agent does not answer. Check in the guest that the "
            "qemu-guest-agent package is installed and its service running, and that the VM was "
            "restarted since the device was enabled."
        ),
        fr=(
            "Le périphérique est activé, mais l'agent ne répond pas. Vérifiez dans l'invité que le "
            "paquet qemu-guest-agent est installé et son service en marche, et que la VM a été "
            "redémarrée depuis l'activation du périphérique."
        ),
    )
    canal = pve.run(
        f"qm guest exec {VMID} -- test -e /dev/virtio-ports/org.qemu.guest_agent.0"
    ).stdout
    assert '"exitcode" : 0' in canal or '"exitcode": 0' in canal, message(
        en="Inside the guest, the agent channel /dev/virtio-ports/org.qemu.guest_agent.0 is missing.",
        fr="Dans l'invité, le canal de l'agent /dev/virtio-ports/org.qemu.guest_agent.0 est absent.",
    )


def test_l_adresse_remontee_est_celle_du_reseau_du_lab(pve) -> None:
    _exiger_agent(pve)
    sortie = pve.run(f"qm agent {VMID} network-get-interfaces").stdout
    adresses = []
    for interface in json.loads(sortie or "[]"):
        if interface.get("name") == "lo":
            continue
        adresses += [a.get("ip-address") for a in interface.get("ip-addresses", [])]
    assert ADRESSE in adresses, message(
        en=f"The agent reports {', '.join(filter(None, adresses)) or 'no address'}, not {ADRESSE}.",
        fr=f"L'agent remonte {', '.join(filter(None, adresses)) or 'aucune adresse'}, pas {ADRESSE}.",
    )


def test_la_correction_respecte_l_integrite_de_la_charge(pve) -> None:
    _exiger_agent(pve)
    debut = pve.file(f"{LAB}/debut").content_string.strip()
    noeud = pve.run("hostname --short").stdout.strip()
    taches = json.loads(
        pve.run(
            f"pvesh get /nodes/{noeud}/tasks --vmid {VMID} --typefilter qmstop "
            f"--since {debut} --output-format json"
        ).stdout
        or "[]"
    )
    assert not taches, message(
        en=(
            f"VM {VMID} was force-stopped ({len(taches)} qmstop task(s)) since the lab started. "
            "Stop it cleanly with qm shutdown or qm reboot: its workload must close properly."
        ),
        fr=(
            f"La VM {VMID} a été arrêtée de force ({len(taches)} tâche(s) qmstop) depuis le début du lab. "
            "Arrêtez-la proprement avec qm shutdown ou qm reboot : sa charge doit se fermer correctement."
        ),
    )
    nonce = pve.file(f"{LAB}/nonce").content_string.strip()
    page = pve.run(f"curl -s --max-time 5 http://{ADRESSE}:8080/").stdout
    assert nonce in page, message(
        en="The witness service no longer answers with the session data: the workload was not preserved.",
        fr="Le service témoin ne répond plus avec les données de la session : la charge n'a pas été préservée.",
    )
