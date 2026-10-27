# Install Proxmox, then have your installation graded

You are handed a **bare Debian 13 machine**. No Proxmox on it, and that is the
point: you do not learn to install a hypervisor by receiving one installed.

Your job is to install **Proxmox VE 9** on it, then have the result graded. The
lab does not look at the commands you typed, it measures the **state of the
machine**. Reach the right state by another path than the guide's, and you have
succeeded.

## What is graded

Nine items, taken from the specification published in the installation guide.
You will find them on the machine, in
`/opt/lab-proxmox/cahier-des-charges.md`.

| # | Item | How it is checked |
|---|------|-------------------|
| 1 | Proxmox VE 9 is installed | `pveversion` answers, and reports a version 9 |
| 2 | The base is Debian 13 | the codename is `trixie` |
| 3 | Services are running | `pve-cluster`, `pvedaemon` and `pveproxy` are active |
| 4 | The web interface listens | port 8006 is held by `pveproxy` |
| 5 | The bridge exists | `vmbr0` is present and carries the server address |
| 6 | Nested virtualization reaches it | `/dev/kvm` exists, the CPU exposes `vmx` or `svm` |
| 7 | Sizing is respected | 4 vCPUs and 6 GB of memory |
| 8 | The second disk is there, **and raw** | a disk of at least 20 GB, with no partition and no filesystem |
| 9 | Updates are possible | the `pve-no-subscription` repository is configured, `apt-get update` succeeds |

## Two costly traps

**The second disk must stay raw.** It is tempting to fold it into a volume or a
pool right away. Do not: the storage labs that follow will build their own ZFS
or LVM-thin pool on it, and they need a pristine disk. The test rejects a disk
that already carries a partition or a filesystem signature.

**The address must live on the bridge, not on the network card.** A Proxmox
installed on top of Debian keeps its address on the physical card until you do
something about it. You must create the `vmbr0` bridge, give it the address,
and set the physical card to `manual` as a port of that bridge. This bridge is
how your future virtual machines will reach the network.

## A third trap, quieter

**Hostname resolution** must return a routable address. If
`hostname --ip-address` answers `127.0.1.1`, the `pve-cluster` service will not
start, and the installation fails with a message that hides its own cause:

```text
ipcc_send_rec[1] failed: Connection refused
```

So check your `/etc/hosts` **before** installing the packages.

## How to proceed

The guide describes the path, under "Quelle méthode d'installation choisir dans
une VM":
<https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/installation/>

Proxmox's own procedure for the Debian path is on their wiki:
<https://pve.proxmox.com/wiki/Install_Proxmox_VE_on_Debian_13_Trixie>

One ordering detail people skip: install the Proxmox **kernel** first, **reboot
onto it**, and only then install the Proxmox packages. Installing both in a row
leaves the machine on the Debian kernel.

## Have your work graded

```bash
dsoxlab check verifier-son-installation
```

Every failing item is named, with what to fix. A failure is not the end: fix it,
then run the grading again as many times as you need.

## Starting over

`dsoxlab clean` removes the brief but **does not uninstall Proxmox**: tearing
Proxmox out of a Debian does not give back a bare Debian, it gives back a
damaged one. To truly start from scratch, destroy the machine and provision it
again.
