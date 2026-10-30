# Challenge: a Proxmox VE you installed yourself

You work on `pve.lab`, a bare Debian 13. The full specification is on the
machine, in `/opt/lab-proxmox/cahier-des-charges.md`.

## What is expected

1. Proxmox VE is installed, version 9 or later, and `pveversion` answers.
2. The `pve-cluster`, `pvedaemon` and `pveproxy` services are active, and the
   web interface answers on port 8006.
3. The `vmbr0` bridge exists and carries the server's IPv4 address.
4. The `pve-no-subscription` repository is configured, and `apt-get update`
   succeeds.

## What is proven

The tests query the machine: the installed version, the services, the port that
answers, the address carried by the bridge and the real result of `apt-get
update`. They do not read the commands you typed, and every failing item is
named along with what to fix.
