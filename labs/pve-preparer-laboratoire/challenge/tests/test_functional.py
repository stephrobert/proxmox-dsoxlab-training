from __future__ import annotations

import pytest

from conftest import lab_host, lab_target_host, message

HOTE = lab_target_host("pve.lab")


@pytest.fixture(scope="module")
def machine():
    return lab_host(HOTE)


@pytest.mark.garde_fou
def test_le_processeur_expose_la_virtualisation(machine):
    flags = machine.run("grep -m1 '^flags' /proc/cpuinfo").stdout.split()
    assert {"vmx", "svm"} & set(flags), message(
        en="The host VM does not expose VT-x/AMD-V.", fr="La VM hôte n'expose pas VT-x/AMD-V."
    )
    assert machine.run("test -c /dev/kvm").rc == 0, message(
        en="/dev/kvm is absent; CPU flags alone do not prove usable KVM.",
        fr="/dev/kvm est absent ; les drapeaux CPU seuls ne prouvent pas que KVM fonctionne.",
    )


@pytest.mark.garde_fou
def test_la_virtualisation_imbriquee_est_active(machine):
    paths = ("/sys/module/kvm_intel/parameters/nested", "/sys/module/kvm_amd/parameters/nested")
    results = [machine.run(f"cat {path}") for path in paths]
    assert any(r.rc == 0 and r.stdout.strip().upper() in {"Y", "1"} for r in results), message(
        en="Nested virtualization is disabled in the active KVM module.",
        fr="La virtualisation imbriquée est désactivée dans le module KVM actif.",
    )


def test_un_invite_temoin_utilise_reellement_kvm(machine):
    pid = machine.file(
        "/run/lab-proxmox/pve-preparer-laboratoire/preparer-kvm.pid"
    ).content_string.strip()
    assert pid.isdecimal(), message(
        en="Start the assigned QEMU witness with KVM acceleration.",
        fr="Démarrez l'invité témoin QEMU attribué avec l'accélération KVM.",
    )
    handles = machine.run(f"find /proc/{pid}/fd -lname /dev/kvm -print")
    assert handles.rc == 0 and handles.stdout.strip(), message(
        en="The QEMU witness is not using /dev/kvm; a CPU flag or config option is not proof of acceleration.",
        fr="L'invité QEMU n'utilise pas /dev/kvm ; un drapeau CPU ou une option de configuration ne prouve pas l'accélération.",
    )
