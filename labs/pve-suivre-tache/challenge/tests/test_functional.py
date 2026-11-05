"""Un verdict par propriété annoncée ; les lectures impossibles refusent."""

import json

import pytest

from conftest import lab_host, lab_target_host, message
from shared.proxmox_checks import (
    config,
    read,
    read_json,
    require_equal,
)


@pytest.fixture(scope="module")
def pve():
    return lab_host(lab_target_host("pve.lab"))


REGISTRE = "/var/lib/lab-proxmox/pve-suivre-tache/registre.json"


def _rapport(pve):
    output = read(pve, "cat /root/rapport-taches.txt")
    rows = [line.split(":", 1) for line in output.splitlines() if ":" in line]
    keys = [key.strip() for key, value in rows]
    assert len(keys) == len(set(keys)), message(
        en="Write exactly one report line per key.", fr="Écrivez une seule ligne de rapport par clé.",
    )
    return {key.strip(): value.strip() for key, value in rows}


def _registre(pve):
    return json.loads(read(pve, f"cat {REGISTRE}"))


@pytest.mark.parametrize("vmid", [191, 192])
def test_l_upid_designe_la_bonne_tache(pve, vmid):
    row = _rapport(pve).get(f"demarrage-{vmid}", "")
    require_equal(row.split(" ")[0], _registre(pve)[f"demarrage-{vmid}"], f"UPID {vmid}")


@pytest.mark.parametrize("vmid", [191, 192])
def test_le_resultat_final_est_exact(pve, vmid):
    row = _rapport(pve).get(f"demarrage-{vmid}", "")
    upid = _registre(pve)[f"demarrage-{vmid}"]
    node = upid.split(":")[1]
    result = read_json(pve, f"pvesh get /nodes/{node}/tasks/{upid}/status --output-format json", dict)
    assert result.get("status") == "stopped" and result.get("exitstatus"), message(
        en="Wait for a readable final task result.", fr="Attendez un résultat final de tâche lisible.",
    )
    require_equal(row.partition(" ")[2], result["exitstatus"], f"résultat / result {vmid}")


def test_l_etat_rapporte_est_courant(pve):
    report = _rapport(pve)
    state = read(pve, "qm status 190")
    assert state in {"status: running", "status: stopped"}, message(
        en="Read a valid current state for VM 190.", fr="Lisez un état courant valide pour la VM 190.",
    )
    require_equal(report.get("etat-190"), state.removeprefix("status: "), "état / state 190")


@pytest.mark.parametrize("vmid", [191, 192])
def test_une_vm_temporaire_est_supprimee(pve, vmid):
    _rapport(pve)
    guests = read_json(pve, "pvesh get /cluster/resources --type vm --output-format json", list)
    assert all(int(g.get("vmid", -1)) != vmid for g in guests), message(
        en=f"Delete temporary VM {vmid}.", fr=f"Supprimez la VM temporaire {vmid}.",
    )


def test_la_sentinelle_existe(pve):
    _rapport(pve)
    config(pve, "qm", 190)


def test_la_configuration_de_la_sentinelle_est_intacte(pve):
    _rapport(pve)
    output = read(pve, "sha256sum /etc/pve/qemu-server/190.conf")
    require_equal(output.split()[0], _registre(pve)["conf-190"], "empreinte / fingerprint 190")
