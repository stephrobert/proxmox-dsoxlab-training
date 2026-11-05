# Défi : Piloter l’API et attendre les résultats réels

Écrivez et exécutez un petit client API qui démarre une fois la VM préparée, suit l’UPID renvoyé jusqu’à son état final avec un polling borné, puis reprend le suivi de cette même tâche après une expiration cliente. Le jeton ne doit apparaître ni dans les rapports ni dans les journaux.

## Ce que les tests observent

- L’UPID rapporté correspond à une vraie tâche Proxmox terminée pour la VM cible.
- La VM est réellement en marche et une seule VM porte l’identité du lab.
- Le rapport et les journaux du client ne contiennent pas le secret API.

Les tests inspectent l’état réel de Proxmox/de l’invité. Ils ne notent ni l’historique des commandes ni une déclaration non vérifiée. Un prérequis absent est signalé comme bloquant, jamais comme une réussite.
