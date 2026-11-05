# pve-epreuve-deploiement

À partir d’un nœud vide installé par vos soins, livrer une VM et un CT Linux répondant au cahier des charges, puis restaurer les données du service dans une nouvelle instance.

Read [`scenario.md`](./scenario.md) before starting.

```bash
dsoxlab run pve-epreuve-deploiement
dsoxlab challenge pve-epreuve-deploiement
dsoxlab check pve-epreuve-deploiement
```

Only use resources named in this lab's manifest. Cluster nodes are never provisioned implicitly. Automated success alone does not attest criteria requiring human observation.

Setup does not install Proxmox or create guests. It requires an already-installed node, a verified Debian 13 CT template via `pve_deployment_ct_template`, and an isolated restore bridge via `pve_deployment_restore_bridge`. VMIDs 198/200 and CTID 201 must be free.
