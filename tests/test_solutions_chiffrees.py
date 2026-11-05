"""Les solutions de référence sont chiffrées et leur clé reste hors de Git.

Porté depuis containers-dsoxlab-training le 2026-11-05.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parent.parent
SOLUTIONS = RACINE / "solution"

#: L'en-tête qu'ansible-vault écrit en première ligne d'un fichier chiffré.
ENTETE_VAULT = b"$ANSIBLE_VAULT"

#: Fichiers de service, non chiffrés par nature : ils ne portent aucun contenu
#: de solution. `verified-with.json` est un index de versions d'outils, un
#: éventuel `README.md` explique où regarder.
EXEMPTS = {"verified-with.json", "README.md"}

#: Ce que ce répertoire peut porter sans que ce soit une solution : les caches
#: que Python et les outils y déposent.
PARTS_IGNOREES = {"__pycache__", ".pytest_cache", ".ruff_cache"}


def fichiers_de_solution() -> list[Path]:
    if not SOLUTIONS.is_dir():
        return []
    return sorted(
        f
        for f in SOLUTIONS.rglob("*")
        if f.is_file()
        and f.name not in EXEMPTS
        and not PARTS_IGNOREES.intersection(f.parts)
    )


def test_le_depot_porte_ses_solutions() -> None:
    """Garde-fou : sans lui, un `solution/` disparu rendrait la suite verte.

    Un contrôle qui ne trouve plus rien à contrôler passe, et c'est la forme la
    plus discrète de faux vert.
    """
    assert SOLUTIONS.is_dir(), (
        "Le répertoire solution/ est absent : aucune solution de référence ne "
        "peut être rejouée, et `scripts/valider-labs.py` ne prouverait plus "
        "rien sur le catalogue."
    )
    assert fichiers_de_solution(), (
        "solution/ existe mais ne porte aucun fichier : le balayage mesurerait "
        "le vide."
    )


@pytest.mark.parametrize(
    "fichier",
    fichiers_de_solution(),
    ids=lambda p: str(p.relative_to(SOLUTIONS)),
)
def test_la_solution_est_chiffree(fichier: Path) -> None:
    """Chaque fichier de solution porte l'en-tête d'ansible-vault."""
    debut = fichier.read_bytes()[: len(ENTETE_VAULT)]

    assert debut == ENTETE_VAULT, (
        f"{fichier.relative_to(RACINE)} n'est pas chiffré.\n\n"
        "Chiffrez-le avant de committer :\n"
        "    ansible-vault encrypt --vault-password-file .vault-pass "
        f"{fichier.relative_to(RACINE)}\n\n"
        "Si le fichier est déjà parti en clair dans un commit, le chiffrer "
        "maintenant ne suffit pas : la version lisible reste dans "
        "l'historique, et le mot de passe du vault doit changer."
    )


def test_le_mot_de_passe_du_vault_n_est_pas_suivi() -> None:
    """Un mot de passe commité avec ce qu'il ouvre annule le chiffrement.

    Il voyage avec le dépôt : l'apprenant qui clone reçoit la serrure et la clé
    dans le même paquet.
    """
    issue = subprocess.run(
        ["git", "-C", str(RACINE), "ls-files", "--error-unmatch", ".vault-pass"],
        cwd=RACINE,
        capture_output=True,
        text=True,
        check=False,
    )

    assert issue.returncode != 0, (
        ".vault-pass est suivi par git. Retirez-le de l'index "
        "(`git rm --cached .vault-pass`), puis CHANGEZ le mot de passe et "
        "rechiffrez les solutions : la valeur publiée reste dans l'historique."
    )
