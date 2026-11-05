# Allocation and recovery recipe

Independent-controller `challenge/work/config.json`: exact three `hosts`,
`guest_ids=[9371]`, `sources` containing **distinct independent catalog hosts**
for `pbs_secondary`, `recovery`, `vault`, `console_verified=true`,
`nested_only=true`, `allow_failure="pve-reprendre-hors-site"`,
`backup_snapshot="vm/9371/<UTC timestamp>"`, `rto_seconds`, `rpo_transactions`,
`guest_network` within `10.10.113.0/24`, durable `marker`,
`service_url="https://<primary-guest>/api/lab/pve-reprendre-hors-site"`,
`recovery_url="https://<restored-guest>/api/lab/pve-reprendre-hors-site"`.
There are **no such independent hosts in the current catalog**. Placeholders
must not be reused cluster nodes; setup stops before any action.

Both guest APIs GET durable `{"sequence":123,"marker":"..."}` and POST append
durably. Trusted TLS required. SSH uses verified dsoxlab inventory or
`N3_SSH_CONFIG`, known keys, noninteractive sudo, controller outside targets.
Secondary credentials/fingerprint must already be protected on recovery host;
the PBS client must address only secondary repository. Rescue key lives at
`/var/lib/lab-proxmox/pve-reprendre-hors-site/recovery-key.json` on the vault,
never print it or record credentials. Instructor qualifies secure delivery
to the empty recovery host and records key identity without key contents.

```bash
python3 tools/controller.py probe --duration 30
python3 tools/controller.py fail --action primary-site --hosts <allocated-recovery-host> --duration 120
python3 tools/controller.py restore
```

Perform restoration in another terminal **inside** the imposed window.
The controller arms rollback before creating its own nft table on recovery,
blocking only exact primary cluster addresses (and declared primary PBS when
present). Never flush global firewall or block rescue/controller/vault/secondary.
Capture restored guest data while primary routes remain blocked. One active
action, 10–120 seconds, 1–180-second probes; if the qualified recovery needs
longer than this bound, stop and redesign the fixture rather than remove guards.
`restore` is emergency rollback. Incomplete SSH return retains evidence/lock;
use the independent console to remove only the owned `n3_recovery` table.

Write `challenge/work/report.md` for all `contract.json` criteria: secondary
sync UPID and manifest, rescue-key identity, primary deny counters/connections,
empty target and restored guest identity, data hashes/sequences, failure and
availability timestamps, RPO/RTO objectives/results, physical separation limits
and controlled return. Checks read raw secondary tasks/manifest, recovery
process/resources, firewall/connections and durable external data. Human review
verifies key-only recovery and all primary dependencies throughout the interval.
Archive evidence; cleanup restores owned isolation/removes controller evidence
only, never deletes backups, recovered guest or secrets. Keep the primary and
recovery networks segregated until the approved sole-writer return procedure.

## Hints

1. Read the manifest from secondary, not the successful primary backup task.
2. DNS, authentication, encryption keys and disks can all retain primary dependencies.
3. A restored file is not a recovered service; RPO/RTO need acknowledged sequences
   and external availability timestamps, not configured schedules.
