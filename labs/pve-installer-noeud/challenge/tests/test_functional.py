from __future__ import annotations

import json

import pytest

from conftest import lab_host, lab_target_host, message

HOTE = lab_target_host("pve.lab")
VMID = 190


@pytest.fixture(scope="module")
def pve():
    return lab_host(HOTE)


def test_le_noeud_installe_est_un_invite_reel(pve):
    etat = pve.run(f"qm status {VMID}")
    assert etat.rc == 0 and "running" in etat.stdout, message(
        en=f"Nested installation VM {VMID} is absent or stopped; install it from the verified ISO.",
        fr=f"La VM d'installation imbriquée {VMID} est absente ou arrêtée ; installez-la depuis l'ISO vérifiée.",
    )
    config = pve.run(f"qm config {VMID}").stdout
    assert "iso/" not in config, message(
        en="The installer ISO is still attached; boot the installed system disk.",
        fr="L'ISO d'installation est encore attachée ; démarrez sur le disque système installé.",
    )
    assert "boot:" in config and "scsi0" in config, message(
        en="The installed node must boot from its system disk.",
        fr="Le nœud installé doit démarrer sur son disque système.",
    )


def test_pve_est_reellement_installe_dans_l_invite(pve):
    result = pve.run(f"qm guest exec {VMID} -- pveversion --verbose")
    assert result.rc == 0, message(
        en="Guest agent could not run pveversion inside the nested node; enable it and verify PVE.",
        fr="L'agent invité n'a pas exécuté pveversion dans le nœud imbriqué ; activez-le et vérifiez PVE.",
    )
    output = json.loads(result.stdout).get("out-data", "")
    assert "pve-manager" in output, message(
        en="The nested guest does not report an installed Proxmox VE manager.",
        fr="L'invité imbriqué ne signale pas de gestionnaire Proxmox VE installé.",
    )
