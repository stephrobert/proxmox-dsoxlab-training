# verifier-son-installation

Install Proxmox VE on the bare Debian node. Debian, KVM, node sizing and the raw second disk are supplied prerequisites, not scored work.

## Graded requirements

1. Install Proxmox VE so pveversion reports pve-manager.
2. Use Proxmox VE version 9 or later.
3. Keep service pve-cluster active.
4. Keep service pvedaemon active.
5. Keep service pveproxy active.
6. Serve an HTTP 200 response over HTTPS on port 8006.
7. Make pveproxy own the listener on port 8006.
8. Place the server IPv4 address, resolved from its hostname, on vmbr0.
9. Enable a complete pve-no-subscription APT repository entry.
10. Download all APT indexes without ignoring a repository download error.

Persistence checks perform a clean stop and start and observe both states. Unreadable measurements fail. Preservation checks only count once the report exists, the network is repaired or the agent answers, depending on the lab.
