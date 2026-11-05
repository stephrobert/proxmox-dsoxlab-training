# Défi : Exploiter une VM Windows avec VirtIO

Utilisez uniquement une ISO Windows pour laquelle vous disposez d’une licence et d’une autorisation, ainsi que l’ISO officielle des pilotes VirtIO. Installez une version choisie et prise en charge, chargez les pilotes disque/réseau, vérifiez l’agent et le réseau après redémarrage, retirez les médias et restaurez une sauvegarde incluant EFI et TPM.

## Ce que les tests observent

- La configuration réelle comprend EFI, TPM 2.0, disque/réseau VirtIO et aucun média d’installation.
- Après redémarrage, l’agent invité rapporte une interface/adresse réseau active.
- Une restauration réelle conserve les périphériques EFI et TPM.

Les tests inspectent l’état réel de Proxmox/de l’invité. Ils ne notent ni l’historique des commandes ni une déclaration non vérifiée. Un prérequis absent est signalé comme bloquant, jamais comme une réussite.
