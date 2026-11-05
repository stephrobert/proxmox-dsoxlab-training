# Mission : Piloter l’API et attendre les résultats réels

Écrivez et exécutez un petit client API qui démarre une fois la VM préparée, suit l’UPID renvoyé jusqu’à son état final avec un polling borné, puis reprend le suivi de cette même tâche après une expiration cliente. Le jeton ne doit apparaître ni dans les rapports ni dans les journaux.

## Critères d’acceptation

1. L’UPID rapporté correspond à une vraie tâche Proxmox terminée pour la VM cible.
2. La VM est réellement en marche et une seule VM porte l’identité du lab.
3. Le rapport et les journaux du client ne contiennent pas le secret API.

## Prérequis

Crée uniquement la VM arrêtée 1736 avec un disque vide de 1 Gio. Créez vous-même un jeton API à privilèges minimaux limité à /vms/1736 ; gardez son secret dans un fichier root uniquement, jamais dans le projet Terraform ou une sortie.

Ce scénario n’installe pas PVE, ne provisionne aucun hôte et n’installe aucune fonctionnalité.
