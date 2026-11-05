# Maintenir un nœud et préparer une montée de version

**Niveau :** N2 · **Environnement :** maintenance · **Durée :** non calibrée

## Mission

Maintenir un nœud de laboratoire avec précontrôles, recette et procédure de reprise documentée.

## Périmètre et sécurité

Ce lab ne vise que `Disposable version-qualified PVE node, verified backups, and console; setup changes no VMID or package state.`. Il n’installe pas Proxmox VE, ne crée pas de cluster, ne modifie pas son appartenance et n’utilise aucun disque, réseau, compte ou workload non attribué. Préservez la console de secours et le chemin d’administration du nœud. N’exposez aucun secret dans les preuves. Une configuration différente convient si elle respecte le contrat et produit le même état observé.

Requires a disposable, version-qualified PVE node and verified backups; setup never upgrades a node.

## Démarrage

Lisez `scenario.fr.md` et le manifeste `/opt/lab-proxmox/pve-maintenir-noeud/manifest.yml`. N’exécutez le setup que sur la cible PVE attribuée. Les tests interrogent la configuration/l’état réel de PVE, jamais l’historique des commandes ou des preuves déclaratives. Le nettoyage ne retire que les fixtures explicitement détenues par ce lab ou son manifeste, jamais une ressource externe ou le cluster.
