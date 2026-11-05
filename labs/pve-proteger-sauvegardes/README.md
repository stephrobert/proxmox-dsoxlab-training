# Encrypt, retain, and verify backups

**Level:** N2 · **Environment:** backup · **Estimated time:** not calibrated

## Mission

Configure encryption, retention, and verification, then prove a recovered key can restore data.

## Scope and safety

This lab targets only `PBS storage lab-pbs-n2-208; supplied VM/backups, limited identity, and offline key vault.`. It does not install Proxmox VE, create a cluster, change cluster membership, or use unassigned disks, networks, identities, or workloads. Preserve the recovery console and the node's management path. Do not expose secrets in evidence. A different configuration is acceptable if it meets the contract and produces the same observed state.

Requires an externally prepared PBS datastore, offline key vault, dated backups, and a disposable corruption fixture.

## Start

Read `scenario.md` and the manifest at `/opt/lab-proxmox/pve-proteger-sauvegardes/manifest.yml`. Run the lab setup only on the assigned PVE target. The tests inspect live PVE configuration/runtime state, never command history or self-reported evidence. Cleanup removes only the lab-owned fixtures listed in its manifest; external storage, workloads, and cluster state are not removed.
