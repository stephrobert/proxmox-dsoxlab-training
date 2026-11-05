# Assessment allocation and evidence interface

Instructor creates independent-controller `challenge/work/config.json` with
exact three `hosts`, `guest_ids=[9381]`, distinct independent catalog `sources`
for `pbs_primary`, `pbs_secondary`, `recovery`, `vault`,
`console_verified=true`, `nested_only=true`,
`allow_failure="pve-epreuve-disponibilite"`, `source`, `destination`,
`maintenance_node` among exact cluster hosts, justified `budget` with
`host_overhead_bytes`, `recovery_bytes`, `disk_reserve_bytes`,
`backup_snapshot="vm/9381/<UTC timestamp>"`, announced `rto_seconds`,
`rpo_transactions`, `guest_network` within `10.10.113.0/24`, durable `marker`,
`service_url="https://<primary-guest>/api/lab/pve-epreuve-disponibilite"`,
`recovery_url="https://<restored-guest>/api/lab/pve-epreuve-disponibilite"`.
**Independent source roles are absent in this catalog.** Setup refuses them;
never reuse a cluster node or accept a fabricated undeclared endpoint.

GET business APIs return durable `{"sequence":123,"marker":"..."}`; POST append
returns durable acknowledgment. Trusted TLS, known SSH keys, noninteractive sudo,
dsoxlab SSH inventory or `N3_SSH_CONFIG`, verified independent rescue console.
Rescue keys/secondary credentials must be delivered securely without printing
contents; primary credentials must not become a recovery dependency.
The recovery target is initially empty. Only assigned guest/storage IDs may be used.

Controller interface (from this lab directory):

```text
python3 tools/controller.py snapshot --phase <phase>
python3 tools/controller.py probe --duration <1..180>
python3 tools/controller.py fail --action <action> --hosts <allocated-hosts> --duration <10..120>
python3 tools/controller.py restore
```

Relevant observations: `qualified`, `replicated`, `load`, `failover`,
`preflight-rejected`, `maintenance`, `reintegrated`, `restored`.
Controller actions: one-node partition, loss of majority, replication-link,
primary-site isolation on the independent recovery target. Each arms rollback
first and refuses concurrent action. Rescue is `restore`; failed SSH recovery
retains lock/evidence, requiring the independent console and only owned
Corosync/nft restoration. Do not flush firewall, lower votes or bypass fencing.
Recovery must occur while primary dependencies remain blocked, with no second writer.
If the qualified recipe cannot fit the declared bound, abort and recalibrate
before assessment rather than remove guardrails.

Write `challenge/work/report.md` and retain raw `challenge/work/evidence` for
all five `contract.json` criteria. Include configured and measured identities,
storage semantics/N-1 reserve, HA/watchdog/fencing and disk/process ownership,
external transaction timeline and exact recovered data, replication/backup
distinction, maintenance/rejection tasks, secondary manifest, key identity,
primary access denial, RPO/RTO evidence and untested physical domains.
Machine checks read actual state, tasks, durable data and controller receipts.
Human assessment verifies fencing, complete dependency independence, physical
limits and runbooks. Archive before cleanup; cleanup restores only owned actions
and removes controller evidence, not instructor guests/storage/backups/secrets.
Return primary/recovery to one writer through the agreed segregated-network runbook.

## Assistance policy

No progressive hints or solution during this assessment, as required by the
authoritative catalog. Agree authorized documentation before starting.
Reference solutions are instructor-only, outside the learner lab.
