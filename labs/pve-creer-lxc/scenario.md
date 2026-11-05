# A light service, in a container that does not overflow

A team wants to host a small web service, and a whole VM would be too heavy
for it. An LXC container is enough, on three conditions: it stays
**unprivileged**, its **resources are bounded** so it does not bother its
neighbours, and the service does **not run as root**.

The lab manifest, in `/opt/lab-proxmox/pve-creer-lxc/manifeste.md`, gives the
CTID, the template already downloaded and verified, the address, the limits
and the page to serve.

## Mission

1. Create container 170 from the manifest's Debian 13 template, unprivileged,
   with 1 core, 512 MB of RAM and no swap, on `vmbr0` with the manifest's
   address.
2. In the container, install `python3`, create the system user `web`, and
   serve the witness page on port 8080 as that user.
3. Make the service restart with the container.

## Graded requirements

1. Configure container 170 property hostname as ct-web.
2. Configure container 170 property unprivileged as 1.
3. Configure container 170 property memory as 512.
4. Configure container 170 property swap as 0.
5. Configure container 170 property cores as 1.
6. Create the container root filesystem on local storage.
7. Configure container net0 property bridge as vmbr0.
8. Configure container net0 property ip as 10.10.113.170/24.
9. Configure container net0 property gw as 10.10.113.1.
10. Configure container DNS as 10.10.113.1.
11. Keep container 170 running.
12. Map container UID 0 to an unprivileged host UID of at least 100000.
13. Run Debian 13 inside the container.
14. Install an executable python3 inside the container.
15. Create web as a non-root system account with an UID below UID_MIN.
16. Serve the exact session witness line at the address and port given by the manifest, reachable from the node.
17. Run the process actually listening on container port 8080 as web.
18. Enforce cgroup memory.max as 536870912.
19. Enforce cgroup memory.swap.max as 0.
20. Restrict the effective container CPU set to exactly one CPU.
21. Preserve a file through a clean container stop and start; the evaluator creates and removes this measurement file.
22. Have the container witness service return without intervention after a clean stop and start.

Persistence checks perform a clean stop and start and observe both states. Unreadable measurements fail. Preservation checks only count once the report exists, the network is repaired or the agent answers, depending on the lab.

## Starting over

`dsoxlab clean pve-creer-lxc` destroys container 170. The node and the
template stay in place.

To check page origin, the evaluator temporarily disables the guest virtual interface, observes that the service becomes unreachable, then restores the interface. It does not change the node management interface.
