# Mission : Exploiter une VM Windows avec VirtIO

Utilisez uniquement une ISO Windows pour laquelle vous disposez d’une licence et d’une autorisation, ainsi que l’ISO officielle des pilotes VirtIO. Installez une version choisie et prise en charge, chargez les pilotes disque/réseau, vérifiez l’agent et le réseau après redémarrage, retirez les médias et restaurez une sauvegarde incluant EFI et TPM.

## Critères d’acceptation

1. La configuration réelle comprend EFI, TPM 2.0, disque/réseau VirtIO et aucun média d’installation.
2. Après redémarrage, l’agent invité rapporte une interface/adresse réseau active.
3. Une restauration réelle conserve les périphériques EFI et TPM.

## Prérequis

BLOQUÉ tant que les deux chemins ISO et une autorisation de licence explicite ne figurent pas dans /etc/lab-proxmox/pve-integrer-windows.yml. Le setup ne télécharge aucun média Windows et ne contourne ni activation ni OOBE.

Ce scénario n’installe pas PVE, ne provisionne aucun hôte et n’installe aucune fonctionnalité.
