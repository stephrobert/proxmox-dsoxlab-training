# pve-reconcilier-etat

Importez la VM existante sans la recréer, enregistrez un plan après une dérive contrôlée de sa configuration réelle, puis corrigez la configuration déclarée. Conservez un plan sûr qui ne détruit ni ne remplace la VM et montrez que l’état final converge avec la VM réelle.

**Prérequis / conditions de blocage :** Crée uniquement la VM arrêtée 1738 et enregistre l’empreinte de sa configuration initiale. N’appliquez aucun plan contenant delete/replace ; les fichiers d’état et de plan doivent rester privés.

```bash
dsoxlab run pve-reconcilier-etat
dsoxlab check pve-reconcilier-etat
dsoxlab clean pve-reconcilier-etat
```

Le nettoyage est limité aux VMID, à la balise et aux objets dédiés déclarés pour ce lab. Il ne supprime ni template, ni charge source, ni stockage partagé, ni nœud du cluster.
