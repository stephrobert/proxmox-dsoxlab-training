# Mission

Initial state: stable cluster, checked backups, approved change version and
independent controller/probe. VM 9361 named `n3-pve-maintenir-cluster-9361`,
dedicated storage `n3-maintenance`; inventory every running load before intervention.

1. Qualify backups and rollback. Evacuate only allocated migratable loads,
   record placement before/after and handle exceptions. Abort if an unrelated
   guest would require movement or remains on the node to be stopped.
2. Admit one maintenance at a time; prove a concurrent request is refused.
   Observe two-survivor quorum and N-1 reserve throughout the intervention.
3. Apply only the approved scoped change, return the node and verify identity,
   version compatibility, networking, storage and HA task states.
4. Execute business transaction, a new backup and a restore-marker read after
   maintenance. Do not replace restoration proof with a successful backup log.

Preserve diagnostics and secrets appropriately; allocated hosts/networks/disks
only, verified SSH/TLS and rescue console. Equivalent maintenance methods are
acceptable within the same contract. No forced votes or lock/durability bypass;
document measured service contract and virtual/physical failure limits.
