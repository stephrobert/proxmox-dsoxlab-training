# Filtrer le management et les invités

**Niveau :** N2 · **Environnement :** reseau · **Durée :** non calibrée

## Mission

Appliquer une politique de flux minimale entre administration, invités et client non autorisé.

## Périmètre et sécurité

Ce lab ne vise que `VMID 203 and its per-VM firewall file /etc/pve/firewall/203.fw; no physical NIC or external network is assigned.`. Il n’installe pas Proxmox VE, ne crée pas de cluster, ne modifie pas son appartenance et n’utilise aucun disque, réseau, compte ou workload non attribué. Préservez la console de secours et le chemin d’administration du nœud. N’exposez aucun secret dans les preuves. Une configuration différente convient si elle respecte le contrat et produit le même état observé.

Le nœud PVE doit déjà être installé et accessible ; le setup prépare uniquement la fixture bornée du lab.

## Démarrage

Lisez `scenario.fr.md` et le manifeste `/opt/lab-proxmox/pve-filtrer-flux/manifest.yml`. N’exécutez le setup que sur la cible PVE attribuée. Les tests interrogent la configuration/l’état réel de PVE, jamais l’historique des commandes ou des preuves déclaratives. Le nettoyage ne retire que les fixtures explicitement détenues par ce lab ou son manifeste, jamais une ressource externe ou le cluster.
