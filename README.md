# Proxmox VE course: install, operate, secure and automate a type 1 hypervisor

**Language:** [English](./README.md) · [Français](./README.fr.md)

[![CI](https://github.com/stephrobert/proxmox-dsoxlab-training/actions/workflows/ci.yml/badge.svg)](https://github.com/stephrobert/proxmox-dsoxlab-training/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://img.shields.io/ossf-scorecard/github.com/stephrobert/proxmox-dsoxlab-training?label=OpenSSF%20Scorecard)](https://securityscorecards.dev/viewer/?uri=github.com/stephrobert/proxmox-dsoxlab-training)
[![Plumber compliance](https://score.getplumber.io/github.com/stephrobert/proxmox-dsoxlab-training.svg)](https://score.getplumber.io/github.com/stephrobert/proxmox-dsoxlab-training)
[![SLSA 3](https://slsa.dev/images/gh-badge-level3.svg)](https://slsa.dev)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](./LICENSE)

Verifiable labs for the blog's
["Proxmox VE" course](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/),
played with [dsoxlab](https://github.com/stephrobert/dsoxlab).

## What it is

At the end, a learner can install Proxmox VE on a machine they do not know,
create virtual machines and containers on it, back them up and **prove they
can restore them**, then run a cluster and automate the platform through its
API. Not a list of topics: every lab ends on a state the tests query, such as
a compliant node, an instance that answers or a restore that brings the
service back.

The order matters. The catalog does **not** ship a ready-made Proxmox: learners
install it themselves, against a specification published in the lesson, and
the first lab checks that installation item by item. Nobody learns to install
a hypervisor by receiving it installed.

**A lab is graded on the state of the system, never on the commands typed.**
Learners reach the result by whatever path they choose.

## Requirements

- **Python 3.11+ and [`uv`](https://docs.astral.sh/uv/)**
- **`git`**
- **`dsoxlab`**, the engine, installed as a standalone tool (see below).
- **A hypervisor**, because every lab here is `runtime: vm`:
  **libvirt/KVM** (with `terraform` and the `dmacvicar/libvirt` provider) is
  the default provider declared in [`meta.yml`](./meta.yml).
- **Nested virtualization enabled** on the host: Proxmox VE creates machines
  itself, so the VM that carries it must expose the CPU virtualization
  extensions. On Linux, `cat /sys/module/kvm_intel/parameters/nested` (or
  `kvm_amd`) must print `Y`.
- **6 GB of free RAM and 60 GB of disk** for the single machine, `pve.lab`.
- **For cluster labs:** a separate 48 GB host, with 24 GB reserved for the
  three-node environment and at least 280 GB free in the libvirt pool.
- **Outbound network access**, for the base image and the Proxmox
  repositories.

One virtual machine, `pve.lab` (Debian 13, 4 vCPU, 6 GB, a 40 GB system disk
and a second raw 20 GB disk), declared in `meta.yml` and created by
`dsoxlab provision --host pve.lab`. Proxmox VE replaces the machine's kernel
and takes over its network: nothing runs on your own machine.

Cluster labs use a separate `proxmox-cluster` target: `pve01.lab`, `pve02.lab`
and `pve03.lab`, each with 4 vCPU, 8 GB RAM, a 40 GB system disk and a 40 GB
extra disk. Starting a cluster lab provisions these three Debian 13 machines
on demand through the KVM backend. It does **not** create a Proxmox cluster:
the learner must build it with `pvecm`. To keep the 24 GB host reserve, use the
single-node and cluster environments one at a time.

Start a cluster lab explicitly with:

```bash
dsoxlab start pve-eprouver-cluster --target proxmox-cluster
```

Do not run `dsoxlab provision` without a host filter: it applies the whole
catalog. Run this read-only capacity preflight, then explicitly select the
cluster target:

```bash
uv run python scripts/provision_cluster.py
dsoxlab start pve-eprouver-cluster --target proxmox-cluster
```

The preflight requires at least 26 GiB available RAM, 280 GiB free in the
libvirt pool, 12 logical CPUs and a moderate CPU load. Cluster nodes can then
start additional guest VMs. Starting the lab provisions the three nodes via
the KVM backend; it never forms the Proxmox cluster. `--apply` on the script is
an alternative for manually provisioning those hosts before starting a lab.
An unfiltered `dsoxlab destroy` destroys the catalog's entire infrastructure,
not just the cluster.

`dsoxlab doctor` says what this repository needs and what it does not, and
tells apart a check that failed from one it could not measure.

## Install

`dsoxlab` is published on [PyPI](https://pypi.org/project/dsoxlab/). Install it
as a standalone tool, so it stays out of this repository:

```bash
# 1. The dsoxlab CLI (external tool, stays out of this repo)
uv tool install dsoxlab

# 2. This lab catalog
git clone https://github.com/stephrobert/proxmox-dsoxlab-training.git
cd proxmox-dsoxlab-training

# 3. Check the contract and the machine
dsoxlab validate-structure
dsoxlab doctor
```

### Your first lab

```bash
export LAB_HOME=$PWD
dsoxlab provision --host pve.lab            # creates only the base node
dsoxlab list-labs                          # the catalog, in teaching order
dsoxlab run       verifier-son-installation
dsoxlab challenge verifier-son-installation   # the specification to meet
dsoxlab check     verifier-son-installation   # the verdict, item by item
```

Between `challenge` and `check`, you install Proxmox VE on `pve.lab` yourself,
following the lesson
["Install Proxmox VE on Debian 13"](https://www.stephane-robert.info/en/docs/proxmox/install-on-debian/).
Allow about thirty minutes.

`run` is what prepares the lab. Running `check` on a lab you never started
measures nothing, and says so rather than recording a 0.

### Keeping it up to date

```bash
uv tool upgrade dsoxlab        # the engine, published on PyPI
git -C <this repo> pull        # the catalog
```

The engine and the catalog move independently: a new `dsoxlab` never requires
re-cloning the labs, and new labs never require upgrading the tool, as long as
the contract version matches.

## How it works

### The declarative contract (two levels)

The catalog is described by data, not code, which is what keeps the `dsoxlab`
engine domain-agnostic:

- **`meta.yml`** at the root declares the repository identity and the **order**
  of the sections shown by `list-labs`;
- **`lab.yaml`** per lab declares its `skills`, `level`, `runtime` (type,
  fixtures, services), `distros`, `doc_url` and a `validation` block. A
  `lab.fr.yaml` overrides `title` and `description` in French, and nothing else.

`dsoxlab validate-structure` checks the whole contract: `meta.yml` is well
formed, every referenced lab exists with a valid `lab.yaml`, every declared
test and fixture file is really there, and every relative link in a README
leads somewhere.

### The lab lifecycle

```bash
dsoxlab list-labs              # browse the catalog
dsoxlab show      <id>         # metadata and status of one lab
dsoxlab run       <id>         # set the starting state
dsoxlab challenge <id>         # read the mission, no step-by-step
dsoxlab hint      <id>         # reveal a hint (deducted from the score)
dsoxlab check     <id>         # run the tests, compute and record the score
dsoxlab clean     <id>         # undo what the lab set up
dsoxlab progress               # per-section progress, average score
```

### Runtimes

Every lab is `vm`: Proxmox VE does not install on a workstation, and its guests
live inside the machine, not on the learner's host.

| Runtime | What the lab asks for |
|---|---|
| `vm` | the `pve.lab` machine for ordinary labs, provisioned with an explicit host filter, on Debian 13, with nested virtualization. Cluster labs select the separate `proxmox-cluster` target, whose three nodes are provisioned on demand; the learner creates the cluster. |

### The validation model

Validation **proves the state, it does not trust the learner**. Each lab ships
`pytest` tests under `challenge/tests/` that read what the system holds, never
what a file contains or which commands were typed.

And a lab is proven **in both directions**: the tests must fail before the work
and pass after it. A test that is green before the work is not a test, it is an
assumption about the setup.

Reference solutions live under `solution/<lab>/`, encrypted with
`ansible-vault`; the password (`.vault-pass` at the root) is never versioned.
A solution in clear text would spoil the lab, and git keeps it forever.

GitHub CI checks the contract, workflows and repository quality, but does not
provision VMs or replay labs. Its badge is therefore not pedagogical evidence:
the runtime 0 → 100 cycle is checked separately with
`python3 scripts/valider-labs.py --lab <id>` on provisioned infrastructure.

### Scoring, hints, progress

`check` records a score (tests passed out of total, minus the cost of any hints
revealed). Hints are **base64-encoded** in `challenge/hints.yaml`, so that
opening the file does not give them away, and their cost grows with their
precision. History lives in a SQLite database **local to this repository**.

A run that measured nothing is neither a pass nor a failure: if every collected
test skips, `check` records no score and says why. A score of 0 would accuse the
lab of what is missing from the machine.

## Catalog

Played in order. Catalogue presence means a lab has been authored; it is not
an execution attestation. A lab is proven only after its tests have failed
before the task and passed after it on the target environment.

<!-- LABS:START -->
### Design and qualify the first lab node

Prepare an isolated lab and connect a guest to its assigned network.


| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `pve-preparer-laboratoire` | Préparer un laboratoire et son plan de ressources | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-raccorder-instance` | Connect a VM to the network and fix the fault at the right layer | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/reseau/) |

### Deploy a node and its first instances

Install Proxmox VE, from the ISO or on top of Debian 13, and check it
against a written specification; then create a KVM VM and an
unprivileged LXC container, build a template, and restore a first service.


| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `pve-installer-noeud` | Installer Proxmox et établir un accès fiable | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/installation/) |
| `verifier-son-installation` | Check your Proxmox VE installation against the specification | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/installation-debian/) |
| `pve-suivre-tache` | Read Proxmox tasks: tie each result to its task | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/interface-ui/) |
| `pve-creer-vm` | Create a KVM VM and check that its service answers | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/creer-vm-kvm/) |
| `pve-creer-lxc` | Create an unprivileged LXC container with bounded resources | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/conteneurs-lxc/) |
| `pve-reparer-agent` | Restore the QEMU guest agent without forcing the VM off | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/qemu-guest-agent/) |
| `pve-gerer-cycle-vie` | Resize a VM and prove a local rollback | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-construire-template` | Build a cloud-init template and independent clones | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-restaurer-premiere-instance` | Back up and restore a first VM on an isolated network | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-epreuve-deploiement` | Livrer et restaurer un premier service virtualisé | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |

### Secure identities and boundaries

Delegate rights, secure identities and filter management and guest flows.


| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `pve-deleguer-acces` | Delegate pool access without widening scope | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-securiser-identites` | Secure human and machine identities | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-filtrer-flux` | Filter management and guest traffic | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-maitriser-volumes-lxc` | Manage LXC volume identity and backups | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |

### Operate guest networks

Segment VLANs, route flows and make reversible network changes.


| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `pve-segmenter-vlan` | Segment and diagnose VLANs | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-changer-reseau` | Route, publish, and change networking safely | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |

### Back up and restore with PBS

Integrate PBS, protect backup keys and prove service recovery.


| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `pve-integrer-pbs` | Integrate Proxmox Backup Server | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-proteger-sauvegardes` | Encrypt, retain, and verify backups | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-prouver-restauration` | Restore a service and measure recovery objectives | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |

### Observe, diagnose and maintain

Observe capacity, diagnose an unavailable guest and maintain a node.


| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `pve-observer-alerter` | Observe capacity and receive alerts | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-diagnostiquer-instance` | Diagnose an unavailable VM | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-maintenir-noeud` | Maintain a node and prepare an upgrade | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-exploiter-thin-pool` | Operate Directory and LVM-thin safely | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-restaurer-redondance-zfs` | Restore ZFS mirror redundancy | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-epreuve-exploitation` | Operate, diagnose, and recover a platform | l2 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |

### Run a cluster and keep it available

Build a three-node cluster, migrate and replicate guests, test high
availability against a failure imposed from outside, and recover after
losing the primary site.


| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `pve-eprouver-cluster` | Build and exercise a three-node cluster | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/chapter-pvecm.html) |
| `pve-qualifier-stockage-partage` | Qualify shared storage and its failure boundary | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/chapter-pvesm.html) |
| `pve-migrer-instance` | Migrate a VM and container with measured client impact | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/chapter-qm.html) |
| `pve-reserver-capacite` | Reserve N-1 capacity and enforce placement | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/) |
| `pve-mesurer-replication` | Measure ZFS replication and the recoverable data boundary | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/chapter-pvesr.html) |
| `pve-eprouver-ha` | Exercise service failover without duplicate writers | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/chapter-ha-manager.html) |
| `pve-maintenir-cluster` | Maintain a node while preserving the service contract | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/) |
| `pve-reprendre-hors-site` | Recover from a secondary PBS without primary-site dependencies | l3 | vm | - |
| `pve-epreuve-disponibilite` | Availability assessment with independent disaster recovery | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/chapter-ha-manager.html) |

### Automate a reproducible platform

Drive the API and wait for real results, provision with Terraform under
measured rights, build a reliable Ansible inventory, and deliver a
platform that a clean controller can rebuild.


| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `pve-piloter-api` | Pilot the API and wait for real results | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/api-viewer/) |
| `pve-provisionner-terraform` | Provision with Terraform and measured permissions | l3 | vm | [guide (FR)](https://registry.terraform.io/providers/bpg/proxmox/latest/docs) |
| `pve-reconcilier-etat` | Manage state, drift and destructive changes | l3 | vm | [guide (FR)](https://registry.terraform.io/providers/bpg/proxmox/latest/docs) |
| `pve-fiabiliser-inventaire` | Build a reliable Ansible inventory | l3 | vm | [guide (FR)](https://docs.ansible.com/ansible/latest/inventory_guide/intro_dynamic_inventory.html) |
| `pve-operer-ansible` | Automate operations with Ansible | l3 | vm | [guide (FR)](https://docs.ansible.com/ansible/latest/collections/community/proxmox/proxmox_module.html) |
| `pve-livrer-plateforme` | Deliver a reproducible, transferable platform | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/) |
| `pve-epreuve-automatisation` | Deliver a reproducible platform through API and IaC | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/) |

### Options

Windows with VirtIO, VMware migration, Ceph and SDN.
Each option is independent, and none of them blocks a level.


| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `pve-integrer-windows` | Operate a Windows VM with VirtIO | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/) |
| `pve-migrer-vmware` | Migrate a VMware workload with a cutover plan | l3 | vm | [guide (FR)](https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE) |
| `pve-eprouver-ceph` | Deploy and troubleshoot Ceph storage | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/chapter-pveceph.html) |
| `pve-deployer-sdn` | Build an SDN network for the workload | l3 | vm | [guide (FR)](https://pve.proxmox.com/pve-docs/chapter-pvesdn.html) |

_47 labs, table generated by `scripts/gen_catalog.py`._
<!-- LABS:END -->

## Contributing

Read [`CONTRIBUTING.md`](./CONTRIBUTING.md). In short: a lab is proven **in both
directions** before it is merged, `dsoxlab validate-structure` is green, and the
statement exists in English and in French.

Anything user-facing is bilingual. A document translated on one side only is
reported by the validator, not left to goodwill.

## License

See [`LICENSE`](./LICENSE).
