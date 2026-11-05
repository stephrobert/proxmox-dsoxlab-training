"""Les messages destinés à l'apprenant passent par le helper bilingue.

Le diagnostic technique reste en anglais. Ce contrôle vérifie les appels,
pas la qualité des traductions, qui demande une relecture.
"""

import ast
from pathlib import Path

import pytest

LABS = Path(__file__).resolve().parents[1] / "labs"
FICHIERS = sorted(LABS.glob("*/challenge/tests/*.py"))


def _est_bilingue(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    fonction = node.func
    nom = fonction.id if isinstance(fonction, ast.Name) else getattr(fonction, "attr", None)
    langues = {kw.arg: kw.value for kw in node.keywords}
    return nom == "message" and all(
        langue in langues
        and not (
            isinstance(langues[langue], ast.Constant)
            and not langues[langue].value
        )
        for langue in ("en", "fr")
    )


def _porteurs_monolingues(source: str) -> list[int]:
    fautifs = []
    for node in ast.walk(ast.parse(source)):
        texte = None
        if isinstance(node, ast.Assert):
            texte = node.msg
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "pytest"
            and node.func.attr in {"fail", "skip"}
        ):
            texte = node.args[0] if node.args else next(
                (kw.value for kw in node.keywords if kw.arg == "reason"), None
            )
        if texte is not None and not _est_bilingue(texte):
            fautifs.append(node.lineno)
    return sorted(fautifs)


def test_le_perimetre_contient_tous_les_labs():
    labs = {path.parent for path in LABS.glob("*/lab.yaml")}
    couverts = {path.parents[2] for path in FICHIERS}
    assert labs, "Aucun lab découvert : le contrôle ne mesure rien."
    assert labs == couverts, "Chaque lab doit fournir des tests à mesurer."
    assert any(
        isinstance(node, ast.Assert)
        for path in FICHIERS
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
    ), "Aucune assertion découverte : le contrôle ne mesure rien."


@pytest.mark.parametrize("fichier", FICHIERS, ids=lambda p: p.parents[2].name)
def test_chaque_message_est_bilingue(fichier):
    fautifs = _porteurs_monolingues(fichier.read_text(encoding="utf-8"))
    assert not fautifs, (
        f"{fichier}: messages monolingues aux lignes {fautifs}. "
        "Utilisez message(en=..., fr=...) avec les deux traductions."
    )


@pytest.mark.parametrize("source", [
    'assert ok, "Create the service"',
    'assert ok, message(en="Create it")',
    'assert ok, message(en="Create it", fr="")',
    'pytest.fail("Create it")',
    'pytest.skip(reason="Unavailable")',
])
def test_le_garde_fou_refuse_un_message_incomplet(source):
    assert _porteurs_monolingues(source) == [1], "Le témoin monolingue doit être refusé."


@pytest.mark.parametrize("source", [
    'assert ok, message(en="Create it", fr="Créez-le")',
    'pytest.fail(conftest.message(en="Create it", fr="Créez-le"))',
    'pytest.skip(reason=message(en="Unavailable", fr="Indisponible"))',
    'assert ok',
    'client.fail("Technical log")',
])
def test_le_garde_fou_accepte_son_temoin_conforme(source):
    assert not _porteurs_monolingues(source), "Le témoin conforme doit être accepté."
