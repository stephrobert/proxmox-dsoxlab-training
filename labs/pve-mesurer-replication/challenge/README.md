# Allocation and safe measurement

Create independent-controller `challenge/work/config.json` with exact three
`hosts`, `guest_ids=[9341]`, `sources={}`, `source="pve01.lab"`,
`destination="pve02.lab"`, `console_verified=true`, `nested_only=true`,
`allow_failure="pve-mesurer-replication"`, `guest_network="10.10.113.0/24"`,
`service_url="https://<guest>/api/lab/pve-mesurer-replication"`, `marker`.
GET witness JSON is durable `{"sequence":123,"marker":"..."}`; POST append
returns an acknowledged durable sequence. Use trusted TLS, known SSH identities
and noninteractive sudo through dsoxlab inventory or `N3_SSH_CONFIG`.
The instructor must qualify ZFS storage and independent rescue/fencing first.
For the reference RPO recipe set `failure_mode="power"` and provide all three
verified UUID mappings described in
[the cluster control instructions](../../pve-eprouver-cluster/challenge/README.md).
Those local hypervisor controls are independent, target only the allocated
nodes, and refuse an unverifiable guest-agent identity. No automatic cluster formation.

```bash
python3 tools/controller.py snapshot --phase replicated
python3 tools/controller.py probe --duration 30
python3 tools/controller.py fail --action replication-link --hosts pve01.lab --duration 120
python3 tools/controller.py fail --action one-node --hosts pve01.lab --duration 120
python3 tools/controller.py snapshot --phase source-unavailable
python3 tools/controller.py restore
```

Run each failure separately. `replication-link` uses a uniquely owned nft table
on source blocking TCP/22 only toward the exact destination, with rollback armed
first; do not change global SSH/firewall. A Corosync partition alone does **not**
fence a non-HA VM. Do not start the replica until the independent qualified
controller has observed fencing/power removal; otherwise the RPO experiment
must fail rather than risk double writers. Capture `source-unavailable` in
another terminal during the imposed window after safe recovery on target.
Failure windows 10–120 seconds, probes 1–180 seconds. `restore` is emergency
rollback; failed SSH recovery retains evidence/lock and requires the rescue console.

Write `challenge/work/report.md` for all `contract.json` criteria: job/task,
volume and snapshot identities, last-sync time, acknowledged/recovered sequence
and hashes, exact measured loss, alert, fencing, sole owner, return and limits.
Checks read raw jobs, real ZFS state, external business data and QEMU ownership;
human review verifies the journal boundary and safe return/fencing.
Archive evidence before cleanup. Cleanup removes only controller-owned rules
and evidence, never snapshots/jobs/guests. Revert only job 9341-0 and allocated
placement through the approved runbook. Never bypass quorum/fencing.

## Hints

1. Observe the last completed replication, not the next scheduled time.
2. Match source/target volumes and sequence numbers at the completed snapshot.
3. Running VM status cannot replace a replication error; a recent replica can
   still miss acknowledged writes, and return of the source can create two writers.
