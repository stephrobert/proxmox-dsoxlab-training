# Mission : Provisionner avec Terraform et des droits mesurés

Reprenez la VM préparée dans un projet Terraform explicite avec le provider bpg épinglé et une identité API à privilèges minimaux. Enregistrez un vrai plan et un état. Après application de la seule configuration prévue, planifiez à nouveau : prouvez que la configuration réelle de la VM correspond et que le second plan sauvegardé ne propose aucun changement.

## Critères d’acceptation

1. L’état Terraform contient exactement le VMID préparé, pas une ressource au nom voisin.
2. Le plan sauvegardé ne supprime ni ne remplace cette VM.
3. La configuration Proxmox réelle respecte les cœurs, la mémoire et le pont déclarés ; le plan final sauvegardé est vide.

## Prérequis

Crée uniquement la VM arrêtée 1737. Le setup n’installe pas Terraform. Stockez les identifiants API hors du projet ; protégez les fichiers d’état et de plan, qui peuvent contenir des valeurs sensibles.

Ce scénario n’installe pas PVE, ne provisionne aucun hôte et n’installe aucune fonctionnalité.
