# Allocation, exercise and evidence

Create `challenge/work/config.json` on the independent workstation with exact
`hosts=["pve01.lab","pve02.lab","pve03.lab"]`, `guest_ids=[9311]`,
`sources={"nfs":"<independent catalog host>"}`, `console_verified=true`,
`nested_only=true`, and `allow_failure="pve-qualifier-stockage-partage"`.
The placeholder is **not** an existing host: this catalog has no NFS source,
so setup fails before any action until that prerequisite is separately supplied.
No source may be a cluster node; no undeclared host is accepted.

Provide `service_url="https://<guest>/api/lab/pve-qualifier-stockage-partage"`,
`guest_network` as an allocated subnet within `10.10.113.0/24`, `marker` as the
durable instructor marker, and `denied_export="/n3-denied-shared"` as a dedicated
negative fixture. GET returns JSON `{"sequence":123,"marker":"..."}`; POST
`{"operation":"append","marker":"..."}` durably appends and returns that state.
Use a trusted certificate; never disable verification. Instructor resources
must be prepared and named before setup. Do not store credentials in URLs/files.
SSH uses provisioned dsoxlab inventory or existing `N3_SSH_CONFIG`, known keys,
noninteractive sudo and an independently tested rescue console.

```bash
python3 tools/controller.py snapshot --phase qualified
python3 tools/controller.py permissions
python3 tools/controller.py probe --duration 30
python3 tools/controller.py fail --action storage --hosts <allocated-nfs-host> --duration 120
python3 tools/controller.py restore
```

Before `qualified`, write the nonce at
`/mnt/pve/n3-shared/.n3-pve-qualifier-stockage-partage-nonce` from one node only.
Record allowed write and actual negative-operation output. The controller
stops only the allocated NFS service after arming its recovery timer. One action
at a time, 10–120 seconds; `restore` is emergency rollback. On incomplete SSH
recovery, use the independent console to start NFS on that source; retain the
lock/evidence. No cluster shutdown, vote forcing, durability reduction or lock bypass.
Archive `challenge/work/evidence` and write `challenge/work/report.md` with
all four criteria in `contract.json`, mount/export identities, refusal output,
I/O/client timeline, hashes, failure domains, limits and return procedure.
Tests read raw mounts/hashes, service responses and bounded failure receipts.
Human review additionally verifies permissions, negative refusal and safe mounts.
Cleanup restores owned actions and deletes controller evidence only; it never
deletes exports/volumes/guests. Remove the owned nonce explicitly after archiving.

## Hints

1. Compare the data and actual mount source, not the storage display name.
2. NFS exports, client authorization and guest content permissions are different layers.
3. Identical storage IDs can hide different disks; node reachability says nothing
   about surviving I/O when the sole NFS server is gone.
