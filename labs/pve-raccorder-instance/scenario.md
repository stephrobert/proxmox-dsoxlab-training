# A VM that runs, and that nobody reaches

Witness VM 160 was delivered yesterday. Proxmox shows it running, its service
listens on port 8080, and yet the team that must use it cannot reach it:
`http://10.10.113.160:8080/` does not answer, neither from their workstation
nor from the node.

The lab manifest, in `/opt/lab-proxmox/pve-raccorder-instance/manifeste.md`,
gives the reserved address and the lab network. The VM disk carries this
session's witness page: recreating the VM would not bring it back.

## Mission

1. From the node, find why the VM cannot be reached. Follow the path in order:
   the VM card, the bridge it is plugged into, then what that bridge connects.
2. Fix it at the right layer: the card of **this** VM must join `vmbr0`. Do
   not recreate the VM, and do not give a physical card to the isolated
   bridge.
3. Check from the node that the witness page answers.

## Graded requirements

1. Attach VM 160 net0 to exactly vmbr0.
2. Make the exact interface tap160i0 an effective port of vmbr0.
3. Serve the exact session witness line at the address and port given by the manifest, reachable from the node.
4. Keep physical interfaces out of isolated bridge vmbr9.
5. Preserve VM 160 SMBIOS identity and create no new VM 160 creation task.
6. Preserve reachability through a clean stop and start of VM 160.
7. Preserve reachability after the evaluator successfully reloads the node network.

Persistence checks perform a clean stop and start and observe both states. Unreadable measurements fail. Preservation checks only count once the report exists, the network is repaired or the agent answers, depending on the lab.

## Starting over

`dsoxlab clean pve-raccorder-instance` destroys VM 160 and removes the
isolated bridge. The node stays in place.

To check page origin, the evaluator temporarily disables the guest virtual interface, observes that the service becomes unreachable, then restores the interface. It does not change the node management interface.
