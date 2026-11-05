#!/usr/bin/env python3
"""Analyser les Dockerfile du catalogue, hors fixtures et travail apprenant.

Adapté de Containers : les solutions vivent ici sous solution/, et les
fichiers chiffrés doivent être déchiffrés avant l'analyse. Sans clé, le
contrôle dit explicitement qu'il n'a pas été joué sur ces fichiers.
"""

import argparse
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCLUS = {".git", ".venv", "fixtures", "work", "solution-en-clair"}


def dockerfiles(root):
    return sorted(
        p for p in root.rglob("Dockerfile*")
        if p.is_file() and not EXCLUS.intersection(p.relative_to(root).parts)
    )


def controler(root):
    fichiers = dockerfiles(root)
    if not fichiers:
        print("N/A : aucun Dockerfile de catalogue ou de solution à contrôler.")
        return 0
    resultat = 0
    with tempfile.TemporaryDirectory(prefix="hadolint-") as temporaire:
        for index, fichier in enumerate(fichiers):
            cible = fichier
            if fichier.read_bytes().startswith(b"$ANSIBLE_VAULT"):
                cle = root / ".vault-pass"
                if not cle.is_file():
                    print(f"::warning::Contrôle NON JOUÉ : {fichier.relative_to(root)} est chiffré, clé absente.")
                    continue
                clair = subprocess.run(
                    ["ansible-vault", "view", "--vault-password-file", str(cle), str(fichier)],
                    capture_output=True, check=False,
                )
                if clair.returncode:
                    print(f"Échec du déchiffrement : {fichier.relative_to(root)}")
                    return 1
                cible = Path(temporaire) / f"Dockerfile-{index}"
                cible.write_bytes(clair.stdout)
            args = ["hadolint"]
            if "solution" in fichier.relative_to(root).parts:
                args += ["--failure-threshold", "error"]
            resultat = max(resultat, subprocess.run([*args, str(cible)], check=False).returncode)
    return resultat


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    return controler(ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
