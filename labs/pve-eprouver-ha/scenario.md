# Mission

Initial state: qualified three-node cluster, storage and N-1 reserve, documented
watchdog profile, independent client/controller. VM 9351 must be named
`n3-pve-eprouver-ha-9351`, use dedicated `n3-ha` storage and expose durable data.

1. Inventory quorum, HA ownership, watchdog, disk identity and failure domains.
   Confirm rescue/abort controls outside the cluster before arming anything.
2. Impose an owner-node partition or qualified virtual power loss externally.
   Do not substitute orderly guest shutdown or migration for a failure.
3. Correlate fencing/watchdog chronology, QEMU processes from multiple observers,
   HA states and external transactions. Reject ambiguous/double disk writers.
4. Restore. In a separate experiment remove majority; verify real write refusal,
   unchanged expected votes and preserved durable data. Restore a healthy cluster.

Only allocated hosts, networks and VM may change. Preserve evidence before
correction; mask secrets, retain verified TLS/SSH and console. An equivalent
implementation is acceptable only if the same safety and evidence contract holds.
Nested virtual-node failure does not certify physical-server/site HA.
