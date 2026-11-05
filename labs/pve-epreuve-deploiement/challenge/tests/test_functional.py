from __future__ import annotations

import pytest

from conftest import lab_host, lab_target_host, message

HOTE = lab_target_host("pve.lab")
VMID = 200


@pytest.fixture(scope="module")
def pve():
    return lab_host(HOTE)


def test_le_service_temoin_est_actif_sur_l_instance_finale(pve):
    assert pve.run(f"qm status {VMID}").stdout.strip().endswith("running"), message(
        en=f"Final VM {VMID} is not running.", fr=f"La VM finale {VMID} ne tourne pas."
    )
    result = pve.run(f"qm guest exec {VMID} -- systemctl is-active temoin.service")
    assert result.rc == 0 and "active" in result.stdout, message(
        en="The witness service is not active in the delivered instance.",
        fr="Le service témoin n'est pas actif dans l'instance livrée.",
    )


def test_une_sauvegarde_independante_est_presente(pve):
    archives = pve.run(
        "find /var/lib/vz/dump -maxdepth 1 -type f -name 'vzdump-qemu-198-*.vma.zst' -print"
    )
    assert archives.rc == 0 and archives.stdout.strip(), message(
        en="The source instance 198 has no independent vzdump archive for restore.",
        fr="L'instance source 198 n'a pas d'archive vzdump indépendante à restaurer.",
    )
    assert pve.run(f"qm config {VMID}").rc == 0, message(
        en="The delivered instance is absent after backup creation.",
        fr="L'instance livrée est absente après création de la sauvegarde.",
    )
