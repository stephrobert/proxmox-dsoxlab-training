"""Le provisionnement du cluster reste explicite et borné par les ressources."""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import provision_cluster


def test_le_prevol_refuse_un_hote_sous_dimensionne() -> None:
    ecarts = provision_cluster._verifier_capacite(
        ram_libre=25 * provision_cluster.GIB,
        disque_libre=300 * provision_cluster.GIB,
        cpus=16,
        charge=0.5,
    )
    assert any("RAM disponible" in ecart for ecart in ecarts)


def test_le_prevol_refuse_un_pool_insuffisant() -> None:
    ecarts = provision_cluster._verifier_capacite(
        ram_libre=30 * provision_cluster.GIB,
        disque_libre=279 * provision_cluster.GIB,
        cpus=16,
        charge=0.5,
    )
    assert any("espace du pool" in ecart for ecart in ecarts)


def test_le_prevol_refuse_charge_cpu_excessive() -> None:
    ecarts = provision_cluster._verifier_capacite(
        ram_libre=30 * provision_cluster.GIB,
        disque_libre=300 * provision_cluster.GIB,
        cpus=16,
        charge=8.1,
    )
    assert any("charge 1 min" in ecart for ecart in ecarts)


def test_une_capacite_suffisante_ne_bloque_pas_le_cluster() -> None:
    assert provision_cluster._verifier_capacite(
        ram_libre=26 * provision_cluster.GIB,
        disque_libre=280 * provision_cluster.GIB,
        cpus=12,
        charge=6,
    ) == []


def test_la_commande_cible_explicitement_les_trois_noeuds() -> None:
    assert provision_cluster._commande_provisionnement() == [
        "dsoxlab", "provision",
        "--host", "pve01.lab",
        "--host", "pve02.lab",
        "--host", "pve03.lab",
        "--lab-home", str(provision_cluster.RACINE),
    ]


def test_le_prevol_par_defaut_ne_lance_aucun_provisionnement(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        provision_cluster,
        "_configuration",
        lambda: ("qemu:///system", "default", {
            host: {"ram_mb": 8192} for host in provision_cluster.HOTES_CLUSTER
        }),
    )
    monkeypatch.setattr(
        provision_cluster,
        "_capacite_hote",
        lambda _uri, _pool: (
            30 * provision_cluster.GIB,
            300 * provision_cluster.GIB,
            16,
            0.5,
        ),
    )
    monkeypatch.setattr(sys, "argv", ["provision_cluster.py"])
    monkeypatch.setattr(
        provision_cluster.subprocess,
        "run",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("Le mode prévol ne doit lancer aucune commande.")
        ),
    )

    assert provision_cluster.main() == 0


def test_le_provisionnement_refuse_sans_terminal_interactif(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        provision_cluster,
        "_configuration",
        lambda: ("qemu:///system", "default", {
            host: {"ram_mb": 8192} for host in provision_cluster.HOTES_CLUSTER
        }),
    )
    monkeypatch.setattr(
        provision_cluster,
        "_capacite_hote",
        lambda _uri, _pool: (
            30 * provision_cluster.GIB,
            300 * provision_cluster.GIB,
            16,
            0.5,
        ),
    )
    monkeypatch.setattr(sys, "argv", ["provision_cluster.py", "--apply"])
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    monkeypatch.setattr(
        provision_cluster.subprocess,
        "run",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("Aucune commande ne doit partir sans confirmation.")
        ),
    )

    assert provision_cluster.main() == 2
