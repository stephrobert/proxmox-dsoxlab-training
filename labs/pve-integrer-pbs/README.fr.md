# Déployer PBS et réaliser une sauvegarde vérifiable

**Niveau :** N2 · **Environnement :** backup · **Durée :** non calibrée

## Mission

Installer un PBS de lab, l’intégrer au nœud et sauvegarder deux charges avec des identités limitées.

## Périmètre et sécurité

Ce lab ne vise que `PBS storage lab-pbs-n2-207; externally supplied PBS endpoint/datastore and VM/CT workloads; no PBS host is provisioned by this lab.`. Il n’installe pas Proxmox VE, ne crée pas de cluster, ne modifie pas son appartenance et n’utilise aucun disque, réseau, compte ou workload non attribué. Préservez la console de secours et le chemin d’administration du nœud. N’exposez aucun secret dans les preuves. Une configuration différente convient si elle respecte le contrat et produit le même état observé.

Requires an externally prepared PBS endpoint/datastore and both assigned VM/CT workloads. This setup does not install or emulate PBS.

## Démarrage

Lisez `scenario.fr.md` et le manifeste `/opt/lab-proxmox/pve-integrer-pbs/manifest.yml`. N’exécutez le setup que sur la cible PVE attribuée. Les tests interrogent la configuration/l’état réel de PVE, jamais l’historique des commandes ou des preuves déclaratives. Le nettoyage ne retire que les fixtures détenues par ce lab et listées dans le manifeste ; le stockage, les workloads externes et l’état du cluster sont préservés.
