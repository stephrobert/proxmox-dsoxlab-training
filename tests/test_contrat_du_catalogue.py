"""Le catalogue tient ses propres promesses, et pas seulement le contrat.

`dsoxlab validate-structure` vérifie le CONTRAT. Ces tests vérifient ce que ce
dépôt-ci promet en plus, et que l'outil ne peut pas connaître.
"""

from __future__ import annotations

import pathlib

import pytest
import yaml

from conftest import lab_target_roles

RACINE = pathlib.Path(__file__).resolve().parent.parent


def test_le_cluster_est_un_environnement_distinct_provisionnable_a_la_demande() -> None:
    meta = yaml.safe_load((RACINE / "meta.yml").read_text(encoding="utf-8"))
    hosts = {host["name"]: host for host in meta["infra"]["hosts"]}
    assert {"pve.lab", "pve01.lab", "pve02.lab", "pve03.lab"} <= hosts.keys()
    assert [
        (
            hosts[name]["ram_mb"],
            hosts[name]["vcpu"],
            hosts[name]["disk_gb"],
            hosts[name]["extra_disk_gb"],
        )
        for name in ("pve01.lab", "pve02.lab", "pve03.lab")
    ] == [(8192, 4, 40, 40)] * 3


def test_les_roles_suivent_la_cible_effectivement_choisie(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "lab.yaml").write_text(
        yaml.safe_dump(
            {
                "runtime": {
                    "default": "cluster",
                    "targets": [
                        {
                            "name": "proxmox-cluster",
                            "host": "pve01.lab",
                            "roles": {"node2": "pve02.lab", "node3": "pve03.lab"},
                        },
                        {"name": "single", "host": "pve.lab"},
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.delenv("DSOXLAB_TARGET", raising=False)
    assert lab_target_roles(tmp_path, "pve01.lab") == {
        "node2": "pve02.lab",
        "node3": "pve03.lab",
    }

    monkeypatch.setenv("DSOXLAB_TARGET", "single")
    assert lab_target_roles(tmp_path, "pve.lab") == {}


def test_les_labs_cluster_selectionnent_les_trois_hotes_du_bon_environnement() -> None:
    hotes_cluster = {"pve01.lab", "pve02.lab", "pve03.lab"}
    labs_cluster = []

    for chemin in _labs():
        lab = yaml.safe_load(chemin.read_text(encoding="utf-8"))
        runtime = lab.get("runtime") or {}
        for cible in runtime.get("targets") or []:
            roles = cible.get("roles") or {}
            if cible.get("host") not in hotes_cluster and not (
                set(roles.values()) & hotes_cluster
            ):
                continue

            labs_cluster.append(chemin.parent.name)
            assert runtime.get("default") == "proxmox-cluster"
            assert cible.get("name") == "proxmox-cluster"
            assert cible.get("host") == "pve01.lab"
            assert roles == {"node2": "pve02.lab", "node3": "pve03.lab"}

    assert labs_cluster, "aucun lab ne sélectionne l'environnement proxmox-cluster"


def test_les_roles_refusent_une_cible_ambigue_ou_inconnue(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "lab.yaml").write_text(
        yaml.safe_dump(
            {
                "runtime": {
                    "targets": [
                        {"name": "proxmox-cluster", "host": "pve01.lab"},
                        {"name": "single", "host": "pve01.lab"},
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.delenv("DSOXLAB_TARGET", raising=False)
    with pytest.raises(RuntimeError, match="ambiguë ou inconnue"):
        lab_target_roles(tmp_path, "pve01.lab")

    monkeypatch.setenv("DSOXLAB_TARGET", "unknown")
    with pytest.raises(RuntimeError, match="ambiguë ou inconnue"):
        lab_target_roles(tmp_path, "pve01.lab")


def _labs() -> list[pathlib.Path]:
    return sorted(RACINE.glob("labs/**/lab.yaml"))


def test_kvm_est_le_provider_par_defaut() -> None:
    meta = yaml.safe_load((RACINE / "meta.yml").read_text(encoding="utf-8"))

    assert meta["infra"]["provider"] == "kvm"


def test_aucun_lab_na_disparu_en_silence() -> None:
    """Un répertoire de lab sans `lab.yaml` lisible est un défaut muet.

    `validate-structure` itère sur ce qui a CHARGÉ : un `lab.yaml` qui lève au
    parsing disparaît du catalogue en silence, et la validation passe sans un
    mot. Ce test est le seul qui attrape ce cas.

    Deux situations que « zéro lab » confond, et qu'on sépare donc :

        labs/ vide                   un catalogue neuf, rien à conclure
        labs/ peuplé, aucun lab.yaml un défaut, et on le nomme
    """
    repertoires = [
        chemin
        for chemin in (RACINE / "labs").rglob("*")
        if chemin.is_dir() and not chemin.name.startswith(".")
    ]
    if not repertoires:
        pytest.skip("labs/ est vide : catalogue neuf, crée un lab avec `dsoxlab new lab <id>`")

    assert _labs(), (
        f"{len(repertoires)} répertoire(s) sous labs/ mais aucun lab.yaml "
        "lisible : un lab.yaml lève au parsing et a disparu du catalogue en "
        "silence. Joue `dsoxlab list-labs` pour le voir."
    )


def test_chaque_lab_est_declare_dans_le_meta() -> None:
    """Un lab présent sur le disque mais absent du meta.yml n'est pas ordonné.

    Il reste jouable, mais il n'apparaît dans aucune section : ni `list-labs`
    ni `next` ne savent où le placer.
    """
    meta = yaml.safe_load((RACINE / "meta.yml").read_text(encoding="utf-8"))
    declares = {
        chemin for section in (meta.get("sections") or []) for chemin in (section.get("labs") or [])
    }
    sur_le_disque = {p.parent.relative_to(RACINE / "labs").as_posix() for p in _labs()}
    orphelins = sorted(sur_le_disque - declares)

    assert not orphelins, (
        f"{len(orphelins)} lab(s) sur le disque mais absents des sections du meta.yml : {orphelins}"
    )


def test_les_labs_sont_ordonnes_une_seule_fois_et_identifies_par_leur_dossier() -> None:
    meta = yaml.safe_load((RACINE / "meta.yml").read_text(encoding="utf-8"))
    declares = [
        chemin for section in (meta.get("sections") or []) for chemin in (section.get("labs") or [])
    ]
    assert len(declares) == len(set(declares)), "un lab apparaît plusieurs fois dans les sections"

    mauvais_ids = []
    for chemin in _labs():
        identifiant = yaml.safe_load(chemin.read_text(encoding="utf-8")).get("id")
        attendu = chemin.parent.relative_to(RACINE / "labs").as_posix()
        if identifiant != attendu:
            mauvais_ids.append(f"{attendu}: id={identifiant!r}")

    assert not mauvais_ids, f"identifiants de manifeste incorrects : {mauvais_ids}"


def test_le_meta_ne_declare_pas_de_lab_absent() -> None:
    """L'inverse, que `validate-structure` ne vérifie pas.

    Le validateur itère sur `discover_labs()`, donc sur ce qui existe : un lab
    déclaré dans le meta.yml mais absent du disque passe sans un mot.
    """
    meta = yaml.safe_load((RACINE / "meta.yml").read_text(encoding="utf-8"))
    declares = {
        chemin for section in (meta.get("sections") or []) for chemin in (section.get("labs") or [])
    }
    manquants = sorted(c for c in declares if not (RACINE / "labs" / c / "lab.yaml").is_file())

    assert not manquants, (
        f"{len(manquants)} lab(s) déclarés dans le meta.yml mais absents du disque : {manquants}"
    )


def test_parite_des_langues() -> None:
    """Un énoncé traduit d'un seul côté est signalé, pas laissé à la relecture."""
    boiteux = []
    for lab in _labs():
        base = lab.parent
        for nom in ("README", "scenario", "challenge/README"):
            en = base / f"{nom}.md"
            fr = base / f"{nom}.fr.md"
            if en.is_file() != fr.is_file():
                boiteux.append(f"{base.name}/{nom}")

    assert not boiteux, f"traduits d'un seul côté : {boiteux}"


def test_chaque_lab_a_une_suite_de_tests_fonctionnels() -> None:
    sans_tests = [
        lab.parent.name
        for lab in _labs()
        if not (lab.parent / "challenge/tests/test_functional.py").is_file()
    ]

    assert not sans_tests, f"labs sans tests fonctionnels : {sans_tests}"
