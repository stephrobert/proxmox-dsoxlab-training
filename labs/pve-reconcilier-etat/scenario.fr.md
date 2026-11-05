# Mission : Maîtriser état, dérive et changements destructeurs

Importez la VM existante sans la recréer, enregistrez un plan après une dérive contrôlée de sa configuration réelle, puis corrigez la configuration déclarée. Conservez un plan sûr qui ne détruit ni ne remplace la VM et montrez que l’état final converge avec la VM réelle.

## Critères d’acceptation

1. L’état Terraform identifie exactement le VMID préexistant.
2. Le plan de dérive constate un changement réel sans action de suppression.
3. La configuration réelle finale correspond à l’état et le plan sûr ne prévoit aucun remplacement.

## Prérequis

Crée uniquement la VM arrêtée 1738 et enregistre l’empreinte de sa configuration initiale. N’appliquez aucun plan contenant delete/replace ; les fichiers d’état et de plan doivent rester privés.

Ce scénario n’installe pas PVE, ne provisionne aucun hôte et n’installe aucune fonctionnalité.
