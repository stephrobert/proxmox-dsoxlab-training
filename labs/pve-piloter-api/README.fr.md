# pve-piloter-api

Écrivez et exécutez un petit client API qui démarre une fois la VM préparée, suit l’UPID renvoyé jusqu’à son état final avec un polling borné, puis reprend le suivi de cette même tâche après une expiration cliente. Le jeton ne doit apparaître ni dans les rapports ni dans les journaux.

**Prérequis / conditions de blocage :** Crée uniquement la VM arrêtée 1736 avec un disque vide de 1 Gio. Créez vous-même un jeton API à privilèges minimaux limité à /vms/1736 ; gardez son secret dans un fichier root uniquement, jamais dans le projet Terraform ou une sortie.

```bash
dsoxlab run pve-piloter-api
dsoxlab check pve-piloter-api
dsoxlab clean pve-piloter-api
```

Le nettoyage est limité aux VMID, à la balise et aux objets dédiés déclarés pour ce lab. Il ne supprime ni template, ni charge source, ni stockage partagé, ni nœud du cluster.
