# Mission et état initial

Cluster sain à trois nœuds, serveur NFS de lab séparé, volume/exports dédiés,
invité 9311 nommé `n3-pve-qualifier-stockage-partage-9311` avec service métier
durable. Stockage `n3-shared` : l’indicateur shared ne constitue pas une preuve.

1. Vérifier l’identité réelle serveur/export de chaque montage NFS. Écrire un
   nonce contrôlé sur le volume attribué depuis un nœud ; lire et comparer ses
   empreintes depuis les autres.
2. Exercer une écriture autorisée et un vrai refus sur un export de lab hors
   périmètre. Ne pas explorer d’exports de production ni modifier globalement NFS.
3. Depuis le contrôleur indépendant, arrêter uniquement le service NFS dédié.
   Observer I/O réelles et service métier externe, pas seulement les interfaces PVE.
4. Rétablir le serveur, relire empreintes, exercer des transactions et vérifier
   l’absence de montages doublés ou réorientés.

Limiter les actions aux hôtes, réseaux, invités et volumes attribués. Conserver
les observations initiales, masquer secrets mais pas identités. Une configuration
équivalente est admise. Garder SSH/TLS vérifiés et secours. Distinguer panne de
stockage et HA : quorum sain ne rend pas un serveur NFS indisponible hautement
disponible. Rapporter domaines virtuels/physiques et limites du retour/nettoyage.
