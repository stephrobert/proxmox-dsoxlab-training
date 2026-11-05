"""Un lab écrit porte une solution ; un squelette refuse au lieu de disparaître.

Classification portée depuis containers-dsoxlab-training le 2026-11-05.
"""

from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parent.parent
LABS = RACINE / "labs"
SOLUTIONS = RACINE / "solution"

#: Ce que `dsoxlab new lab` laisse dans la suite d'un lab non écrit.
MARQUEUR_SQUELETTE = "def test_a_ecrire"

#: Ce qu'un squelette doit faire : refuser. Le vérifier est le coeur de ce
#: module, parce que remplacer ce `raise` par un skip rendrait les 42
#: squelettes verts d'un coup, sans qu'aucun autre contrôle ne bouge.
MARQUEUR_DE_REFUS = "raise AssertionError"


def tous_les_labs() -> list[str]:
    return sorted(str(c.parent.relative_to(LABS)) for c in LABS.rglob("lab.yaml"))


def suite_du_lab(rel: str) -> Path:
    return LABS / rel / "challenge" / "tests" / "test_functional.py"


def est_un_squelette(rel: str) -> bool:
    suite = suite_du_lab(rel)
    if not suite.is_file():
        return True
    return MARQUEUR_SQUELETTE in suite.read_text(encoding="utf-8")


def a_une_solution(rel: str) -> bool:
    dossier = SOLUTIONS / rel
    return dossier.is_dir() and any(f.is_file() for f in dossier.rglob("*"))


TOUS = tous_les_labs()
SQUELETTES = [rel for rel in TOUS if est_un_squelette(rel)]
ECRITS = [rel for rel in TOUS if not est_un_squelette(rel)]


def test_le_catalogue_se_lit_dans_les_deux_etats() -> None:
    """Garde-fou : un marqueur qui dériverait classerait tout du même côté.

    Si `dsoxlab new lab` change sa tournure, tous les labs passent pour écrits
    et les contrôles ci-dessous ne jugent plus rien, en silence.
    """
    assert TOUS, "aucun lab.yaml trouvé : le glob est cassé."
    assert ECRITS, (
        f"Aucun lab écrit : `{MARQUEUR_SQUELETTE}` n'est probablement plus le "
        "marqueur que pose le générateur."
    )
    if not SQUELETTES:
        # SANS SQUELETTE, CE GARDE-FOU NE MESURE PLUS RIEN, et il ne prouve pas
        # pour autant que le marqueur a dérivé : les deux situations se
        # ressemblent et n'appellent pas le même geste. Il saute donc, au lieu
        # de refuser une livraison saine ou de conclure au vert sans avoir
        # regardé.
        #
        # Rencontré en livrant sur `main` : la branche de travail porte 39
        # squelettes, et la livraison n'emporte que les labs attestés. Le
        # contrôle y accusait un catalogue dont tous les labs sont écrits.
        pytest.skip(
            "aucun squelette dans ce catalogue : la dérive du marqueur ne peut "
            "pas être mesurée ici. C'est le cas d'une livraison qui n'emporte "
            "que des labs attestés, et ce n'est pas un défaut."
        )


@pytest.mark.parametrize("rel", SQUELETTES)
def test_un_squelette_refuse_au_lieu_de_skipper(rel: str) -> None:
    """Un lab non écrit doit être ROUGE, pas vert et muet.

    C'est le point de tout ce module : pytest compte un skip comme un succès,
    et un catalogue de squelettes skippés annonce alors que tout passe.
    """
    texte = suite_du_lab(rel).read_text(encoding="utf-8")

    assert MARQUEUR_DE_REFUS in texte, (
        f"{rel} est un squelette dont la suite ne lève pas : elle ne porte pas "
        f"`{MARQUEUR_DE_REFUS}`.\n\nUn squelette qui skippe fait passer "
        "`dsoxlab check` et le rejeu du catalogue au vert sans rien prouver. "
        "Tant que les tests ne sont pas écrits, la suite doit refuser."
    )
    assert "pytestmark" not in texte, (
        f"{rel} porte un `pytestmark` : s'il désactive la suite, le lab devient "
        "vert sans mesurer quoi que ce soit. Aucune suite du catalogue n'en "
        "emploie, et c'est ce qui rend le rejeu lisible."
    )


@pytest.mark.parametrize("rel", ECRITS)
def test_un_lab_ecrit_porte_une_solution_de_reference(rel: str) -> None:
    """Un test sans solution ne peut pas être validé.

    C'est l'implication que le catalogue doit tenir :

        lab publié  =>  solution existe  =>  solution rejouable

    Sans solution, `scripts/valider-labs.py` ne peut rien rejouer, et le lab n'a
    jamais été éprouvé dans le sens « 100 ».
    """
    assert a_une_solution(rel), (
        f"{rel} a des tests fonctionnels écrits, mais AUCUNE solution sous "
        f"solution/{rel}/.\n\nRien ne prouve alors que ses tests sont "
        "satisfaisables : ils peuvent exiger l'impossible, et seul un apprenant "
        "s'en apercevrait."
    )


@pytest.mark.parametrize("rel", SQUELETTES)
def test_un_squelette_ne_porte_pas_de_solution(rel: str) -> None:
    """L'autre moitié de l'implication, et elle attrape une incohérence réelle.

    Une solution écrite pour des tests qui n'existent pas n'a jamais été jouée
    par quoi que ce soit : le cycle de validation a besoin des deux. Si la
    solution est juste, ce sont les tests qui manquent ; si les tests ont été
    effacés, c'est une régression qu'il faut voir.
    """
    assert not a_une_solution(rel), (
        f"{rel} porte une solution sous solution/{rel}/, mais sa suite est "
        "encore le squelette du générateur.\n\nRien n'a donc jamais joué cette "
        "solution : le cycle « 0 avant, 100 après » a besoin de tests écrits. "
        "Soit les tests restent à écrire et la solution est prématurée, soit "
        "ils ont disparu."
    )
