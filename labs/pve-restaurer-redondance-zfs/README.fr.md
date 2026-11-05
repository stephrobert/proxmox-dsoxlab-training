# Exploiter un miroir ZFS et récupérer un disque

**Niveau :** N2 · **Environnement :** stockage · **Durée :** non calibrée

## Mission

Maintenir un service sur un miroir de lab dégradé puis retrouver une redondance saine.

## Périmètre et sécurité

Ce lab ne vise que `Dedicated disposable two-device ZFS pool labmirror-n2-214 and evaluator-owned corpus; setup does not create or degrade a pool.`. Il n’installe pas Proxmox VE, ne crée pas de cluster, ne modifie pas son appartenance et n’utilise aucun disque, réseau, compte ou workload non attribué. Préservez la console de secours et le chemin d’administration du nœud. N’exposez aucun secret dans les preuves. Une configuration différente convient si elle respecte le contrat et produit le même état observé.

Requires the dedicated disposable two-device `labmirror-n2-214` mirror; setup never creates or degrades a pool.

## Démarrage

Lisez `scenario.fr.md` et le manifeste `/opt/lab-proxmox/pve-restaurer-redondance-zfs/manifest.yml`. N’exécutez le setup que sur la cible PVE attribuée. Les tests interrogent la configuration/l’état réel de PVE, jamais l’historique des commandes ou des preuves déclaratives. Le nettoyage ne retire que les fixtures explicitement détenues par ce lab ou son manifeste, jamais une ressource externe ou le cluster.
