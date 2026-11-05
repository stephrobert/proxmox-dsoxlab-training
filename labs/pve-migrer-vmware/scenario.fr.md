# Mission : Migrer une charge VMware avec une recette de bascule

Importez un export VMware autorisé dans le réseau isolé du lab, inventorie tous les disques et dépendances, validez l’invité au-delà du démarrage, puis ne basculez qu’après l’arrêt de la source. Vérifiez l’état source par l’API VMware et préservez un point de retour pour les écritures.

## Critères d’acceptation

1. La VM importée dans PVE possède tous les disques déclarés, démarre et rapporte une interface réseau active par l’agent invité.
2. La VM source VMware est réellement arrêtée à la bascule ; aucune charge active en double n’existe.
3. Un instantané/export de retour existe avant toute acceptation d’écritures post-bascule.

## Prérequis

BLOQUÉ sans OVA/OVF autorisé dans /opt/lab-proxmox/import/source.ova et identifiants govc protégés pour vérifier l’état source. Le setup et le nettoyage n’éteignent jamais la source.

Ce scénario n’installe pas PVE, ne provisionne aucun hôte et n’installe aucune fonctionnalité.
