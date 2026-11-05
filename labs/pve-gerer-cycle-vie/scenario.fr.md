# Gérer ressources, disques et retours locaux

## Mission

Agrandir une VM, préparer un retour local et vérifier la persistance des changements utiles.

## État initial

- VM témoin 195 en fonctionnement, avec un disque de 4 Gio et 1 Gio de mémoire
- Disque et mémoire avec marge autorisée
- Petite application avec données contrôlées

## Contraintes

- N’agir que sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une configuration différente du corrigé est acceptée si elle respecte les contraintes et produit toutes les preuves.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.

## Critères d'acceptation

- **La capacité supplémentaire est utilisable par l’invité.** — Comparer configuration PVE, partition/volume et filesystem ; écrire dans la nouvelle capacité de façon bornée.
- **Les limites CPU et mémoire restent conformes.** — Mesurer les allocations effectives et vérifier que la réserve de l’hôte est conservée.
- **Le retour au snapshot restaure exactement son périmètre.** — Modifier séparément un fichier interne et une dépendance externe ; vérifier le résultat et l’explication de la limite.
- **Le démarrage automatique respecte la configuration attendue.** — Redémarrer le nœud jetable puis contrôler ordre ou dépendances déclarées et réponse du service.

Le setup n'attribue pas de CT à ce lab. La VM 195 est réservée au parcours, et le snapshot `avant-changement` doit être créé par l'apprenant.

Les tests automatisés prouvent uniquement l'état observable du système. Les étapes nécessitant une observation humaine (provenance ISO, accès console ou panne imposée) doivent être revues séparément avant toute attestation.
