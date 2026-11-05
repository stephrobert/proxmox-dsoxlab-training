# Diagnostiquer une VM indisponible

**Niveau :** N2 · **Environnement :** mono · **Durée :** non calibrée

## Mission

Rétablir une instance indisponible en identifiant la cause et en conservant ses données et protections.

## Périmètre et sécurité

Ce lab ne vise que `Pre-provisioned disposable VMID 211 named n2-diagnostique with its disk, guest agent, and firewall; the only injected fault is net0 on vmbr999.`. Il n’installe pas Proxmox VE, ne crée pas de cluster, ne modifie pas son appartenance et n’utilise aucun disque, réseau, compte ou workload non attribué. Préservez la console de secours et le chemin d’administration du nœud. N’exposez aucun secret dans les preuves. Une configuration différente convient si elle respecte le contrat et produit le même état observé.

Nécessite la VM jetable 211 attribuée, avec disque amorçable, pare-feu, agent invité et vmbr0 avant l’injection de la panne réseau.

## Démarrage

Lisez `scenario.fr.md` et le manifeste `/opt/lab-proxmox/pve-diagnostiquer-instance/manifest.yml`. N’exécutez le setup que sur la cible PVE attribuée. Les tests interrogent la configuration/l’état réel de PVE, jamais l’historique des commandes ou des preuves déclaratives. Le nettoyage ne retire que les fixtures explicitement détenues par ce lab ou son manifeste, jamais une ressource externe ou le cluster.
