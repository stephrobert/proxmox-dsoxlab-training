# Mission

État initial : PBS secondaire réellement séparé dans le modèle, PVE de reprise
vierge, coffre de secours et journal extérieurs. VM primaire 9371 nommée
`n3-pve-reprendre-hors-site-9371` ; snapshot secondaire et stockage de reprise
`n3-offsite` explicitement attribués. Ces hôtes indépendants sont absents actuellement.

1. Annoncer RPO/RTO et snapshot exact. Lire synchronisations terminées et vrai
   manifeste sur le secondaire PBS.
2. Depuis le contrôleur extérieur, bloquer réseaux/stockages primaires pendant
   toute la recette. Observer accès tentés/établis, pas seulement l’intention.
3. Utiliser les seules clés du coffre indépendant sans en afficher le contenu.
   Restaurer sur cible vierge depuis le seul PBS secondaire.
4. Exercer transactions externes et comparer séquence/marqueur retrouvés,
   écritures acquittées et horodatages panne/disponibilité.
5. Séparer écrivains primaire/restauré durant le retour contrôlé.

Seuls hôtes, stockages, réseaux et ID attribués peuvent changer. Conserver
observations, masquer secrets mais pas identités, maintenir TLS/SSH et secours.
Ni votes/fencing contournés ni durabilité réduite. Expliciter la séparation
physique non testée : une topologie nested ne prouve pas la tolérance à perte
physique de site. Les recettes équivalentes sûres sont admises.
