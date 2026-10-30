# Changelog

All notable changes to this catalog are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this catalog
follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**What a version means here.** A catalog is not a library: a MINOR bump adds
labs, a PATCH fixes a statement or a test without changing what a lab proves,
and a MAJOR renames or removes labs, which breaks the progress already recorded
by learners.

## [Unreleased]

### Added

- The catalog skeleton, created by `dsoxlab new catalog`.
- **The first lab, `verifier-son-installation`**: it grades, item by item, a
  Proxmox VE 9 installation the learner performed themselves on a bare
  Debian 13, with four bilingual hints of growing cost and a challenge README.
- **Five level 1 labs**, each attested 0 → 100 on a fresh machine:
  `pve-raccorder-instance` (plug a VM back into the right bridge without
  recreating it), `pve-suivre-tache` (tie each result to its task by UPID),
  `pve-creer-vm` (hardware contract, boot from disk, a service that comes
  back after a reboot), `pve-creer-lxc` (unprivileged container, limits
  read from the cgroups) and `pve-reparer-agent` (guest agent restored with
  no forced stop, fault drawn from two cases).
- `shared/noeud-proxmox.yml`, a guard that only replays the attested
  Proxmox installation when the node is not ready, and
  `shared/image-debian-cloud.yml`, the Debian 13 cloud image verified by
  its checksum.
- **The tooling of the sibling catalogs**: `scripts/valider-labs.py` and
  `validation-labs.json`, which attest a lab both ways (0 before the work, 100
  after the solution); `gen_catalog.py`, `check-playbooks.py`,
  `check-tests.py`, `chiffrer-solutions.sh`, `rebase-vms.sh` and the
  safeguards under `tests/`.
- **The security chain of a public repository**: `plumber` and `scorecard`
  workflows, CodeQL configuration, `dependabot`, `CODEOWNERS`, issue
  templates, `.poutine.yml`, `.plumber.yaml`, `uv.lock`, and the `pre-commit`
  hook taken from the siblings.

### Changed

- **Sections follow the levels of the course**: deploy, secure and operate,
  cluster and availability, automate, then the options. Sections that are
  still empty are declared, not hidden.
- `README`, `RELEASING`, `pyproject.toml` and `meta.fr.yml` are filled in on
  the siblings' model; they still carried the skeleton texts and the
  temporary name `proxmox`.
- GitHub Actions are pinned to the same versions as the siblings.
