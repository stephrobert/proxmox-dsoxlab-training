"""Note l'installation de Proxmox que l'apprenant a faite lui-même.

Ce lab ne fabrique rien. Il reçoit une Debian 13 NUE, l'apprenant y installe
Proxmox VE 9 par le dépôt `pve-no-subscription`, et ces tests mesurent le
résultat face au cahier des charges publié dans le guide d'installation :

    https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/installation/

Deux principes guident leur écriture.

D'abord, chaque test interroge l'ÉTAT du système, jamais les commandes tapées
pour l'obtenir. Un apprenant qui installe Proxmox autrement que par le chemin
suggéré, et qui atteint le même état, a réussi.

Ensuite, chaque message d'échec NOMME le poste en défaut et dit quoi corriger.
C'est ce qui fait de ce lab un exercice plutôt qu'une barrière : une
installation qui ne passe pas se répare sans tout recommencer. Un message
« assert False » n'apprendrait rien.

Les valeurs attendues viennent du cahier des charges, mesuré le 2026-10-27 sur
une installation réelle de Proxmox VE 9.2.2.
"""

from __future__ import annotations

import re

import pytest

from conftest import lab_host, lab_target_host, message

CIBLE = lab_target_host("pve.lab")

# Le cahier des charges, en un seul endroit : ces chiffres sont ceux du guide,
# et les messages d'échec s'en servent pour dire ce qui est attendu.
VCPU_MINI = 4
RAM_MINI_MO = 5800  # 6 Go annoncés, moins ce que le noyau et le firmware réservent
DISQUE_SYSTEME_MINI_GO = 35  # 40 Go annoncés, moins la marge de formatage
SECOND_DISQUE_MINI_GO = 18  # 20 Go annoncés
PORT_INTERFACE = 8006


@pytest.fixture(scope="module")
def pve():
    return lab_host(CIBLE)


def _go(hote, peripherique: str) -> float:
    """Taille d'un périphérique bloc, en Go décimaux."""
    res = hote.run(f"lsblk -bdno SIZE /dev/{peripherique} 2>/dev/null")
    sortie = res.stdout.strip()
    return int(sortie) / 1_000_000_000 if sortie.isdigit() else 0.0


def test_proxmox_est_installe(pve) -> None:
    """`pveversion` répond, donc les paquets Proxmox sont en place."""
    res = pve.run("pveversion")
    assert res.rc == 0, message(
        en=(
            "`pveversion` is not available: Proxmox VE is not installed on this "
            "machine. Install it on top of Debian 13 with the "
            "pve-no-subscription repository, as the installation guide explains."
        ),
        fr=(
            "`pveversion` ne répond pas : Proxmox VE n'est pas installé sur cette "
            "machine. Installez-le par-dessus Debian 13 avec le dépôt "
            "pve-no-subscription, comme l'explique le guide d'installation."
        ),
    )


def test_la_version_est_bien_une_9(pve) -> None:
    """Le cahier des charges demande la branche 9, pas une version antérieure."""
    sortie = pve.run("pveversion").stdout.strip()
    trouve = re.search(r"pve-manager/(\d+)\.(\d+)", sortie)
    assert trouve, message(
        en=f"Could not read the version from `pveversion` output: {sortie!r}",
        fr=f"Version illisible dans la sortie de `pveversion` : {sortie!r}",
    )
    majeure = int(trouve.group(1))
    assert majeure >= 9, message(
        en=(
            f"Proxmox VE {trouve.group(0)} is installed, but the course targets "
            "branch 9, built on Debian 13. Check which repository you added: a "
            "Debian 12 repository installs Proxmox VE 8."
        ),
        fr=(
            f"Proxmox VE {trouve.group(0)} est installé, alors que la formation "
            "vise la branche 9, bâtie sur Debian 13. Vérifiez le dépôt ajouté : "
            "un dépôt Debian 12 installe Proxmox VE 8."
        ),
    )


def test_la_base_est_bien_debian_13(pve) -> None:
    """Proxmox VE 9 repose sur Debian 13 « trixie »."""
    nom = pve.run(". /etc/os-release && echo $VERSION_CODENAME").stdout.strip()
    assert nom == "trixie", message(
        en=(
            f"The base system is Debian {nom!r}, not 'trixie'. Proxmox VE 9 is "
            "built on Debian 13: reinstall from a Debian 13 image."
        ),
        fr=(
            f"Le système de base est Debian {nom!r}, et non « trixie ». "
            "Proxmox VE 9 repose sur Debian 13 : repartez d'une image Debian 13."
        ),
    )


