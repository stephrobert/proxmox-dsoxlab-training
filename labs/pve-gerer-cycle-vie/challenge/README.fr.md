# Ce qui est attendu

Agrandir une VM, préparer un retour local et vérifier la persistance des changements utiles.

# Ce qui est prouvé

- **La capacité supplémentaire est utilisable par l’invité.** — Comparer configuration PVE, partition/volume et filesystem ; écrire dans la nouvelle capacité de façon bornée.
- **Les limites CPU et mémoire restent conformes.** — Mesurer les allocations effectives et vérifier que la réserve de l’hôte est conservée.
- **Le retour au snapshot restaure exactement son périmètre.** — Modifier séparément un fichier interne et une dépendance externe ; vérifier le résultat et l’explication de la limite.
- **Le démarrage automatique respecte la configuration attendue.** — Redémarrer le nœud jetable puis contrôler ordre ou dépendances déclarées et réponse du service.

Les critères nécessitant une observation humaine doivent être revus séparément avant attestation.
