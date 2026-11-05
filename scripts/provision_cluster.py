#!/usr/bin/env python3
"""Provisionner les trois nœuds Proxmox uniquement après un prévol explicite."""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
HOTES_CLUSTER = ("pve01.lab", "pve02.lab", "pve03.lab")
GIB = 1024**3
RAM_LIBRE_MIN = 26 * GIB
DISQUE_LIBRE_MIN = 280 * GIB
CPU_LOGIQUE_MIN = 12
CHARGE_MAX_PAR_CPU = 0.5
CONFIRMATION = "PROVISIONNER LE CLUSTER PROXMOX"


def _commande(argv: list[str]) -> str:
    resultat = subprocess.run(argv, check=True, capture_output=True, text=True)
    return resultat.stdout


def _configuration() -> tuple[str, str, dict[str, dict[str, int]]]:
    meta = yaml.safe_load((RACINE / "meta.yml").read_text(encoding="utf-8"))
    infra = meta["infra"]
    kvm = infra["providers"]["kvm"]
    uri = kvm.get("libvirt_uri", "qemu:///system")
    pool = kvm.get("storage_pool", "default")
    hotes = {hote["name"]: hote for hote in infra["hosts"]}
    manquants = set(HOTES_CLUSTER) - set(hotes)
    if manquants:
        raise ValueError(f"Nœuds cluster absents de meta.yml : {sorted(manquants)}")
    return uri, pool, hotes


def _capacite_hote(uri: str, pool: str) -> tuple[int, int, int, float]:
    with Path("/proc/meminfo").open(encoding="ascii") as meminfo:
        ligne = next(
            ligne for ligne in meminfo if ligne.startswith("MemAvailable:")
        )
    ram_libre = int(ligne.split()[1]) * 1024
    cpus = os.cpu_count() or 0
    charge = os.getloadavg()[0]

    xml = _commande(["virsh", "-c", uri, "pool-dumpxml", pool])
    pool_xml = ET.fromstring(xml)  # noqa: S314 - XML produced by local libvirt.
    chemin = pool_xml.findtext("./target/path")
    if not chemin:
        raise ValueError(f"Le pool libvirt {pool!r} n'a pas de chemin local mesurable.")
    disque_libre = int(
        _commande(["df", "-B1", "--output=avail", chemin]).splitlines()[1].strip()
    )
    return ram_libre, disque_libre, cpus, charge


def _verifier_capacite(
    ram_libre: int,
    disque_libre: int,
    cpus: int,
    charge: float,
) -> list[str]:
    ecarts = []
    if ram_libre < RAM_LIBRE_MIN:
        ecarts.append(
            f"RAM disponible {ram_libre / GIB:.1f} GiB, minimum {RAM_LIBRE_MIN / GIB} GiB"
        )
    if disque_libre < DISQUE_LIBRE_MIN:
        ecarts.append(
            f"espace du pool {disque_libre / GIB:.1f} GiB, minimum "
            f"{DISQUE_LIBRE_MIN / GIB} GiB"
        )
    if cpus < CPU_LOGIQUE_MIN:
        ecarts.append(f"{cpus} CPU logiques, minimum {CPU_LOGIQUE_MIN}")
    if cpus and charge > cpus * CHARGE_MAX_PAR_CPU:
        ecarts.append(
            f"charge 1 min {charge:.2f}, maximum {cpus * CHARGE_MAX_PAR_CPU:.2f}"
        )
    return ecarts


def _commande_provisionnement() -> list[str]:
    return [
        "dsoxlab", "provision",
        *[option for hote in HOTES_CLUSTER for option in ("--host", hote)],
        "--lab-home", str(RACINE),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="provisionner après prévol conforme et confirmation interactive",
    )
    args = parser.parse_args()

    try:
        uri, pool, hotes = _configuration()
        if not uri.startswith("qemu:///"):
            raise ValueError(
                f"URI libvirt {uri!r} non locale : le prévol ne peut pas mesurer "
                "la capacité de l'hôte distant."
            )
        ram_libre, disque_libre, cpus, charge = _capacite_hote(uri, pool)
    except (
        OSError, ValueError, KeyError, IndexError, ET.ParseError,
        subprocess.CalledProcessError,
    ) as exc:
        detail = getattr(exc, "stderr", None) or str(exc)
        print(f"Prévol impossible : {detail}", file=sys.stderr)
        return 2

    ram_demandee = sum(hotes[nom]["ram_mb"] for nom in HOTES_CLUSTER)
    print("Cibles explicites :", ", ".join(HOTES_CLUSTER))
    print(f"RAM déclarée des nœuds : {ram_demandee / 1024:.1f} GiB")
    print(f"RAM disponible / exigée : {ram_libre / GIB:.1f} / {RAM_LIBRE_MIN / GIB} GiB")
    print(
        f"Espace libre du pool {pool} / exigé : "
        f"{disque_libre / GIB:.1f} / {DISQUE_LIBRE_MIN / GIB} GiB"
    )
    print(f"CPU logiques / charge 1 min : {cpus} / {charge:.2f}")

    ecarts = _verifier_capacite(ram_libre, disque_libre, cpus, charge)
    if ecarts:
        print("Provisionnement refusé :", file=sys.stderr)
        for ecart in ecarts:
            print(f"- {ecart}", file=sys.stderr)
        return 2

    if not args.apply:
        print("Prévol réussi, aucune VM créée. Ajouter --apply pour continuer.")
        return 0

    if not sys.stdin.isatty():
        print("Confirmation interactive requise ; aucune VM créée.", file=sys.stderr)
        return 2
    commande = _commande_provisionnement()
    print("Commande ciblée :", shlex.join(commande))
    print(f"Tapez exactement « {CONFIRMATION} » pour continuer.")
    try:
        confirmation = input("> ")
    except EOFError:
        confirmation = ""
    if confirmation != CONFIRMATION:
        print("Confirmation absente ou incorrecte ; aucune VM créée.")
        return 2
    try:
        return subprocess.run(commande, check=False).returncode
    except OSError as exc:
        print(f"Impossible de lancer dsoxlab : {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
