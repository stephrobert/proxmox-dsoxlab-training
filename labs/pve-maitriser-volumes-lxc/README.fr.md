# Gérer les volumes et identités des LXC

**Niveau :** N2 · **Environnement :** backup · **Durée :** non calibrée

## Mission

Corriger un accès aux données d’un CT et prouver la restauration de tous les volumes demandés.

## Périmètre et sécurité

Ce lab ne vise que `Pre-provisioned disposable CTID 384 named lab-n2-volumes; managed volume lab-n2-volumes; bind mount /srv/lab-n2-share.`. Il n’installe pas Proxmox VE, ne crée pas de cluster, ne modifie pas son appartenance et n’utilise aucun disque, réseau, compte ou workload non attribué. Préservez la console de secours et le chemin d’administration du nœud. N’exposez aucun secret dans les preuves. Une configuration différente convient si elle respecte le contrat et produit le même état observé.

Requires the pre-provisioned disposable unprivileged CT 384, its supplied managed volume, bind mount, and backup.

## Démarrage

Lisez `scenario.fr.md` et le manifeste `/opt/lab-proxmox/pve-maitriser-volumes-lxc/manifest.yml`. N’exécutez le setup que sur la cible PVE attribuée. Les tests interrogent la configuration/l’état réel de PVE, jamais l’historique des commandes ou des preuves déclaratives. Le nettoyage ne retire que les fixtures explicitement détenues par ce lab ou son manifeste, jamais une ressource externe ou le cluster.
