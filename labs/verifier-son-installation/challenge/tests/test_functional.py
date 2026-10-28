"""Note l'installation de Proxmox que l'apprenant a faite lui-même.

Ce lab ne fabrique rien. Il reçoit une Debian 13 NUE, l'apprenant y installe
Proxmox VE 9 par le dépôt `pve-no-subscription`, et ces tests mesurent le
résultat face au cahier des charges publié dans le guide d'installation :

    https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/installation/

Trois principes guident leur écriture.

D'abord, chaque test interroge l'ÉTAT du système, jamais les commandes tapées
pour l'obtenir. Un apprenant qui installe Proxmox autrement que par le chemin
suggéré, et qui atteint le même état, a réussi.

Ensuite, chaque message d'échec NOMME le poste en défaut et dit quoi corriger.
C'est ce qui fait de ce lab un exercice plutôt qu'une barrière : une
installation qui ne passe pas se répare sans tout recommencer. Un message
« assert False » n'apprendrait rien.

Enfin, ON NE NOTE QUE LE TRAVAIL DE L'APPRENANT. Les quatre autres postes du
cahier des charges, la distribution de base, la virtualisation imbriquée, le
dimensionnement et le second disque brut, sont garantis par le provisionnement
de la machine : ce sont des PRÉREQUIS, pas des acquis. Ils sont vérifiés par
`setup.yaml`, qui refuse de démarrer le lab s'ils manquent.

Cette séparation n'est pas cosmétique, elle a été mesurée le 2026-10-27 : en
notant ces quatre postes, le lab rendait 40/100 sur une machine où RIEN n'avait
encore été fait. Un score de départ non nul vole quarante points à l'apprenant
et casse l'attestation du catalogue, qui exige un 0 avant la solution.

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
    """L'interface web RÉPOND, et pas seulement « le port est ouvert ».

    Ce test a été renforcé le 2026-10-27, après qu'il eut validé à 100/100 une
    installation inutilisable. Il se contentait alors de voir le port 8006 tenu
    par pveproxy. Or pveproxy peut très bien écouter pendant que ses workers
    meurent en boucle, faute de certificat :

        /etc/pve/local/pve-ssl.pem: failed to use local certificate chain

    Un port ouvert est une FORME ; une réponse HTTP est un COMPORTEMENT. Seul
    le second prouve que l'apprenant pourra se connecter.
    """
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
    # Le vrai controle : une requete, et un code de retour. `--max-time` evite
    # qu un pveproxy en souffrance fasse pendre le test indefiniment.
    code = pve.run(
        f"curl -sk --max-time 15 -o /dev/null -w '%{{http_code}}' "
        f"https://127.0.0.1:{PORT_INTERFACE}/"
    ).stdout.strip()
    assert code == "200", message(
        en=(
            f"Port {PORT_INTERFACE} is open but the interface answers {code or 'nothing'} "
            "instead of 200. pveproxy is listening without serving. Look at "
            "`journalctl -u pveproxy -n 20`: a missing certificate "
            "(/etc/pve/local/pve-ssl.pem) is the usual cause, and `pvecm updatecerts "
            "--force` regenerates it."
        ),
        fr=(
            f"Le port {PORT_INTERFACE} est ouvert mais l'interface répond "
            f"{code or 'rien'} au lieu de 200. pveproxy écoute sans servir. "
            "Regardez `journalctl -u pveproxy -n 20` : un certificat absent "
            "(/etc/pve/local/pve-ssl.pem) en est la cause habituelle, et "
            "`pvecm updatecerts --force` le régénère."
        ),
    )


def _diagnostic_apt(hote, sortie: str) -> str:
    """Dit POURQUOI apt échoue, au lieu de se contenter de le constater.

    La cause la plus fréquente après l'installation n'est pas le dépôt, mais la
    résolution de noms : en confiant le réseau à ifupdown, on met
    systemd-resolved hors circuit, et /etc/resolv.conf, qui est un LIEN vers
    son stub, continue de pointer sur 127.0.0.53. Plus rien ne résout, et rien
    d'autre ne paraît cassé. Mesuré le 2026-10-27.
    """
    if "resolving" not in sortie.lower():
        return ""
    lien = hote.run("test -L /etc/resolv.conf && echo lien || echo fichier").stdout.strip()
    resolved = hote.run("systemctl is-active systemd-resolved").stdout.strip()
    detail = (
        "\n  Cause probable : la RÉSOLUTION DE NOMS, pas le dépôt."
        f"\n  /etc/resolv.conf est un {lien}, systemd-resolved est {resolved!r}."
    )
    if lien == "lien" and resolved != "active":
        detail += (
            "\n  C'est le cas qui piège : le lien mène au stub d'un service"
            "\n  désactivé. Supprimez le lien et posez un vrai fichier portant"
            "\n  `nameserver <adresse de votre passerelle>`."
        )
    return detail


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
    # Ce `apt-get update` couvre DEUX pannes a la fois : un depot inutilisable,
    # et une resolution de noms cassee. Le diagnostic distingue les deux, sans
    # quoi l apprenant chercherait du cote du depot alors que c est le DNS.
    maj = pve.run("apt-get update -qq 2>&1")
    detail = _diagnostic_apt(pve, maj.stdout) if maj.rc != 0 else ""
    assert maj.rc == 0, message(
        en=(
            f"`apt-get update` fails, so the repositories are unusable:\n"
            f"{maj.stdout.strip()}{detail}"
        ),
        fr=(
            f"`apt-get update` échoue, les dépôts sont donc inutilisables :\n"
            f"{maj.stdout.strip()}{detail}"
        ),
    )
