"""Les énoncés désignent des hôtes déclarés et des chemins existants.

Porté depuis containers-dsoxlab-training le 2026-11-05.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parent.parent
LABS = RACINE / "labs"
META = RACINE / "meta.yml"

sys.path.insert(0, str(RACINE / "scripts"))
from lecture_yaml import lire_yaml  # noqa: E402

#: Un nom d'hôte du lab, cité entre accents graves. Le suffixe `.lab` est la
#: convention de tous les catalogues `vm` de la collection.
#:
#: La négation en tête écarte le seul homonyme du catalogue : `dsoxlab.lab` est
#: le nom du **label** que chaque lab pose sur ses objets Docker, et un énoncé a
#: de bonnes raisons de le citer. Sans elle, le contrôle refusait un texte juste
#: en annonçant un hôte manquant, ce qui envoie corriger le meta.yml pour rien.
#: L'exclusion ne masque aucun hôte réel : aucune machine ne porte ce nom, et le
#: label le porte dans les vingt-trois catalogues.
HOTE_CITE = re.compile(r"`(?!dsoxlab\.lab`)([A-Za-z0-9][A-Za-z0-9_.-]*\.lab)`")

#: Un chemin du répertoire de travail, cité entre accents graves. Le reste du
#: texte parle de commandes et de concepts, pas d'emplacements.
CHEMIN_CITE = re.compile(r"`(challenge/[A-Za-z0-9_./-]+)`")

#: Les textes que l'apprenant lit avant de travailler, dans les deux langues.
TEXTES = (
    "README.md",
    "README.fr.md",
    "scenario.md",
    "scenario.fr.md",
    "challenge/README.md",
    "challenge/README.fr.md",
)

# Un corpus sans aucune citation ne mesure rien. Le seuil de vingt labs de
# Containers ne décrit pas Proxmox ; les extracteurs sont éprouvés plus bas.
LABS_CITANTS_MINIMUM = 1


def tous_les_labs() -> list[str]:
    return sorted(str(c.parent.relative_to(LABS)) for c in LABS.rglob("lab.yaml"))


def hotes_declares() -> set[str]:
    infra = lire_yaml(META).get("infra") or {}
    return {h["name"] for h in (infra.get("hosts") or []) if h.get("name")}


def workdir_declare(rel: str) -> str:
    runtime = lire_yaml(LABS / rel / "lab.yaml").get("runtime") or {}
    if runtime.get("workdir"):
        return runtime["workdir"].rstrip("/")
    # Les labs N3 utilisent un contrôleur LOCAL, même en runtime VM. Son
    # répertoire de travail se lit dans le code qui le consomme, pas dans
    # runtime.workdir. Les wrappers délèguent au même module n3.py.
    controller = LABS / rel / "tools/controller.py"
    if not controller.is_file():
        return ""
    source = controller.read_text(encoding="utf-8")
    partage = "pve-eprouver-cluster/tools/n3.py"
    if partage in source:
        controller = LABS / partage
    elif (controller.parent / "n3.py").is_file():
        controller = controller.parent / "n3.py"
    for node in ast.walk(ast.parse(controller.read_text(encoding="utf-8"))):
        if (
            isinstance(node, ast.Assign)
            and any(ast.unparse(t) == "self.work" for t in node.targets)
            and isinstance(node.value, ast.BinOp)
            and isinstance(node.value.op, ast.Div)
            and ast.unparse(node.value.left) == "self.lab"
            and isinstance(node.value.right, ast.Constant)
            and isinstance(node.value.right.value, str)
        ):
            return node.value.right.value.rstrip("/")
    return ""


def _textes_du_lab(rel: str) -> list[Path]:
    return [LABS / rel / nom for nom in TEXTES if (LABS / rel / nom).is_file()]


def _cites(rel: str, motif: re.Pattern[str]) -> set[str]:
    trouves: set[str] = set()
    for fichier in _textes_du_lab(rel):
        trouves |= set(motif.findall(fichier.read_text(encoding="utf-8")))
    return trouves


TOUS = tous_les_labs()
HOTES = hotes_declares()


def test_le_meta_declare_bien_des_hotes() -> None:
    """Garde-fou : sans hôte déclaré, le contrôle des hôtes serait vert à vide.

    Il refuserait tout, ou ne comparerait rien selon l'ordre des assertions :
    dans les deux cas il ne mesurerait plus le catalogue.
    """
    assert TOUS, "aucun lab.yaml trouvé : le glob est cassé."
    assert HOTES, (
        "meta.yml ne déclare aucun hôte sous infra.hosts : la comparaison "
        "ci-dessous n'aurait plus de référence."
    )


def test_les_enonces_nomment_bien_la_machine() -> None:
    """Garde-fou de couverture, et il mesure quelque chose de réel.

    Un contrôle qui ne trouve plus rien à contrôler est vert, et c'est la forme
    la plus discrète de faux vert.
    """
    citants = [rel for rel in TOUS if _cites(rel, HOTE_CITE)]

    assert len(citants) >= LABS_CITANTS_MINIMUM, (
        f"Seuls {len(citants)} labs sur {len(TOUS)} citent un hôte `*.lab` : "
        "l'expression régulière ne trouve probablement plus rien, ou les "
        "énoncés ont cessé de nommer la machine sur laquelle on travaille."
    )


def test_les_extracteurs_voient_ce_qu_ils_pretendent_voir() -> None:
    """Les deux motifs, éprouvés sur des cas construits.

    Construits plutôt que cherchés dans le dépôt : ce test ne doit pas dépendre
    du contenu du jour, et il doit rester utile le jour où le catalogue
    n'emploie plus la tournure d'aujourd'hui.
    """
    assert HOTE_CITE.findall("Sur `docker.lab`, une Debian jetable.") == ["docker.lab"]
    assert HOTE_CITE.findall("Le conteneur `vitrine` tourne.") == [], (
        "Un nom de conteneur ne doit pas être pris pour un hôte."
    )
    assert HOTE_CITE.findall("le fichier `daemon.json`") == [], (
        "Un nom de fichier ne doit pas être pris pour un hôte."
    )
    assert HOTE_CITE.findall("conservez son label `dsoxlab.lab`") == [], (
        "Le nom du label ne doit pas être pris pour un hôte."
    )
    assert HOTE_CITE.findall("Sur `docker.lab`, le label `dsoxlab.lab`") == [
        "docker.lab"
    ], "L'exclusion du label ne doit pas emporter l'hôte cité dans la même phrase."

    assert CHEMIN_CITE.findall("écrivez `challenge/work/compose.yaml`") == [
        "challenge/work/compose.yaml"
    ]
    assert CHEMIN_CITE.findall("lancez `docker ps`") == []


@pytest.mark.parametrize("rel", TOUS)
def test_un_enonce_ne_cite_aucun_hote_inexistant(rel: str) -> None:
    """Un hôte cité doit être une machine que `dsoxlab provision` crée.

    Le FQDN d'un lab `vm` vit dans `meta.yml: infra.hosts[]`, et `lab.yaml` le
    reprend dans `runtime.targets[].host`. Un énoncé qui en cite un autre
    envoie l'apprenant ouvrir une session SSH vers rien.
    """
    egares = sorted(_cites(rel, HOTE_CITE) - HOTES)

    assert not egares, (
        f"{rel} cite des hôtes que meta.yml ne déclare pas : {egares}\n\n"
        f"Hôtes déclarés : {sorted(HOTES)}\n\n"
        "Soit l'énoncé se trompe de nom, soit la machine manque au bloc "
        "`infra.hosts` du meta.yml, et le lab ne se provisionne pas."
    )


@pytest.mark.parametrize("rel", TOUS)
def test_un_enonce_ne_cite_aucun_chemin_inexistant(rel: str) -> None:
    """Un chemin cité doit mener quelque part.

    Trois cas légitimes, et un seul fautif :

      - le répertoire de travail déclaré par le lab, qui n'existe qu'après
        `dsoxlab run` ;
      - un chemin SOUS ce répertoire, donc une fixture qui y sera copiée ;
      - un fichier ou un dossier réellement présent dans le lab.

    Tout le reste envoie l'apprenant à un endroit où rien n'est lu.
    """
    workdir = workdir_declare(rel)
    lab = LABS / rel

    egares = []
    for cite in sorted(_cites(rel, CHEMIN_CITE)):
        propre = cite.rstrip("/")
        if workdir and (propre == workdir or propre.startswith(workdir + "/")):
            continue
        if (lab / propre).exists():
            continue
        egares.append(cite)

    assert not egares, (
        f"{rel} cite des chemins qui n'existent pas : {egares}\n\n"
        f"Répertoire de travail déclaré : `{workdir or 'aucun'}`\n\n"
        "Un énoncé qui désigne un endroit où rien n'est lu coûte une demi-heure "
        "à qui le suit à la lettre : c'est ce que l'issue #237 de dsoxlab a "
        "mesuré, où les mêmes fichiers valaient 0/100 au mauvais endroit et "
        "100/100 au bon."
    )
