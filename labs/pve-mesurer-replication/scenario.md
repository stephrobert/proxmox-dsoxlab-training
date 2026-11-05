# Mission

Initial state: two qualified ZFS stores in the cluster, VM 9341 named
`n3-pve-mesurer-replication-9341` with a sequential durable journal, external
controller and rescue console. Allocate only storage `n3-replica` and job 9341-0.

1. Check source/target volume identities, configure the job and wait for real
   completion. Capture snapshot names/GUIDs, task status and business sequence.
2. Append more acknowledged writes. From the external controller make the
   source genuinely unavailable/fenced, recover from the target and compare
   the recovered journal with the last completed replication and acknowledged tail.
3. In a separate restored experiment, cut only source-to-target replication
   SSH traffic; observe the actual job error while leaving controller rescue SSH.
4. Follow the authorized return runbook; prove one disk owner/process before
   resuming writes. Never start a replica while the source might still write.

Preserve pre-correction observations; use allocated hosts, volumes and networks
only, verified TLS/SSH, masked secrets and independent controls. No forced votes,
lock bypass or durability weakening. Report virtual/physical domains, measured
transaction loss and the difference between replication, migration and backup.
