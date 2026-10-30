"""Note la lecture des tâches de Proxmox et le nettoyage qui la suit.

Contrat du TP `pve-suivre-tache` (src/data/parcours/proxmox.yaml du site) :
chaque résultat est rattaché à la BONNE tâche, une tâche terminée en erreur est
reconnue avec sa cause, la vérification porte sur l'état COURANT et non sur un
vieux journal, et les objets temporaires sont retirés sans toucher au témoin.

Les tests confrontent le rapport de l'apprenant, /root/rapport-taches.txt, au
registre des UPID réels que le setup a gardé, puis à l'état du nœud.
"""

from __future__ import annotations

import json
import re

import pytest

from conftest import lab_host, lab_target_host, message

CIBLE = lab_target_host("pve.lab")
RAPPORT = "/root/rapport-taches.txt"
REGISTRE = "/var/lib/lab-proxmox/pve-suivre-tache/registre.json"


@pytest.fixture(scope="module")
def pve():
    return lab_host(CIBLE)


def _registre(hote) -> dict[str, str]:
    return json.loads(hote.file(REGISTRE).content_string)


def _rapport(hote) -> dict[str, str]:
    fichier = hote.file(RAPPORT)
    assert fichier.exists, message(
        en=f"The report {RAPPORT} does not exist. Write it on the model given in the lab instructions.",
        fr=f"Le rapport {RAPPORT} n'existe pas. Rédigez-le sur le modèle donné par la consigne du lab.",
    )
    lignes = {}
    for ligne in fichier.content_string.splitlines():
        cle, sep, valeur = ligne.partition(":")
        if sep and cle.strip():
            lignes[cle.strip()] = valeur.strip()
    return lignes


def _statut_final(hote, upid: str) -> str:
    noeud = upid.split(":")[1]
    sortie = hote.run(f"pvesh get /nodes/{noeud}/tasks/{upid}/status --output-format json").stdout
    return json.loads(sortie).get("exitstatus", "")


def _normaliser(texte: str) -> str:
    return re.sub(r"\s+", " ", texte).strip().lower()


def test_chaque_resultat_est_rattache_a_la_bonne_tache(pve) -> None:
    rapport = _rapport(pve)
    registre = _registre(pve)
    ecarts = []
    for cle in ("demarrage-191", "demarrage-192"):
        upid_rapporte = rapport.get(cle, "").split(" ")[0]
        if upid_rapporte != registre[cle]:
            ecarts.append(f"{cle} : {upid_rapporte or 'absent'}")
    assert not ecarts, message(
        en=(
            "These lines do not carry the UPID of the right start task:\n  " + "\n  ".join(ecarts)
            + "\nAn UPID names the node, the task type and the VMID: check all three."
        ),
        fr=(
            "Ces lignes ne portent pas l'UPID de la bonne tâche de démarrage :\n  " + "\n  ".join(ecarts)
            + "\nUn UPID nomme le nœud, le type de tâche et le VMID : vérifiez les trois."
        ),
    )


def test_la_tache_en_erreur_est_reconnue_avec_sa_cause(pve) -> None:
    rapport = _rapport(pve)
    registre = _registre(pve)
    if _statut_final(pve, registre["demarrage-191"]) == "OK":
        assert rapport.get("demarrage-191", "").split(" ", 1)[-1].strip().upper() == "OK", message(
            en="The start of VM 191 succeeded: its result is OK.",
            fr="Le démarrage de la VM 191 a réussi : son résultat est OK.",
        )
    reel = _statut_final(pve, registre["demarrage-192"])
    rapporte = rapport.get("demarrage-192", "").split(" ", 1)[1] if " " in rapport.get("demarrage-192", "") else ""
    assert rapporte and rapporte.strip().upper() != "OK", message(
        en="The start of VM 192 was accepted by the API, then FAILED: its result is not OK.",
        fr="Le démarrage de la VM 192 a été accepté par l'API, puis a ÉCHOUÉ : son résultat n'est pas OK.",
    )
    a, b = _normaliser(rapporte), _normaliser(reel)
    assert a and (a in b or b in a), message(
        en=f"The reported cause does not match the task's final message:\n  reported: {rapporte}\n  Proxmox: {reel}",
        fr=f"La cause rapportée ne correspond pas au message final de la tâche :\n  rapporté : {rapporte}\n  Proxmox : {reel}",
    )


def test_l_etat_rapporte_est_l_etat_courant(pve) -> None:
    rapport = _rapport(pve)
    etat = pve.run("qm status 190").stdout.replace("status:", "").strip()
    assert rapport.get("etat-190", "").lower() == etat, message(
        en=(
            f"The current state of VM 190 is '{etat}', the report says '{rapport.get('etat-190', 'nothing')}'. "
            "Its start task did succeed, but that was before: a log is history, not state."
        ),
        fr=(
            f"L'état actuel de la VM 190 est « {etat} », le rapport dit « {rapport.get('etat-190', 'rien')} ». "
            "Sa tâche de démarrage a bien réussi, mais c'était avant : un journal est un historique, pas un état."
        ),
    )


def test_les_temporaires_sont_retires_sans_toucher_au_temoin(pve) -> None:
    restantes = [v for v in (191, 192) if pve.run(f"qm status {v}").rc == 0]
    assert not restantes, message(
        en=f"These temporary VMs still exist: {', '.join(map(str, restantes))}.",
        fr=f"Ces VM temporaires existent encore : {', '.join(map(str, restantes))}.",
    )
    sentinelle = pve.file("/etc/pve/qemu-server/190.conf")
    assert sentinelle.exists, message(
        en="The sentinel VM 190 was deleted: it had to stay.",
        fr="La VM sentinelle 190 a été supprimée : elle devait rester.",
    )
    sha = pve.run("sha256sum /etc/pve/qemu-server/190.conf").stdout.split()[0]
    assert sha == _registre(pve)["conf-190"], message(
        en="The configuration of the sentinel VM 190 was modified: it had to stay untouched.",
        fr="La configuration de la VM sentinelle 190 a été modifiée : elle devait rester intacte.",
    )
