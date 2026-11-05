# Défi : Migrer une charge VMware avec une recette de bascule

Importez un export VMware autorisé dans le réseau isolé du lab, inventorie tous les disques et dépendances, validez l’invité au-delà du démarrage, puis ne basculez qu’après l’arrêt de la source. Vérifiez l’état source par l’API VMware et préservez un point de retour pour les écritures.

## Ce que les tests observent

- La VM importée dans PVE possède tous les disques déclarés, démarre et rapporte une interface réseau active par l’agent invité.
- La VM source VMware est réellement arrêtée à la bascule ; aucune charge active en double n’existe.
- Un instantané/export de retour existe avant toute acceptation d’écritures post-bascule.

Les tests inspectent l’état réel de Proxmox/de l’invité. Ils ne notent ni l’historique des commandes ni une déclaration non vérifiée. Un prérequis absent est signalé comme bloquant, jamais comme une réussite.
