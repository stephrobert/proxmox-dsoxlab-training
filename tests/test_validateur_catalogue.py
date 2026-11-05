"""Éprouver le validateur Proxmox sans machines ni campagne réelle.

Équivalent des tests de harnais contenus dans test_maturite_des_labs de
Containers. Les photographies Docker distantes ne sont pas une mesure PVE.
"""

import runpy
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def validateur(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    return runpy.run_path(str(ROOT / "scripts/valider-labs.py"))


@pytest.mark.parametrize("avant,apres,attendu", [(0, 4, "VALIDE"), (1, 4, "ROUGE"), (0, 3, "ROUGE")])
def test_le_cycle_distingue_depart_solution_et_travail_incomplet(validateur, monkeypatch, avant, apres, attendu):
    fonction = validateur["valider"]
    globals_ = fonction.__globals__
    scores = iter([avant, apres])
    appels = []

    def commande(*args, **kwargs):
        appels.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    def mesure(_):
        passed = next(scores)
        return {"status": "passed" if passed == 4 else "failed", "score": passed * 25,
                "passed": passed, "total": 4, "echecs": []}

    monkeypatch.setitem(globals_, "_dsoxlab", commande)
    monkeypatch.setitem(globals_, "_conteneurs", set)
    monkeypatch.setitem(globals_, "snapshot_reset", lambda _: None)
    monkeypatch.setitem(globals_, "hotes_du_lab", lambda _: ["pve.lab"])
    monkeypatch.setitem(globals_, "_poser_la_solution", lambda _: None)
    monkeypatch.setitem(globals_, "_check", mesure)
    verdict = fonction("pve-creer-vm", ROOT / "labs/pve-creer-vm")
    assert verdict.verdict == attendu, "Le cycle doit refuser un départ vert ou une solution incomplète."
    assert appels[-1] == ("clean", "pve-creer-vm"), "Le cycle doit nettoyer même après refus."


def test_une_isolation_impossible_ne_lance_pas_le_lab(validateur, monkeypatch):
    fonction = validateur["valider"]
    globals_ = fonction.__globals__
    appels = []

    def refuser(_):
        raise validateur["IsolationEteinte"]("base absente")

    monkeypatch.setitem(globals_, "_conteneurs", set)
    monkeypatch.setitem(globals_, "hotes_du_lab", lambda _: ["pve.lab"])
    monkeypatch.setitem(globals_, "snapshot_reset", refuser)
    monkeypatch.setitem(globals_, "_dsoxlab", lambda *args, **kw: appels.append(args))
    verdict = fonction("pve-creer-vm", ROOT / "labs/pve-creer-vm")
    assert verdict.verdict == "ROUGE", "Une isolation impossible interdit toute conclusion au vert."
    assert "base absente" in verdict.pourquoi, "La panne du banc doit être nommée."
    assert all(args[0] == "clean" for args in appels), "Aucun run ne doit suivre l'échec d'isolation."


@pytest.mark.parametrize("action,confirmation", [("clean", True), ("run", False), ("check", False)])
def test_la_confirmation_du_nettoyage_est_explicite(validateur, monkeypatch, action, confirmation):
    appels = []

    def lancer(args, **kwargs):
        appels.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(validateur["subprocess"], "run", lancer)
    validateur["_dsoxlab"](action, "pve-creer-vm")
    assert ("--yes" in appels[0]) is confirmation, "Le nettoyage non interactif doit porter --yes."
