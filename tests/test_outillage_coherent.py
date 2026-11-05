"""Chaque hook vise un fichier présent et chaque test est réellement câblé.

Adapté de Containers : un appel à pytest tests/ couvre aussi ses modules,
et un hook qui cite plusieurs fichiers doit tous les trouver.
"""

import shlex
from pathlib import Path

import pytest
import yaml

RACINE = Path(__file__).resolve().parents[1]


def hooks_locaux():
    config = yaml.safe_load((RACINE / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    return [h for repo in config["repos"] if repo["repo"] == "local" for h in repo["hooks"]]


def cibles_pytest(entry):
    args = shlex.split(entry)
    if "pytest" not in args:
        return []
    # --with pytest est une dépendance de uv, pas la commande à exécuter.
    position = max(i for i, arg in enumerate(args) if arg == "pytest")
    return [arg for arg in args[position + 1:] if arg.startswith("tests/")]


def couvre(entry, relatif):
    return any(
        relatif == cible or relatif.startswith(cible.rstrip("/") + "/")
        for cible in cibles_pytest(entry)
    )


def test_le_perimetre_existe():
    assert hooks_locaux(), "Aucun hook local découvert."
    assert list((RACINE / "tests").glob("test_*.py")), "Aucun test découvert."


@pytest.mark.parametrize("hook", hooks_locaux(), ids=lambda h: h["id"])
def test_les_cibles_du_hook_existent(hook):
    for cible in cibles_pytest(hook["entry"]):
        assert (RACINE / cible).exists(), f"{hook['id']} vise un test absent : {cible}"
    for arg in shlex.split(hook["entry"]):
        if arg.startswith(("scripts/", "tests/outils/")):
            assert (RACINE / arg).is_file(), f"{hook['id']} vise un script absent : {arg}"


@pytest.mark.parametrize("test", sorted((RACINE / "tests").glob("test_*.py")), ids=lambda p: p.name)
def test_chaque_module_est_cable(test):
    relatif = test.relative_to(RACINE).as_posix()
    assert any(couvre(h["entry"], relatif) for h in hooks_locaux()), f"{relatif} n'est pas câblé."


def test_contrat_et_catalogue_sont_verifies():
    entries = [h["entry"] for h in hooks_locaux()]
    assert any("validate-structure" in e for e in entries), "Le contrat n'est pas vérifié."
    assert any("gen_catalog.py --check" in e for e in entries), "Le catalogue n'est pas vérifié."


@pytest.mark.parametrize("entry,relatif,attendu", [
    ("uv run --with pytest pytest tests/ -q", "tests/test_a.py", True),
    ("pytest tests/test_a.py tests/test_b.py -q", "tests/test_b.py", True),
    ("pytest tests/test_a.py", "tests/test_b.py", False),
    ("echo pytest", "tests/test_a.py", False),
])
def test_le_detecteur_de_cablage_sait_refuser(entry, relatif, attendu):
    assert couvre(entry, relatif) is attendu, "Le détecteur confond présence et couverture."