def test_les_services_proxmox_tournent(pve) -> None:
    """Les trois services que le guide fait vérifier sont actifs."""
    for service in ("pve-cluster", "pvedaemon", "pveproxy"):
        etat = pve.run(f"systemctl is-active {service}").stdout.strip()
        assert etat == "active", message(
            en=(
                f"Service {service} is {etat!r} instead of 'active'. Look at "
                f"`journalctl -u {service} -n 50` to find out why it will not start."
            ),
            fr=(
                f"Le service {service} est {etat!r} au lieu de « active ». "
                f"Regardez `journalctl -u {service} -n 50` pour savoir pourquoi "
                "il ne démarre pas."
            ),
        )


def test_l_interface_web_repond(pve) -> None:
    """Le port 8006 écoute, et c'est bien pveproxy qui le tient."""
    res = pve.run(f"ss -tlnp | grep :{PORT_INTERFACE}")
    assert res.rc == 0 and res.stdout.strip(), message(
        en=(
            f"Nothing is listening on port {PORT_INTERFACE}: the Proxmox web "
            "interface is unreachable. Check that pveproxy is running."
        ),
        fr=(
            f"Rien n'écoute sur le port {PORT_INTERFACE} : l'interface web de "
            "Proxmox est injoignable. Vérifiez que pveproxy tourne."
        ),
    )
    assert "pveproxy" in res.stdout, message(
        en=(
            f"Port {PORT_INTERFACE} is taken by another process than pveproxy:\n"
            f"{res.stdout.strip()}"
        ),
        fr=(
            f"Le port {PORT_INTERFACE} est pris par un autre processus que "
            f"pveproxy :\n{res.stdout.strip()}"
        ),
    )


def test_le_pont_vmbr0_porte_l_adresse(pve) -> None:
    """L'adresse vit sur le pont, condition pour que les VM joignent le réseau."""
    res = pve.run("ip -brief a show vmbr0")
    assert res.rc == 0, message(
        en=(
            "Bridge vmbr0 does not exist. Proxmox needs it to connect virtual "
            "machines to the network: declare it in /etc/network/interfaces, "
            "with the physical interface as bridge-ports."
        ),
        fr=(
            "Le pont vmbr0 n'existe pas. Proxmox en a besoin pour relier les "
            "machines virtuelles au réseau : déclarez-le dans "
            "/etc/network/interfaces, avec la carte physique en bridge-ports."
        ),
    )
    assert re.search(r"\b\d+\.\d+\.\d+\.\d+/\d+", res.stdout), message(
        en=(
            f"Bridge vmbr0 carries no IPv4 address:\n{res.stdout.strip()}\n"
            "The server address must sit on the bridge, not on the physical card."
        ),
        fr=(
            f"Le pont vmbr0 ne porte aucune adresse IPv4 :\n{res.stdout.strip()}\n"
            "L'adresse du serveur doit être sur le pont, pas sur la carte physique."
        ),
    )


def test_la_virtualisation_imbriquee_arrive_jusqu_ici(pve) -> None:
    """Sans /dev/kvm, ce Proxmox ne pourra démarrer aucune machine."""
    assert pve.file("/dev/kvm").exists, message(
        en=(
            "/dev/kvm is missing: this Proxmox will not be able to start a single "
            "virtual machine. Nested virtualization is not enabled on the host. "
            "Shut the VM down, enable it, then start again."
        ),
        fr=(
            "/dev/kvm est absent : ce Proxmox ne pourra démarrer aucune machine "
            "virtuelle. La virtualisation imbriquée n'est pas active sur "
            "l'hyperviseur hôte. Éteignez la VM, activez-la, puis redémarrez."
        ),
    )
    drapeaux = pve.run("grep -cE '(vmx|svm)' /proc/cpuinfo").stdout.strip()
    assert drapeaux.isdigit() and int(drapeaux) > 0, message(
        en=(
            "The CPU exposes no vmx or svm flag: the processor extensions do not "
            "reach this machine, even though /dev/kvm exists."
        ),
        fr=(
            "Le processeur n'expose ni vmx ni svm : les extensions du processeur "
            "n'arrivent pas jusqu'à cette machine, bien que /dev/kvm existe."
        ),
    )


