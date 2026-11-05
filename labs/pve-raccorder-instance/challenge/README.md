# pve-raccorder-instance

Repair the network attachment of the supplied VM 160. Keep its existing VM identity and disk; the session page alone does not establish that identity.

## Graded requirements

1. Attach VM 160 net0 to exactly vmbr0.
2. Make the exact interface tap160i0 an effective port of vmbr0.
3. Serve the exact session witness line at the address and port given by the manifest, reachable from the node.
4. Keep physical interfaces out of isolated bridge vmbr9.
5. Preserve VM 160 SMBIOS identity and create no new VM 160 creation task.
6. Preserve reachability through a clean stop and start of VM 160.
7. Preserve reachability after the evaluator successfully reloads the node network.

Persistence checks perform a clean stop and start and observe both states. Unreadable measurements fail. Preservation checks only count once the report exists, the network is repaired or the agent answers, depending on the lab.

To check page origin, the evaluator temporarily disables the guest virtual interface, observes that the service becomes unreachable, then restores the interface. It does not change the node management interface.
