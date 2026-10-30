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
- **Outbound network access**, for the base image and the Proxmox
  repositories.

One virtual machine, `pve.lab` (Debian 13, 4 vCPU, 6 GB, a 40 GB system disk
and a second raw 20 GB disk), declared in `meta.yml` and created by
`dsoxlab provision`. Proxmox VE replaces the machine's kernel and takes over
its network: nothing runs on your own machine.

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
dsoxlab provision                          # creates pve.lab, a bare Debian 13
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
| `vm` | the `pve.lab` machine, provisioned by `dsoxlab provision`, on Debian 13, with nested virtualization. The learner installs Proxmox VE on it, then creates their guests there. |

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

Played in order. More labs are added as they are written and proven in both
directions.

<!-- LABS:START -->
### Deploy a node and its first instances

Install Proxmox VE, from the ISO or on top of Debian 13, and check it
against a written specification; then create a KVM VM and an
unprivileged LXC container, build a template, and restore a first
instance.


| Lab (id) | Title | Level | Runtime | Companion guide |
|---|---|---|---|---|
| `verifier-son-installation` | Check your Proxmox VE installation against the specification | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/installation-debian/) |
| `pve-creer-vm` | Create a KVM VM and check that its service answers | l1 | vm | [guide (FR)](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/creer-vm-kvm/) |

_2 labs, table generated by `scripts/gen_catalog.py`._
<!-- LABS:END -->

## Contributing

Read [`CONTRIBUTING.md`](./CONTRIBUTING.md). In short: a lab is proven **in both
directions** before it is merged, `dsoxlab validate-structure` is green, and the
statement exists in English and in French.

Anything user-facing is bilingual. A document translated on one side only is
reported by the validator, not left to goodwill.

## License

See [`LICENSE`](./LICENSE).
