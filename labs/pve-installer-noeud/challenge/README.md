# What is expected

Installer réellement un nœud depuis une ISO contrôlée et le remettre à un collègue avec un accès vérifié.

# What is proven

- **L’installation a été réalisée sur le support prévu.** — Conserver la provenance ISO et contrôler les disques, le système démarré et le journal d’installation ; une image préinstallée ne valide pas ce geste.
- **Le client atteint le bon nœud avec une confiance TLS explicitée.** — Comparer certificat ou CA par canal indépendant, puis vérifier API et nom attendu ; un certificat substitué doit être rejeté.
- **Versions, dépôts, temps et résolution sont cohérents.** — Lire les configurations effectives et exécuter les contrôles sans modifier une source inconnue ; signaler les écarts de version.
- **L’accès et le stockage restent fonctionnels après reboot.** — Redémarrer le nœud installé, vérifier depuis le client et contrôler le volume destiné aux invités.

Criteria requiring human observation need a separate review before attestation.
