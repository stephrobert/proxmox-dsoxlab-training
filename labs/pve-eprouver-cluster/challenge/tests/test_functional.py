"""Real catalog criteria; no PVE connection is attempted at collection time."""

import json
import subprocess
from pathlib import Path

import pytest

from conftest import message

LAB = Path(__file__).resolve().parents[2]
CRITERIA = [p["id"] for p in json.loads((LAB / "contract.json").read_text())["points_a_tester"]]


@pytest.mark.parametrize("criterion", CRITERIA)
def test_catalog_criterion(criterion):
    result = subprocess.run(
        ["python3", str(LAB / "tools/controller.py"), "check", "--criterion", criterion],
        capture_output=True, text=True, timeout=600, check=False,
    )
    assert result.returncode == 0, message(
        en=(
            f"Complete criterion '{criterion}' and run the check again. "
            "The controller could not confirm the required state.\n"
            f"Technical diagnostic:\n{result.stdout}{result.stderr}"
        ),
        fr=(
            f"Satisfaites le critère '{criterion}', puis relancez le contrôle. "
            "Le contrôleur ne peut pas confirmer l'état attendu.\n"
            f"Diagnostic technique :\n{result.stdout}{result.stderr}"
        ),
    )