def test_le_dimensionnement_respecte_le_cahier_des_charges(pve) -> None:
    """Processeurs et mémoire, les deux postes qu'on sous-estime le plus."""
    vcpu = int(pve.run("nproc").stdout.strip() or 0)
    assert vcpu >= VCPU_MINI, message(
        en=f"{vcpu} vCPU available, the specification asks for {VCPU_MINI}.",
        fr=f"{vcpu} vCPU disponibles, le cahier des charges en demande {VCPU_MINI}.",
    )
    ram_mo = int(pve.run("awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo").stdout.strip() or 0)
    assert ram_mo >= RAM_MINI_MO, message(
        en=(
            f"{ram_mo} MB of RAM, the specification asks for 6 GB. Proxmox needs "
            "room for its own services AND for the machines you will create."
        ),
        fr=(
            f"{ram_mo} Mo de RAM, le cahier des charges en demande 6 Go. Proxmox "
            "a besoin de place pour ses propres services ET pour les machines "
            "que vous créerez."
        ),
    )


def test_le_second_disque_est_present_et_brut(pve) -> None:
    """Le disque que les labs de stockage utiliseront, intact."""
    disques = pve.run(
        "lsblk -dno NAME,TYPE | awk '$2==\"disk\" {print $1}'"
    ).stdout.split()
    assert disques, message(
        en="No block device found, which should not happen.",
        fr="Aucun périphérique bloc trouvé, ce qui ne devrait pas arriver.",
    )

    # Le disque systeme est celui qui porte la racine ; tout autre disque assez
    # grand fera l affaire comme second disque. On ne suppose PAS un nom de
    # peripherique : vda, sda et nvme0n1 sont tous legitimes selon l hote.
    racine = pve.run("findmnt -no SOURCE /").stdout.strip()
    porteur = pve.run(f"lsblk -no pkname {racine} 2>/dev/null | head -1").stdout.strip()

    candidats = [d for d in disques if d != porteur and _go(pve, d) >= SECOND_DISQUE_MINI_GO]
    assert candidats, message(
        en=(
            "No second disk of at least 20 GB beside the system disk "
            f"({porteur or 'unknown'}). The storage labs need a RAW disk: add "
            "one to the virtual machine, and do not partition it."
        ),
        fr=(
            "Aucun second disque d'au moins 20 Go à côté du disque système "
            f"({porteur or 'inconnu'}). Les labs de stockage ont besoin d'un "
            "disque BRUT : ajoutez-en un à la machine virtuelle, sans le "
            "partitionner."
        ),
    )

    # « Brut » veut dire : aucune partition, aucun systeme de fichiers, aucune
    # signature LVM ou ZFS. Un disque deja pris par un pool ne sert plus a rien.
    intacts = []
    for d in candidats:
        partitions = pve.run(f"lsblk -no NAME {d} | tail -n +2").stdout.strip()
        signature = pve.run(f"lsblk -no FSTYPE /dev/{d}").stdout.strip()
        if not partitions and not signature:
            intacts.append(d)
    assert intacts, message(
        en=(
            f"The second disk ({', '.join(candidats)}) is already in use: it "
            "carries partitions or a filesystem signature. The storage labs "
            "build their own pool on it, so it must stay raw. Wipe it, or add "
            "another disk."
        ),
        fr=(
            f"Le second disque ({', '.join(candidats)}) est déjà utilisé : il "
            "porte des partitions ou une signature de système de fichiers. Les "
            "labs de stockage y construiront leur propre pool, il doit donc "
            "rester brut. Effacez-le, ou ajoutez un autre disque."
        ),
    )


def test_le_depot_sans_abonnement_est_configure(pve) -> None:
    """Sans lui, la machine ne reçoit aucune mise à jour."""
    # Debian 13 decrit ses depots au format deb822 : des fichiers .sources, et
    # non plus les lignes « deb … » des fichiers .list. On accepte les deux, car
    # une machine mise a niveau depuis Debian 12 peut porter l ancien format.
    res = pve.run(
        "grep -rhs -E 'pve-no-subscription' /etc/apt/sources.list.d/ /etc/apt/sources.list"
    )
    assert res.stdout.strip(), message(
        en=(
            "The pve-no-subscription repository is not configured. Without it, "
            "apt reaches only the enterprise repository, which answers 401 "
            "without a subscription, and the machine gets no updates."
        ),
        fr=(
            "Le dépôt pve-no-subscription n'est pas configuré. Sans lui, apt ne "
            "voit que le dépôt entreprise, qui répond 401 sans abonnement, et la "
            "machine ne reçoit aucune mise à jour."
        ),
    )
    maj = pve.run("apt-get update -qq 2>&1")
    assert maj.rc == 0, message(
        en=f"`apt-get update` fails, so the repositories are unusable:\n{maj.stdout.strip()}",
        fr=f"`apt-get update` échoue, les dépôts sont donc inutilisables :\n{maj.stdout.strip()}",
    )
