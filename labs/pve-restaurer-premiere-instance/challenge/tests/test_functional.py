from __future__ import annotations

import pytest

from conftest import lab_host, lab_target_host, message

HOTE = lab_target_host("pve.lab")
VMID = 199


@pytest.fixture(scope="module")
def pve():
    return lab_host(HOTE)


def test_une_archive_vzdump_lisible_est_presente(pve):
    result = pve.run(
        "find /var/lib/vz/dump -maxdepth 1 -type f -name 'vzdump-qemu-198-*.vma.zst' -print"
    )
    assert result.rc == 0 and result.stdout.strip(), message(
        en="No local vzdump archive for source VM 198; a snapshot is not a backup.",
        fr="Aucune archive vzdump locale de la VM source 198 ; un snapshot n'est pas une sauvegarde.",
    )
    archive = result.stdout.splitlines()[0]
    assert pve.run(f"zstd -t '{archive}'").rc == 0, message(
        en="The backup archive fails its compression integrity check.",
        fr="L'archive échoue au contrôle d'intégrité de compression.",
    )


def test_la_vm_restauree_est_distincte_et_demarre(pve):
    cfg = pve.run(f"qm config {VMID}")
    assert cfg.rc == 0 and "scsi0:" in cfg.stdout, message(
        en="The restored VM is missing its system disk.",
        fr="La VM restaurée n'a pas son disque système.",
    )
    assert "clone:" not in cfg.stdout, message(
        en="Restore to the assigned VMID; a linked clone is not a restore.",
        fr="Restaurez vers le VMID attribué ; un clone lié n'est pas une restauration.",
    )
    assert pve.run(f"qm status {VMID}").stdout.strip().endswith("running"), message(
        en="The restored VM is not running.", fr="La VM restaurée ne tourne pas."
    )
