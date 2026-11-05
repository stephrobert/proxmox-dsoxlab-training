# Allocation and bounded maintenance

Independent-controller `challenge/work/config.json`: exact three `hosts`,
`guest_ids=[9361]`, `sources={}`, `console_verified=true`, `nested_only=true`,
`allow_failure="pve-maintenir-cluster"`, `maintenance_node="pve01.lab"`,
`destination="pve02.lab"`, `budget` containing justified
`host_overhead_bytes`, `recovery_bytes`, `disk_reserve_bytes`,
`guest_network="10.10.113.0/24"`,
`service_url="https://<guest>/api/lab/pve-maintenir-cluster"`, durable `marker`.
GET returns durable `{"sequence":123,"marker":"..."}`, POST append acknowledges
durable updates. Trusted TLS and known SSH keys/noninteractive sudo required,
dsoxlab inventory or explicit `N3_SSH_CONFIG`. Instructor verifies rescue,
backups and the authorized change; no generic package upgrade is performed.

```bash
python3 tools/controller.py snapshot --phase maintenance
python3 tools/controller.py probe --duration 120
python3 tools/controller.py fail --action one-node --hosts pve01.lab --duration 120
python3 tools/controller.py snapshot --phase reintegrated
python3 tools/controller.py snapshot --phase restored
python3 tools/controller.py restore
```

Take `maintenance` after evacuation, before node removal. Keep the external
probe in another terminal. The controller refuses overlapping active actions;
retain the second request's refusal. Corosync removal is the bounded approved
membership intervention, not proof of an OS upgrade or physical outage.
Do not proceed with another node maintenance. Failure windows 10–120 seconds;
probes 1–180 seconds. Independent return is armed before stop; `restore` is
emergency rollback. Failed SSH recovery retains lock/evidence for rescue console.

After return, back up only 9361 and restore it only via an explicitly allocated
scratch guest/network or a safe stopped same-ID restore; never overwrite an
unrelated ID or permit a second network writer. Capture `restored` with actual
restored business marker, not the original running guest. Document the scratch
allocation before use; this controller never auto-selects a free ID.
Write `challenge/work/report.md` for the four criteria, evacuation/exceptions,
concurrency refusal, measured reserve/quorum, approved change, identities/storage,
post-maintenance backup UPID and real restored marker, limits and rollback.
Machine tests query real placement, quorum/storage, backup tasks and durable
data. Human review verifies concurrency, scoped change and restoration identity.
Archive evidence; cleanup restores owned actions/removes evidence only, never
destroys backups or guests. Restore allocated placements through your runbook.

## Hints

1. Inventory the whole node before stopping it.
2. A second maintenance can remove the surviving majority; make the refusal explicit.
3. Successful reintegration is more than membership: storage, service and a
   marker read from a real restoration must pass again.
