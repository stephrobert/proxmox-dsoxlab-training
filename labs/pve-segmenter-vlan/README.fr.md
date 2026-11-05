# Segmenter et diagnostiquer les VLAN

**Niveau :** N2 · **Environnement :** reseau · **Durée :** non calibrée

## Mission

Construire deux segments et appliquer une exception routée explicite sans exposer le management.

## Périmètre et sécurité

Ce lab ne vise que `VMID 205; isolated bridge vmbr205 and VLAN IDs 285/286; no physical uplink is assigned.`. Il n’installe pas Proxmox VE, ne crée pas de cluster, ne modifie pas son appartenance et n’utilise aucun disque, réseau, compte ou workload non attribué. Préservez la console de secours et le chemin d’administration du nœud. N’exposez aucun secret dans les preuves. Une configuration différente convient si elle respecte le contrat et produit le même état observé.

Le nœud PVE doit déjà être installé et accessible ; le setup prépare uniquement la fixture bornée du lab.

## Démarrage

Lisez `scenario.fr.md` et le manifeste `/opt/lab-proxmox/pve-segmenter-vlan/manifest.yml`. N’exécutez le setup que sur la cible PVE attribuée. Les tests interrogent la configuration/l’état réel de PVE, jamais l’historique des commandes ou des preuves déclaratives. Le nettoyage ne retire que les fixtures détenues par ce lab et listées dans le manifeste ; le stockage, les workloads externes et l’état du cluster sont préservés.
