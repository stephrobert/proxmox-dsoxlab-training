# pve-creer-lxc

Create container 170 from the supplied Debian 13 template and run its HTTP witness service under web.

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

To check page origin, the evaluator temporarily disables the guest virtual interface, observes that the service becomes unreachable, then restores the interface. It does not change the node management interface.
