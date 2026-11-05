# Défi : Maîtriser état, dérive et changements destructeurs

Importez la VM existante sans la recréer, enregistrez un plan après une dérive contrôlée de sa configuration réelle, puis corrigez la configuration déclarée. Conservez un plan sûr qui ne détruit ni ne remplace la VM et montrez que l’état final converge avec la VM réelle.

## Ce que les tests observent

- L’état Terraform identifie exactement le VMID préexistant.
- Le plan de dérive constate un changement réel sans action de suppression.
- La configuration réelle finale correspond à l’état et le plan sûr ne prévoit aucun remplacement.

Les tests inspectent l’état réel de Proxmox/de l’invité. Ils ne notent ni l’historique des commandes ni une déclaration non vérifiée. Un prérequis absent est signalé comme bloquant, jamais comme une réussite.
