# Allocation and measured migration

On the independent workstation create `challenge/work/config.json`:

```json
{
  "hosts": ["pve01.lab", "pve02.lab", "pve03.lab"],
  "guest_ids": [9321, 9322], "sources": {},
  "console_verified": true, "nested_only": true,
  "destination": "pve02.lab", "guest_network": "10.10.113.0/24",
  "service_url": "https://<vm-witness>/api/lab/pve-migrer-instance",
  "marker": "<durable instructor marker>"
}
```

The VM witness GET returns durable JSON `{"sequence":123,"marker":"..."}`;
POST `{"operation":"append","marker":"..."}` durably appends. Provide a trusted
certificate, never credentials in the URL. Also exercise and document the CT
witness and client sessions. All prepared guest names must match the scenario.
Set `ct_service_url="https://<ct-witness>/api/lab/pve-migrer-instance"` with the
same durable JSON interface. Machine checks also compare the CT's durable
sequence/marker and actual local LXC process owner after movement and restart.
The second destination is pve03.lab; document its qualification before selecting
pve02.lab. Provisioned SSH inventory or explicit `N3_SSH_CONFIG` must retain known
host keys and noninteractive sudo. The controller must be outside all target IPs.

```bash
python3 tools/controller.py snapshot --phase preflight-rejected
python3 tools/controller.py probe --duration 120
python3 tools/controller.py snapshot --phase migrated
python3 tools/controller.py snapshot --phase rebooted
```

Take `preflight-rejected` only after a real failed `qmigrate` task. Run the
bounded probe in a separate terminal while migrating the allocated VM/CT.
Take `migrated` when both are running on destination, `rebooted` after their
real stop/start tasks finish there. Probes are 1–180 seconds, SSH operations
bounded; no controller failure action is needed for a migration.
Do not bypass locks or expected votes. Preserve rescue access.

Write `challenge/work/report.md` against all four `contract.json` criteria:
dependency inventory, failed UPID/error, owner/process evidence, VM/CT data
hashes and sessions, measured interruption and restart dependencies, limits
and return/cleanup steps. Machine checks query actual task status, resource
placement, QEMU ownership, start tasks and external durable responses. Human
review covers CT-specific hashes/sessions and supported migration choices.
Archive `challenge/work/evidence` before cleanup. Cleanup removes controller
evidence only; instructor guests/disks remain. Revert only the dedicated
negative dependency and any allocated placement changes via your runbook.

## Hints

1. A migration accepted by the API can still fail as a task.
2. Check destination storage, snippets, ISO files and bridge identities separately.
3. A guest that migrated successfully can retain a source dependency until its
   next cold start; client timestamps, not a green icon, measure the interruption.
