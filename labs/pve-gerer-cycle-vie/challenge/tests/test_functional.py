from __future__ import annotations

import pytest

from conftest import lab_host, lab_target_host, message

HOTE = lab_target_host("pve.lab")
VMID = 195


@pytest.fixture(scope="module")
def pve():
    return lab_host(HOTE)


def test_la_vm_a_ete_dimensionnee_et_demarre(pve):
    cfg = pve.run(f"qm config {VMID}")
    assert cfg.rc == 0, message(
        en=f"VM {VMID} is missing; create the lifecycle exercise VM.",
        fr=f"La VM {VMID} manque ; créez la VM d'exercice du cycle de vie.",
    )
    assert "memory: 2048" in cfg.stdout and "cores: 2" in cfg.stdout, message(
        en="The exercise VM must stay within 2 GiB and two vCPUs.",
        fr="La VM d'exercice doit rester limitée à 2 Gio et deux vCPU.",
    )
    assert pve.run(f"qm status {VMID}").stdout.strip().endswith("running"), message(
        en="The resized VM is not running.", fr="La VM redimensionnée ne tourne pas."
    )


def test_le_point_de_retour_local_existe(pve):
    snap = pve.run(f"qm listsnapshot {VMID}")
    assert snap.rc == 0 and "avant-changement" in snap.stdout, message(
        en="Create the named local rollback snapshot before changing the guest.",
        fr="Créez l'instantané local de retour nommé avant de modifier l'invité.",
    )
    assert "scsi0:" in pve.run(f"qm config {VMID}").stdout, message(
        en="The guest system disk is missing.", fr="Le disque système invité manque."
    )
