"""Pure local content/guardrail tests; never connect to PVE or provision."""

import ast
import json
import unittest
from pathlib import Path

import n3
import yaml

REPO = Path(__file__).resolve().parents[3]
LABS = tuple(n3.ALLOWED_ACTIONS)


def result(value):
    return {"rc": 0, "stdout": json.dumps(value), "stderr": ""}


class LocalContractTests(unittest.TestCase):
    def test_every_catalog_criterion_has_exact_identity_and_method(self):
        catalog = yaml.safe_load(
            (REPO.parent / "test-astro-5/src/data/parcours/proxmox.yaml").read_text()
        )
        missions = {m["id"]: m for m in catalog["travaux_pratiques"]}
        for name in LABS:
            contract = json.loads((REPO / "labs" / name / "contract.json").read_text())
            for actual, expected in zip(contract["points_a_tester"], missions[name]["points_a_tester"], strict=True):
                for key in ("id", "attendu", "methode"):
                    self.assertEqual(actual[key], expected[key], f"{name}/{key}")

    def test_bilingual_structure_and_exact_runtime(self):
        for name in LABS:
            lab = REPO / "labs" / name
            for file in ("README.md", "README.fr.md", "scenario.md", "scenario.fr.md",
                         "challenge/README.md", "challenge/README.fr.md",
                         "tools/controller.py", "challenge/tests/test_functional.py",
                         "setup.yaml", "cleanup.yaml"):
                self.assertTrue((lab / file).is_file(), f"{name}/{file}")
            for file in ("lab.yaml", "lab.fr.yaml"):
                runtime = yaml.safe_load((lab / file).read_text())["runtime"]
                self.assertEqual(runtime["default"], "proxmox-cluster")
                self.assertEqual(runtime["targets"][0]["name"], "proxmox-cluster")
                self.assertEqual(runtime["targets"][0]["host"], "pve01.lab")
                self.assertEqual(runtime["targets"][0]["roles"],
                                 {"node2": "pve02.lab", "node3": "pve03.lab"})

    def test_syntax_and_no_stale_host_names_or_automatic_cluster_formation(self):
        for name in LABS:
            roots = [REPO / "labs" / name, REPO / "solution-en-clair" / name]
            for root in roots:
                for file in root.rglob("*"):
                    if file.suffix not in {".py", ".yaml", ".md", ".json"}:
                        continue
                    text = file.read_text()
                    self.assertNotRegex(text, r"\bpve(?:2|3)?\.lab\b", str(file))
                    self.assertNotRegex(text, r"\bpvecm\s+(?:create|add)\b", str(file))
                    if file.suffix == ".py":
                        ast.parse(text, filename=str(file))
                    elif file.suffix == ".yaml":
                        list(yaml.safe_load_all(text))
                    elif file.suffix == ".json":
                        json.loads(text)

    def test_refuses_unknown_process_observer(self):
        state = {"nodes": {"pve01.lab": {"processes": result([{"vmid": 9351}])}}}
        with self.assertRaises(n3.PreconditionError):
            n3.owners(state, 9351)

    def test_power_off_is_required_to_replace_missing_observer(self):
        state = {
            "nodes": {"pve01.lab": {"processes": result([{"vmid": 9351}])}},
            "power": {
                "pve02.lab": {"rc": 0, "stdout": "shut off\n"},
                "pve03.lab": {"rc": 0, "stdout": "shut off\n"},
            },
        }
        self.assertEqual(n3.owners(state, 9351), ["pve01.lab"])
        state["power"]["pve02.lab"]["stdout"] = "running\n"
        with self.assertRaises(n3.PreconditionError):
            n3.owners(state, 9351)

    def test_refuses_cross_identity_disk_writer(self):
        state = {"nodes": {
            host: {"processes": result([
                {"vmid": 9999, "disks": ["/dev/zvol/lab/vm-9351-disk-0"]}
            ] if host == "pve01.lab" else [])} for host in n3.HOSTS
        }}
        with self.assertRaises(n3.PreconditionError):
            n3.owners(state, 9351)

    def test_business_requires_durable_data_not_health_flag(self):
        with self.assertRaises(n3.PreconditionError):
            n3.business({"samples": [{"status": 200, "body": {"healthy": True}}]})
        good = {"samples": [{"status": 200, "body": {"sequence": 12, "marker": "nonce"}}]}
        self.assertEqual(n3.business(good)["sequence"], 12)
        lost = {"samples": [{"status": 200, "body": {"sequence": 11, "marker": "nonce"}}]}
        with self.assertRaises(n3.PreconditionError):
            n3.same_data(good, lost)

    def test_exam_has_no_learner_reference_or_hints(self):
        lab = REPO / "labs/pve-epreuve-disponibilite"
        self.assertNotIn("reference_approved", (lab / "tools/controller.py").read_text())
        self.assertIn("No progressive hints or solution", (lab / "challenge/README.md").read_text())
        self.assertIn("Aucun indice progressif ni solution", (lab / "challenge/README.fr.md").read_text())


if __name__ == "__main__":
    unittest.main()
