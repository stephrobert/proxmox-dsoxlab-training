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

## What is graded

| # | What is checked | How |
|---|---|---|
| 1 | Isolation | `unprivileged: 1`, and the container root mapped to a host UID of at least 100000 |
| 2 | The service | the page read from the node carries the container marker, served by user `web` |
| 3 | The limits | the configuration AND the effective cgroups: 512 MB of memory, a single core, no swap |
| 4 | The reboot | a file written before the reboot is read back after it, and the page comes back on its own |

## Starting over

`dsoxlab clean pve-creer-lxc` destroys container 170. The node and the
template stay in place.
