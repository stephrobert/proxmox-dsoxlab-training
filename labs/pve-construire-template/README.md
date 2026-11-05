# pve-construire-template

Produire un template versionné et deux clones distincts utilisables sans configuration manuelle après démarrage.

Read [`scenario.md`](./scenario.md) before starting.

```bash
dsoxlab run pve-construire-template
dsoxlab challenge pve-construire-template
dsoxlab check pve-construire-template
```

Only use resources named in this lab's manifest. Cluster nodes are never provisioned implicitly. Automated success alone does not attest criteria requiring human observation.

Setup reserves VMIDs 197–199, verifies the Debian 13 image, and generates two separate Ed25519 keys under `/opt/lab-proxmox/pve-construire-template/keys`. Private keys stay on the node and must not appear in evidence.
