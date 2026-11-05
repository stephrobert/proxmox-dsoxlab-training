"""Les indices sont rédigés, bilingues et gradués sur quatre paliers.

Porté depuis containers-dsoxlab-training le 2026-11-05.
"""

import base64
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
LABS = REPO / "labs"

# Formules que le générateur laisse derrière lui, dans les deux langues.
#
# Ce sont les PHRASES du gabarit, pas des fragments. La première version
# cherchait « à écrire » et « to write », et cela a coûté un faux positif
# mesuré le 2026-09-25 : l'indice anglais de `environments/when-to-use-workspaces`
# dit « the block **to write** is a data "terraform_remote_state" », une tournure
# parfaitement légitime dans un indice rédigé. Le lab était retenu dans la dette
# alors que ses trois indices étaient écrits, et rien ne pouvait l'en sortir.
#
# Un détecteur trop large ne se contente pas de crier à tort : il rend la liste
# de dette fausse, donc inutilisable.
MARQUEURS = (
    "Nudge à écrire",
    "Méthode à écrire",
    "Quasi-solution à écrire",
    "Nudge to write",
    "Method to write",
    "Near-solution to write",
    "A_COMPLETER",
)

# Les six labs complets de Proxmox utilisent ces quatre paliers, mesurés le
# 2026-11-05. Les montants de Containers ne sont pas le contrat de Proxmox.
COUTS_ATTENDUS = [5, 10, 15, 20]

# Labs dont les indices sont encore ceux du générateur, mesurés le 2026-09-18.
# Un lab repris se retire d'ici, et le test le vérifie.
DETTE: set[str] = set()


def labs_avec_indices() -> list[str]:
    return sorted(
        str(f.parent.parent.relative_to(LABS))
        for f in LABS.rglob("challenge/hints.yaml")
    )


def indices_en_clair(rel: str) -> list[dict]:
    """Les indices d'un lab, décodés. La liste peut être vide."""
    fichier = LABS / rel / "challenge" / "hints.yaml"
    contenu = yaml.safe_load(fichier.read_text(encoding="utf-8")) or {}
    clairs = []
    for h in contenu.get("hints") or []:
        clairs.append(
            {
                "cost": h.get("cost"),
                "fr": base64.b64decode(h.get("text_fr", ""), validate=True).decode("utf-8"),
                "en": base64.b64decode(h.get("text_en", ""), validate=True).decode("utf-8"),
            }
        )
    return clairs


def porte_le_gabarit(clairs: list[dict]) -> bool:
    return any(m in i[langue] for i in clairs for langue in ("fr", "en") for m in MARQUEURS)


@pytest.mark.parametrize("rel", labs_avec_indices())
def test_les_indices_ne_sont_pas_ceux_du_generateur(rel: str) -> None:
    clairs = indices_en_clair(rel)
    assert clairs, f"{rel} : hints.yaml ne porte aucun indice."

    if porte_le_gabarit(clairs):
        assert rel in DETTE, (
            f"{rel} : les indices sont encore ceux du générateur.\n"
            f"Premier indice décodé : {clairs[0]['fr']!r}\n\n"
            "Quatre indices bilingues de coût croissant, du plus vague au plus "
            "explicite, sans jamais donner le bloc complet. Ils sont en base64 "
            "pour qu'un apprenant n'y accède pas en ouvrant le fichier."
        )
        return

    assert rel not in DETTE, (
        f"{rel} : les indices ont été écrits, mais le lab figure encore dans "
        "DETTE. Retirez-le de la liste, sinon elle ne décroît jamais et plus "
        "personne ne la regarde."
    )


@pytest.mark.parametrize("rel", sorted(set(labs_avec_indices()) - DETTE))
def test_quatre_indices_de_cout_croissant(rel: str) -> None:
    """Quatre paliers, et non trois comme chez les catalogues frères.

    Le quatrième a ici un emploi précis : nommer l'outil qui montre la faute
    quand tout semble juste sans l'être. `hadolint` sur un Dockerfile qui
    construit, `dive` sur une image dont la taille surprend, `docker inspect`
    sur un conteneur qui répond mais tourne en root.
    """
    couts = [i["cost"] for i in indices_en_clair(rel)]
    assert couts == COUTS_ATTENDUS, (
        f"{rel} : les coûts des indices valent {couts}, attendu "
        f"{COUTS_ATTENDUS}. Quatre paliers du plus vague au plus explicite."
    )


@pytest.mark.parametrize("rel", sorted(set(labs_avec_indices()) - DETTE))
def test_les_deux_langues_sont_renseignees(rel: str) -> None:
    """`text_fr` recopié de l'anglais signale une traduction jamais faite.

    L'égalité n'est pas fautive indice par indice : le dernier palier est
    parfois un extrait de Dockerfile, identique dans les deux langues par nature. Ce
    qui est fautif, c'est que le lab ENTIER soit identique en français et en
    anglais, car alors personne n'a traduit.
    """
    clairs = indices_en_clair(rel)
    for rang, indice in enumerate(clairs, start=1):
        assert indice["fr"].strip(), f"{rel} : indice {rang} sans texte français."
        assert indice["en"].strip(), f"{rel} : indice {rang} sans texte anglais."

    assert any(i["fr"] != i["en"] for i in clairs), (
        f"{rel} : tous les indices portent le même texte en français et en "
        "anglais. `text_fr` est une copie de l'anglais tant que personne n'est "
        "passé."
    )


def test_la_dette_ne_designe_que_des_labs_existants() -> None:
    """Un lab renommé ou supprimé ne doit pas laisser une entrée fantôme."""
    fantomes = DETTE - set(labs_avec_indices())
    assert not fantomes, (
        f"DETTE désigne des labs qui n'existent pas : {sorted(fantomes)}."
    )


def test_tous_les_labs_fournissent_des_indices():
    labs = {str(p.parent.relative_to(LABS)) for p in LABS.rglob("lab.yaml")}
    assert labs, "Aucun lab découvert : le contrôle ne mesure rien."
    assert set(labs_avec_indices()) == labs, "Chaque lab doit fournir son hints.yaml."
