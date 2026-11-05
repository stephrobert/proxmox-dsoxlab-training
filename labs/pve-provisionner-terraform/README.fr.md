# pve-provisionner-terraform

Reprenez la VM préparée dans un projet Terraform explicite avec le provider bpg épinglé et une identité API à privilèges minimaux. Enregistrez un vrai plan et un état. Après application de la seule configuration prévue, planifiez à nouveau : prouvez que la configuration réelle de la VM correspond et que le second plan sauvegardé ne propose aucun changement.

**Prérequis / conditions de blocage :** Crée uniquement la VM arrêtée 1737. Le setup n’installe pas Terraform. Stockez les identifiants API hors du projet ; protégez les fichiers d’état et de plan, qui peuvent contenir des valeurs sensibles.

```bash
dsoxlab run pve-provisionner-terraform
dsoxlab check pve-provisionner-terraform
dsoxlab clean pve-provisionner-terraform
```

Le nettoyage est limité aux VMID, à la balise et aux objets dédiés déclarés pour ce lab. Il ne supprime ni template, ni charge source, ni stockage partagé, ni nœud du cluster.
