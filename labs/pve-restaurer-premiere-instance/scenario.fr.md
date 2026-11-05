# Sauvegarder et restaurer une première instance

## Mission

Sauvegarder une instance puis retrouver ses données et son service dans une restauration isolée.

## État initial

- VM source 198 avec marqueur injecté
- Stockage de sauvegarde distinct du volume source
- Bridge de restauration isolé fourni par l'instructeur (`pve_restore_bridge`)

## Contraintes

- N’agir que sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une configuration différente du corrigé est acceptée si elle respecte les contraintes et produit toutes les preuves.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.

## Critères d'acceptation

- **Une sauvegarde complète de la VM source existe.** — Inspecter le job et son manifeste ; vérifier que les volumes attendus sont inclus.
- **La restauration ne dépend plus du disque source.** — Rendre la source inaccessible dans le lab et restaurer sur une nouvelle VMID à partir de l’archive.
- **Les données restaurées sont correctes et servies.** — Vérifier le nonce antérieur au backup et une opération applicative depuis le client isolé.
- **La restauration ne crée pas de doublon sur le réseau d’origine.** — Observer les adresses et le trafic des deux segments ; la sentinelle d’origine doit rester intacte.

Les tests automatisés prouvent uniquement l'état observable du système. Les étapes nécessitant une observation humaine (provenance ISO, accès console ou panne imposée) doivent être revues séparément avant toute attestation.
