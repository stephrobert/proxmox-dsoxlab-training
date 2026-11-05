# Défi : Provisionner avec Terraform et des droits mesurés

Reprenez la VM préparée dans un projet Terraform explicite avec le provider bpg épinglé et une identité API à privilèges minimaux. Enregistrez un vrai plan et un état. Après application de la seule configuration prévue, planifiez à nouveau : prouvez que la configuration réelle de la VM correspond et que le second plan sauvegardé ne propose aucun changement.

## Ce que les tests observent

- L’état Terraform contient exactement le VMID préparé, pas une ressource au nom voisin.
- Le plan sauvegardé ne supprime ni ne remplace cette VM.
- La configuration Proxmox réelle respecte les cœurs, la mémoire et le pont déclarés ; le plan final sauvegardé est vide.

Les tests inspectent l’état réel de Proxmox/de l’invité. Ils ne notent ni l’historique des commandes ni une déclaration non vérifiée. Un prérequis absent est signalé comme bloquant, jamais comme une réussite.
