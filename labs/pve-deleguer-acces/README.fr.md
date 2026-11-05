# Déléguer les droits sans élargir le périmètre

**Niveau :** N2 · **Environnement :** mono · **Durée :** non calibrée

## Mission

Déléguer l’exploitation d’un pool à une équipe et conserver une séparation vérifiable avec le pool voisin.

## Périmètre et sécurité

Ce lab ne vise que `VMIDs 201/n2-delegueracc and 216/n2-voisin; pools lab-n2-deleguer and lab-n2-voisin; test accounts equipe-n2@pve, auditeur-n2@pve, and secours-n2@pve.`. Il n’installe pas Proxmox VE, ne crée pas de cluster, ne modifie pas son appartenance et n’utilise aucun disque, réseau, compte ou workload non attribué. Préservez la console de secours et le chemin d’administration du nœud. N’exposez aucun secret dans les preuves. Une configuration différente convient si elle respecte le contrat et produit le même état observé.

Le nœud PVE doit déjà être installé et accessible ; le setup prépare uniquement la fixture bornée du lab.

## Démarrage

Lisez `scenario.fr.md` et le manifeste `/opt/lab-proxmox/pve-deleguer-acces/manifest.yml`. N’exécutez le setup que sur la cible PVE attribuée. Les tests interrogent la configuration/l’état réel de PVE, jamais l’historique des commandes ou des preuves déclaratives. Le nettoyage ne retire que les fixtures explicitement détenues par ce lab ou son manifeste, jamais une ressource externe ou le cluster.
