# Chiffrer, conserver et vérifier les sauvegardes

**Niveau :** N2 · **Environnement :** backup · **Durée :** non calibrée

## Mission

Configurer chiffrement, rétention et vérification, puis prouver qu’une clé récupérée permet la restauration.

## Périmètre et sécurité

Ce lab ne vise que `PBS storage lab-pbs-n2-208; supplied VM/backups, limited identity, and offline key vault.`. Il n’installe pas Proxmox VE, ne crée pas de cluster, ne modifie pas son appartenance et n’utilise aucun disque, réseau, compte ou workload non attribué. Préservez la console de secours et le chemin d’administration du nœud. N’exposez aucun secret dans les preuves. Une configuration différente convient si elle respecte le contrat et produit le même état observé.

Requires an externally prepared PBS datastore, offline key vault, dated backups, and a disposable corruption fixture.

## Démarrage

Lisez `scenario.fr.md` et le manifeste `/opt/lab-proxmox/pve-proteger-sauvegardes/manifest.yml`. N’exécutez le setup que sur la cible PVE attribuée. Les tests interrogent la configuration/l’état réel de PVE, jamais l’historique des commandes ou des preuves déclaratives. Le nettoyage ne retire que les fixtures détenues par ce lab et listées dans le manifeste ; le stockage, les workloads externes et l’état du cluster sont préservés.
