# pve-restaurer-premiere-instance

Sauvegarder une instance puis retrouver ses données et son service dans une restauration isolée.

Read [`scenario.md`](./scenario.md) before starting.

```bash
dsoxlab run pve-restaurer-premiere-instance
dsoxlab challenge pve-restaurer-premiere-instance
dsoxlab check pve-restaurer-premiere-instance
```

Only use resources named in this lab's manifest. Cluster nodes are never provisioned implicitly. Automated success alone does not attest criteria requiring human observation.

Setup reserves VMIDs 198 and 199 and prepares the source witness VM and verified Debian image. It requires an instructor-provided isolated restore bridge through `pve_restore_bridge`; it does not create external networks.
