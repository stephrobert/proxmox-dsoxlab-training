# Mission

État initial : cluster avec budgets explicites, deux charges à séparer,
candidate arrêtée, mesures mémoire hôtes et stockage dédié `n3-capacity`.
IDs 9331, 9332, 9333 nommés `n3-pve-reserver-capacite-<id>`.

1. Mesurer mémoire utilisée/maximale de chaque hôte, maxima invités configurés,
   surcharge hôte et disque disponible. Simuler la perte du plus gros nœud,
   pas du nœud moyen. Séparer hypothèses et mesures.
2. Configurer la règle effective de placement/anti-affinité supportée par la
   version pour les deux charges. Montrer la séparation avant/après un déplacement.
3. Présenter une candidate dépassant la réserve résiduelle de reprise.
   Refuser ou reporter explicitement ; aucun stress mémoire non borné.
4. Exercer une charge transactionnelle bornée, remesurer la marge et publier
   les limites matérielles.

Limiter les changements aux ID, stockages et réseaux attribués. Conserver
observations, SSH/TLS vérifiés, secours et secrets masqués. Variantes respectant
le contrat admises. Aucun quorum forcé ni surallocation cachée ; un budget
ne prouve pas une HA après perte physique de nœud.
