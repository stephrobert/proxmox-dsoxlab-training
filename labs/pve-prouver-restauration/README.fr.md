# Restaurer un service et mesurer RPO et RTO

**Niveau :** N2 · **Environnement :** backup · **Durée :** non calibrée

## Mission

Rétablir une application depuis PBS avec source indisponible et rendre un bilan de reprise vérifiable.

## Périmètre et sécurité

Ce lab ne vise que `Empty recovery VMID 209 reserved for a restored VM named n2-restored-209; PBS storage lab-pbs-n2-209, evaluator-owned backup/journal, and isolated recovery network.`. Il n’installe pas Proxmox VE, ne crée pas de cluster, ne modifie pas son appartenance et n’utilise aucun disque, réseau, compte ou workload non attribué. Préservez la console de secours et le chemin d’administration du nœud. N’exposez aucun secret dans les preuves. Une configuration différente convient si elle respecte le contrat et produit le même état observé.

Requires the assigned PBS recovery fixture, evaluator-owned journal, and isolated recovery network.

## Démarrage

Lisez `scenario.fr.md` et le manifeste `/opt/lab-proxmox/pve-prouver-restauration/manifest.yml`. N’exécutez le setup que sur la cible PVE attribuée. Les tests interrogent la configuration/l’état réel de PVE, jamais l’historique des commandes ou des preuves déclaratives. Le nettoyage ne retire que les fixtures détenues par ce lab et listées dans le manifeste ; le stockage, les workloads externes et l’état du cluster sont préservés.
