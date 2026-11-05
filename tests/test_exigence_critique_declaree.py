"""Une exigence annoncée comme non compensable est déclarée et nomme un test.

Porté depuis containers-dsoxlab-training le 2026-11-05.
"""

import ast
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
LABS = REPO / "labs"

#: Les tournures par lesquelles un énoncé promet une exigence non compensable.
#:
#: Ce sont des PHRASES et non des mots : chercher « critique » attraperait
#: « une étape critique du démarrage » et ferait de ce test un bruit qu'on
#: apprend à ignorer. Un contrôle qu'on contourne par habitude ne contrôle
#: plus rien.
PROMESSES = (
    "aucun total ne compense",
    "aucun total ne le compense",
    "aucun total ne la compense",
    "ne se compense par aucun total",
    "n'est compensée par aucun total",
    "ne sont compensées par aucun total",
    "compensée par aucune note",
    "no total makes up for",
    "made up for by no total",
    "made up for by no score",
)

#: Les types de lab qui ÉVALUENT quelqu'un. Les autres ne notent personne, donc
#: une exigence non compensable n'y veut rien dire, et dsoxlab refuse d'ailleurs
#: le champ sur eux.
TYPES_QUI_EVALUENT = {"challenge", "capstone"}

#: Les fichiers où une promesse peut être écrite, et qu'un apprenant lit.
DOCUMENTS = (
    "scenario.fr.md",
    "scenario.md",
    "challenge/README.fr.md",
    "challenge/README.md",
    "challenge/tests/test_functional.py",
)


def _labs() -> list[Path]:
    return sorted(p.parent for p in LABS.glob("*/lab.yaml"))


def _promesses(lab: Path) -> list[tuple[str, str]]:
    """Les promesses trouvées, avec le fichier qui les porte."""
    trouvees = []
    for relatif in DOCUMENTS:
        f = lab / relatif
        if not f.is_file():
            continue
        texte = f.read_text(encoding="utf-8", errors="replace").lower()
        for phrase in PROMESSES:
            if phrase.lower() in texte:
                trouvees.append((relatif, phrase))
                break
    return trouvees


@pytest.mark.parametrize("lab", _labs(), ids=lambda p: p.name)
def test_une_promesse_ecrite_a_sa_declaration(lab: Path) -> None:
    """Un énoncé qui promet une exigence critique doit la déclarer."""
    contrat = yaml.safe_load((lab / "lab.yaml").read_text(encoding="utf-8"))
    promesses = _promesses(lab)
    if not promesses:
        return

    declares = contrat.get("exam_blocking_checks") or []
    ou = ", ".join(f"{fichier} (« {phrase} »)" for fichier, phrase in promesses)
    assert declares, (
        f"`{lab.name}` promet une exigence qu'aucun total ne compense, et ne la "
        f"déclare nulle part.\n"
        f"  promesse lue dans : {ou}\n"
        f"  exam_blocking_checks : absent\n\n"
        "Sans déclaration, le moteur ne l'applique pas : quatre contrôles sur "
        "cinq donnent 80, et 80 passe un seuil de 75. L'épreuve serait reçue "
        "alors que son exigence critique a échoué, ce qui est exactement le "
        "défaut que dsoxlab 0.7.0 a corrigé.\n\n"
        "Déclarez le ou les contrôles qui portent l'exigence, ou retirez la "
        "promesse de l'énoncé."
    )


@pytest.mark.parametrize("lab", _labs(), ids=lambda p: p.name)
def test_une_declaration_nomme_des_controles_qui_existent(lab: Path) -> None:
    """Un nom déclaré doit correspondre à un test, sinon il ne bloque rien.

    dsoxlab le vérifie aussi, et c'est voulu : ce test-ci tourne dans la CI du
    catalogue, sur chaque PR, sans machine ni infrastructure, alors que
    `validate-structure` demande que le catalogue soit découvrable. Les deux
    attrapent le même renommage, à deux moments différents.
    """
    contrat = yaml.safe_load((lab / "lab.yaml").read_text(encoding="utf-8"))
    declares = contrat.get("exam_blocking_checks") or []
    if not declares:
        return

    fichier = lab / "challenge/tests/test_functional.py"
    assert fichier.is_file(), (
        f"`{lab.name}` déclare des contrôles bloquants et n'a pas de fichier "
        "de tests."
    )
    definis = {
        n.name
        for n in ast.walk(ast.parse(fichier.read_text(encoding="utf-8")))
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    manquants = [nom for nom in declares if nom not in definis]
    assert not manquants, (
        f"`{lab.name}` déclare des contrôles bloquants qui n'existent pas :\n"
        + "\n".join(f"  {nom}" for nom in manquants)
        + "\n\nUn test renommé désarme son exigence EN SILENCE : l'épreuve "
        "redevient compensable sans que personne ne l'ait décidé."
    )


@pytest.mark.parametrize("lab", _labs(), ids=lambda p: p.name)
def test_seul_un_lab_qui_evalue_declare_une_exigence(lab: Path) -> None:
    """Une exigence non compensable sur un lab qui ne note personne.

    Elle ne veut rien dire, pour la même raison qu'un seuil au même endroit :
    il n'y a pas de total à ne pas compenser.
    """
    contrat = yaml.safe_load((lab / "lab.yaml").read_text(encoding="utf-8"))
    if not (contrat.get("exam_blocking_checks") or []):
        return
    type_lab = contrat.get("lab_type", "lab")
    assert type_lab in TYPES_QUI_EVALUENT, (
        f"`{lab.name}` est un lab `{type_lab}`, qui ne note personne, et il "
        "déclare pourtant une exigence qu'aucun total ne compense.\n"
        f"Seuls {', '.join(sorted(TYPES_QUI_EVALUENT))} évaluent."
    )


def test_le_controle_attrape_une_promesse_orpheline(tmp_path: Path) -> None:
    """LE GARDE-FOU SE VÉRIFIE LUI-MÊME, sur un lab fabriqué pour échouer.

    Un test qui ne rougit pas quand il doit rougir ne mesure rien. Celui-ci
    liste les labs du dépôt, qui sont tous conformes : sans ce cas-ci, il
    passerait au vert même si sa recherche de phrases ne trouvait plus rien.
    """
    faux = tmp_path / "epreuve-fabriquee"
    (faux / "challenge/tests").mkdir(parents=True)
    (faux / "lab.yaml").write_text(
        yaml.safe_dump({
            "id": "epreuve-fabriquee", "title": "X", "level": "c1",
            "lab_type": "challenge", "exam_passing_score": 75,
        }), encoding="utf-8")
    (faux / "scenario.fr.md").write_text(
        "Une exigence n'est compensée par aucun total : perdre la donnée fait "
        "échouer l'épreuve.\n", encoding="utf-8")

    assert _promesses(faux), "la promesse n'est pas reconnue"
    contrat = yaml.safe_load((faux / "lab.yaml").read_text(encoding="utf-8"))
    assert not (contrat.get("exam_blocking_checks") or []), (
        "le lab fabriqué ne doit rien déclarer"
    )
