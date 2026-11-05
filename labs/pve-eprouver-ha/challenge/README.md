# Allocation, bounded failure and acceptance

Controller allocation `challenge/work/config.json`: exact three `hosts`,
`guest_ids=[9351]`, `sources={}`, `console_verified=true`, `nested_only=true`,
`allow_failure="pve-eprouver-ha"`, `destination="pve02.lab"`,
`guest_network="10.10.113.0/24"`,
`service_url="https://<guest>/api/lab/pve-eprouver-ha"`, durable `marker`.
GET returns JSON `{"sequence":123,"marker":"..."}`, POST append returns durable
acknowledgments. Trusted TLS, known SSH keys, noninteractive sudo and independent
rescue console are mandatory. Use dsoxlab SSH inventory or `N3_SSH_CONFIG`.
Instructor must document watchdog and qualify reserve/storage before setup.

```bash
python3 tools/controller.py probe --duration 120
python3 tools/controller.py fail --action one-node --hosts pve01.lab --duration 120
python3 tools/controller.py snapshot --phase failover
python3 tools/controller.py fail --action no-majority --hosts pve02.lab pve03.lab --duration 120
python3 tools/controller.py restore
```

Replace pve01.lab only with the **observed owner** among the exact three nodes.
Run external probe and capture `failover` in another terminal within the
imposed window when recovery is actually observed. `one-node` stops Corosync,
not the guest: a partition experiment only counts if fencing is truly observed
and ownership becomes unambiguous. No automatic claim that stopping Corosync
is itself successful HA. Independent recovery timers are armed before changes,
10–120-second failures, 1–180-second probes, one active action at a time.
`restore` is emergency rollback; if the watchdog reboots a node and SSH fails,
use the independent console, retaining the lock/evidence.

Write `challenge/work/report.md` for the four `contract.json` criteria, including
actual owner loss, watchdog/fencing logs, unique disk/process ownership,
transaction/data hashes and outage interval, negative refusal and return plan.
Machine checks require real controller receipts, multi-node QEMU observations,
durable responses and unchanged votes. Human review must confirm fencing
meaning, unavailable-node ownership and actual storage semantics.
No forced votes, lock bypasses or reduced durability. State virtual versus
physical domains; claim only measured results. Archive evidence before cleanup.
Cleanup restores only owned actions and deletes controller evidence, never
guests/storage/HA policy. Revert only this VM's policy via the approved runbook.

## Hints

1. Identify the owner and measure client transactions before failure.
2. Correlate watchdog/fencing events with QEMU and HA ownership on survivors.
3. Migration is not a failure; an unreachable owner is not automatically fenced.
   No majority must remain a refusal, not a reason to lower expected votes.
