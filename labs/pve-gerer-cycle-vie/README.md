# pve-gerer-cycle-vie

Agrandir une VM, préparer un retour local et vérifier la persistance des changements utiles.

Read [`scenario.md`](./scenario.md) before starting.

```bash
dsoxlab run pve-gerer-cycle-vie
dsoxlab challenge pve-gerer-cycle-vie
dsoxlab check pve-gerer-cycle-vie
```

Only use resources named in this lab's manifest. Cluster nodes are never provisioned implicitly. Automated success alone does not attest criteria requiring human observation.

Setup provides only witness VM 195; it does not assign a CT. The learner must create the `avant-changement` snapshot.
