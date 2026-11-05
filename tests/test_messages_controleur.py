"""Exécuter les assertions des neuf labs sans solliciter Proxmox."""

import runpy
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

LABS = Path(__file__).resolve().parents[1] / "labs"
LABS_CONTROLEUR = (
    "pve-epreuve-disponibilite", "pve-eprouver-cluster", "pve-eprouver-ha",
    "pve-maintenir-cluster", "pve-mesurer-replication", "pve-migrer-instance",
    "pve-qualifier-stockage-partage", "pve-reprendre-hors-site", "pve-reserver-capacite",
)


@pytest.mark.parametrize("lab", LABS_CONTROLEUR)
@pytest.mark.parametrize("langue", ["en", "fr"])
def test_message_et_verdict_du_controleur(monkeypatch, lab, langue):
    monkeypatch.setenv("DSOXLAB_LANG", langue)
    module = runpy.run_path(str(LABS / lab / "challenge/tests/test_functional.py"))
    criterion = module["CRITERIA"][0]
    resultat = SimpleNamespace(returncode=0, stdout="observed state", stderr="probe failure")
    appels = []

    def lancer(args, **kwargs):
        appels.append(args)
        return resultat

    monkeypatch.setattr(subprocess, "run", lancer)
    module["test_catalog_criterion"](criterion)
    # Dégrader seulement le verdict, et constater la dégradation avant l'appel.
    resultat.returncode = 1
    assert resultat.returncode == 1, "Le contrôleur simulé doit refuser avant la mesure."
    for _ in range(2):
        with pytest.raises(AssertionError) as erreur:
            module["test_catalog_criterion"](criterion)
        texte = str(erreur.value)
        assert criterion in texte, "Le message doit nommer le critère attendu."
        assert "observed stateprobe failure" in texte, "Le diagnostic technique doit être conservé."
        attendu = "Satisfaites le critère" if langue == "fr" else "Complete criterion"
        assert attendu in texte, "La consigne doit suivre DSOXLAB_LANG."
    assert all(args[-2:] == ["--criterion", criterion] for args in appels), (
        "Le contrôle doit transmettre le critère au contrôleur."
    )
