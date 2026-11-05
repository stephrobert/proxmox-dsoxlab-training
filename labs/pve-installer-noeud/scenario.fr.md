# Installer Proxmox et établir un accès fiable

## Mission

Installer réellement un nœud depuis une ISO contrôlée et le remettre à un collègue avec un accès vérifié.

## État initial

- VM externe vide ou serveur de lab réservé
- Console extérieure et ISO référencée
- Plan d’adressage validé

## Contraintes

- N’agir que sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une configuration différente du corrigé est acceptée si elle respecte les contraintes et produit toutes les preuves.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Le stockage et les ressources sacrifiables sont identifiés avant exécution ; refuser le scénario si la borne de sécurité n’est pas démontrée.

## Critères d'acceptation

- **L’installation a été réalisée sur le support prévu.** — Conserver la provenance ISO et contrôler les disques, le système démarré et le journal d’installation ; une image préinstallée ne valide pas ce geste.
- **Le client atteint le bon nœud avec une confiance TLS explicitée.** — Comparer certificat ou CA par canal indépendant, puis vérifier API et nom attendu ; un certificat substitué doit être rejeté.
- **Versions, dépôts, temps et résolution sont cohérents.** — Lire les configurations effectives et exécuter les contrôles sans modifier une source inconnue ; signaler les écarts de version.
- **L’accès et le stockage restent fonctionnels après reboot.** — Redémarrer le nœud installé, vérifier depuis le client et contrôler le volume destiné aux invités.

Les tests automatisés prouvent uniquement l'état observable du système. Les étapes nécessitant une observation humaine (provenance ISO, accès console ou panne imposée) doivent être revues séparément avant toute attestation.
