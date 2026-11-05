from pathlib import Path
from runpy import run_path

LAB = Path(__file__).resolve().parent.parent
if __name__ == "__main__":
    run_path(str(LAB.parent / "pve-eprouver-cluster/tools/n3.py"))["main"](LAB)
