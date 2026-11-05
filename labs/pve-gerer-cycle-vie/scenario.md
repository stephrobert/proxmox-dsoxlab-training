# Gérer ressources, disques et retours locaux

## Mission

Agrandir une VM, préparer un retour local et vérifier la persistance des changements utiles.

## Starting state

- Witness VM 195 running with a 4 GiB disk and 1 GiB memory
- Disque et mémoire avec marge autorisée
- Petite application avec données contrôlées

## Constraints

- N’agir que sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une configuration différente du corrigé est acceptée si elle respecte les contraintes et produit toutes les preuves.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.

## Acceptance criteria

- **La capacité supplémentaire est utilisable par l’invité.** — Comparer configuration PVE, partition/volume et filesystem ; écrire dans la nouvelle capacité de façon bornée.
- **Les limites CPU et mémoire restent conformes.** — Mesurer les allocations effectives et vérifier que la réserve de l’hôte est conservée.
- **Le retour au snapshot restaure exactement son périmètre.** — Modifier séparément un fichier interne et une dépendance externe ; vérifier le résultat et l’explication de la limite.
- **Le démarrage automatique respecte la configuration attendue.** — Redémarrer le nœud jetable puis contrôler ordre ou dépendances déclarées et réponse du service.

Automated checks prove only observable system state. Human-observed steps (for example ISO provenance, console access, or imposed outages) require their own recorded review before attestation.

Setup does not assign a CT. VM 195 is reserved for this lab, and the learner must create the `avant-changement` snapshot.
