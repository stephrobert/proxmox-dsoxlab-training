# What is expected

Sauvegarder une instance puis retrouver ses données et son service dans une restauration isolée.

# What is proven

- **Une sauvegarde complète du périmètre demandé existe.** — Inspecter le job et son manifeste ; vérifier que les volumes attendus sont inclus.
- **La restauration ne dépend plus du disque source.** — Rendre la source inaccessible dans le lab et restaurer sur une nouvelle VMID à partir de l’archive.
- **Les données restaurées sont correctes et servies.** — Vérifier le nonce antérieur au backup et une opération applicative depuis le client isolé.
- **La restauration ne crée pas de doublon sur le réseau d’origine.** — Observer les adresses et le trafic des deux segments ; la sentinelle d’origine doit rester intacte.

Criteria requiring human observation need a separate review before attestation.
