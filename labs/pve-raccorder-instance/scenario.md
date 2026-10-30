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

## What is graded

| # | What is checked | How |
|---|---|---|
| 1 | The topology | `net0` carries `bridge=vmbr0`, and `tap160i0` is an actual port of `vmbr0` |
| 2 | The right instance | the page read from the node contains the session nonce |
| 3 | The right layer | the VM is reachable, and the isolated bridge received no physical port |
| 4 | Persistence | after a guest reboot and an `ifreload -a` on the node, the page comes back |

## Starting over

`dsoxlab clean pve-raccorder-instance` destroys VM 160 and removes the
isolated bridge. The node stays in place.
