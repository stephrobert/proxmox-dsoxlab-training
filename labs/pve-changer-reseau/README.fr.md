# Router, traduire et modifier le réseau sans se couper

**Niveau :** N2 · **Environnement :** reseau · **Durée :** non calibrée

## Mission

Mettre en place les flux sortants et une publication contrôlée, puis effectuer un changement réseau réversible.

## Périmètre et sécurité

Ce lab ne vise que `VMID 206; isolated bridge vmbr206; nftables chain N2LAB206; no physical uplink or default route is assigned.`. Il n’installe pas Proxmox VE, ne crée pas de cluster, ne modifie pas son appartenance et n’utilise aucun disque, réseau, compte ou workload non attribué. Préservez la console de secours et le chemin d’administration du nœud. N’exposez aucun secret dans les preuves. Une configuration différente convient si elle respecte le contrat et produit le même état observé.

Le nœud PVE doit déjà être installé et accessible ; le setup prépare uniquement la fixture bornée du lab.

## Démarrage

Lisez `scenario.fr.md` et le manifeste `/opt/lab-proxmox/pve-changer-reseau/manifest.yml`. N’exécutez le setup que sur la cible PVE attribuée. Les tests interrogent la configuration/l’état réel de PVE, jamais l’historique des commandes ou des preuves déclaratives. Le nettoyage ne retire que les fixtures détenues par ce lab et listées dans le manifeste ; le stockage, les workloads externes et l’état du cluster sont préservés.
