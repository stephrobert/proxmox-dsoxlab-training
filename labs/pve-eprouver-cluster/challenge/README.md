# Challenge and instructor allocation

On the **independent workstation**, from this lab directory, create
`challenge/work/config.json` (never commit secrets):

```json
{
  "hosts": ["pve01.lab", "pve02.lab", "pve03.lab"],
  "guest_ids": [],
  "sources": {},
  "console_verified": true,
  "nested_only": true,
  "allow_failure": "pve-eprouver-cluster"
}
```

The instructor must actually verify those safeguards, not merely set flags.
The independent on-demand `proxmox-cluster` profile uses 8 GiB/4 vCPU per
node, with 40 GiB system and 40 GiB extra disks. Do not provision unless
explicitly requested; form the cluster manually, never as an automatic setup
or reference-solution side effect. A failure is refused if **any** unallocated
guest exists, even stopped: a node restart could otherwise start that guest.
The normal provisioned dsoxlab SSH inventory is used. Alternatively
`N3_SSH_CONFIG` names an existing OpenSSH inventory with the exact host aliases.
Known host keys and noninteractive sudo must already work. Controller checks
that none of the targets resolves to a local controller address.
Do not provision nodes as part of this exercise or disable host-key/TLS checking.

Run setup before forming the cluster. Once healthy:

```bash
python3 tools/controller.py snapshot --phase qualified
python3 tools/controller.py fail --action one-node --hosts pve03.lab --duration 120
python3 tools/controller.py fail --action no-majority --hosts pve02.lab pve03.lab --duration 120
python3 tools/controller.py check --criterion coherence
python3 tools/controller.py restore
```

The controller stops **Corosync only** on the exact allocated nodes, arms a
bounded recovery timer before each stop, measures raw votes and pmxcfs refusal,
then restores in `finally`. This is a membership-partition experiment, not a
physical power-loss claim. HA watchdog may reset a disposable nested node;
do not use production hosts. Failure duration must be 10–120 seconds.
The emergency command is `restore`; if SSH recovery fails, use the independent
console to start Corosync on only the affected allocated hosts. Evidence/lock
is retained on incomplete recovery; never erase it to hide the failure.
Only one controller action/maintenance can be active at a time.

Optional independent virtual-power control: set `failure_mode="power"` and
`domains={"pve01.lab":"<UUID>","pve02.lab":"<UUID>","pve03.lab":"<UUID>"}`.
Each exact UUID must be verified through local `qemu:///system` guest-agent
addresses against its allocated SSH node IP during setup. No guessed domain
name or external URI is accepted. The controller arms its **local** start timer
before `virsh destroy`, observes actual shut-off state and starts only that UUID
on return. Missing libvirt/guest-agent identity is an explicit precondition error.
This measures virtual power loss only, not a physical-server outage.

Write `challenge/work/report.md`: allocation, topology, before/during/after
observations, each criterion from `contract.json`, refusal/task diagnostics,
failure domains, limits and precise return/cleanup procedure. Human review
must check the network isolation and absence of vote/lock bypasses. Machine
checks compare live members, votes, versions, configuration hashes and real
failure receipts, not prose assertions. Evidence is in `challenge/work/evidence`.
Archive it before cleanup. Cleanup preserves all instructor resources and the
allocation file; it only restores owned actions and deletes owned evidence.

## Progressive hints

1. Observe each survivor, not just a responding UI.
2. Compare expected votes, online members and writable pmxcfs state.
3. A responsive node without a majority cannot authorize cluster writes.
   Recovery must converge to one distributed configuration, not just three pings.
