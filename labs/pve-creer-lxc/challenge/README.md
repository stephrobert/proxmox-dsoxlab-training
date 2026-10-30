# Challenge: an unprivileged, bounded container, and a service that is not root

You work on `pve.lab`. The manifest is in
`/opt/lab-proxmox/pve-creer-lxc/manifeste.md`.

## What is expected

1. Container 170 is unprivileged and running.
2. `http://10.10.113.170:8080/` serves the witness line, and the service
   process belongs to user `web`.
3. The container has 1 core, 512 MB of RAM and no swap, and these limits are
   applied by its cgroups.
4. After a reboot of the container, a file written before is still there, and
   the page comes back on its own.

## What is proven

The tests read the container configuration, its UID map and its cgroups from
the node, query the service from the node, then reboot the container before
checking the file and the page.
