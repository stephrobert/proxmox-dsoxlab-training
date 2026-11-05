# Mission d’épreuve

Exploiter trois nœuds qualifiés avec réserve, démontrer le comportement du service
lors d’une panne imposée extérieurement, puis reprendre depuis un backup extérieur.
État initial : cluster/stockage qualifiés, client transactionnel extérieur,
contrôle alimentation/réseau indépendant et arrêt d’urgence, PBS primaire,
copie secondaire, cible de reprise vierge et objectifs RPO/RTO annoncés.
VM 9381 `n3-pve-epreuve-disponibilite-9381`, stockage `n3-availability`.
Les hôtes indépendants PBS/reprise/coffre ne sont pas déclarés actuellement.

Livrer configuration/allocation, preuves métier/données y compris pannes/refus,
et dossier de transmission avec limites, retour, reprise et nettoyage.
Démontrer les cinq critères de `contract.json` : architecture, bascule,
modèle de données, maintenance/refus de migration incompatible, reprise indépendante.

Ne jamais forcer quorum ni réduire durabilité. Panne réellement imposée depuis
l’extérieur ; un arrêt ordonné d’invité ne prouve aucun fencing. Limiter toutes
les actions aux ressources attribuées, préserver secours, identités SSH/TLS
et secrets. Distinguer pertes de nœud virtuel, serveur physique et site :
nested ne prouve pas les trois. **Aucune aide ni solution pendant l’épreuve.**
Convenir documents autorisés et critères d’arrêt avant démarrage. Seule l’interface
opérationnelle de preuves est fournie, pas la réponse à l’épreuve.
