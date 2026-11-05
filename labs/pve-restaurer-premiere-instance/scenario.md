# Sauvegarder et restaurer une première instance

## Mission

Sauvegarder une instance puis retrouver ses données et son service dans une restauration isolée.

## Starting state

- Source VM 198 with an injected witness marker
- Backup storage distinct from the source volume
- Instructor-provided isolated restore bridge (`pve_restore_bridge`)

## Constraints

- N’agir que sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une configuration différente du corrigé est acceptée si elle respecte les contraintes et produit toutes les preuves.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.

## Acceptance criteria

- **A complete backup of the source VM exists.** — Inspect the job and manifest; verify that expected volumes are included.
- **La restauration ne dépend plus du disque source.** — Rendre la source inaccessible dans le lab et restaurer sur une nouvelle VMID à partir de l’archive.
- **Les données restaurées sont correctes et servies.** — Vérifier le nonce antérieur au backup et une opération applicative depuis le client isolé.
- **La restauration ne crée pas de doublon sur le réseau d’origine.** — Observer les adresses et le trafic des deux segments ; la sentinelle d’origine doit rester intacte.

Automated checks prove only observable system state. Human-observed steps (for example ISO provenance, console access, or imposed outages) require their own recorded review before attestation.
