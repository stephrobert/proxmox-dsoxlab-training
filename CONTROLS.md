# Catalog checks

Ported from `containers-dsoxlab-training` on November 5, 2026.
The source contains **20 test modules**. Sixteen shared checks are now present
and wired into the Proxmox catalog. Four modules exercise Docker components
that this catalog does not contain.

## Test mapping

Module names refer to files under `tests/` in each repository.

| Containers module | Proxmox treatment |
| --- | --- |
| `test_assertions_bilingues.py` | Existing port retained, including both language arguments and rejection witnesses. |
| `test_assertions_non_nues.py` | Existing port retained. |
| `test_liens_internes.py` | Existing port retained. |
| `test_langue_officielle.py` | Existing port retained. |
| `test_verdicts_et_commun_separes.py` | Existing check and companion tool retained. |
| `test_meta_declare_les_labs.py` | Ported: both directions, duplicates and missing files. Source Docker prerequisites and the generator's `_runtime_label` do not apply. |
| `test_hints_ecrits.py` | Ported: four written bilingual hints, strict base64 decoding. Retains Proxmox costs: 5, 10, 15, 20. |
| `test_style_apprenant.py` | Ported, with the explicit allowance for brief emoji. Existing French typography hook retained. |
| `test_solutions_chiffrees.py` | Ported: Vault header, solution files and untracked Vault key. |
| `test_aucun_jeton_versionne.py` | Ported: secret patterns and witnesses; tracked scope checked against known repository files. The source threshold of 400 does not describe the 132 tracked files here. |
| `test_exigence_critique_declaree.py` | Ported: non-compensable promises and declared test names. |
| `test_briefs_pointent_juste.py` | Ported: declared hosts, existing paths, declared work directories or paths actually consumed by the local N3 controller. |
| `test_images_epinglees.py` | Ported with its witnesses: registry references in setup and cleanup playbooks, excluding learner fixtures. Does not claim to pin qcow2 images or PVE packages. |
| `test_outillage_coherent.py` | Adapted: validates every hook target and recognizes directory-wide pytest coverage. Requires contract and catalog checks. |
| `test_maturite_des_labs.py` | Classification ported. Docker harness tests replaced by `test_validateur_catalogue.py`, exercising cycle failures and unavailable isolation without machines. These tests do not provide a PVE resource snapshot. |
| `test_ancres_trois_issues.py` | Ported with `scripts/verifier-ancres.py`: valid or invalid anchor, unreachable page, stale or unused waiting entries. No Containers waiting list copied. |
| `test_paquets_epingles.py` | N/A: checks five Docker packages in `infra/bootstrap.yaml`, absent here. This port makes no claim about PVE package pinning. |
| `test_capstone_recovery.py` | N/A: tests `_wait_ready` in the absent Docker lab `capstone-chaine-complete`. |
| `test_sonde_du_contexte_de_build.py` | N/A: tests the probe in the absent lab `buildkit-secret-de-build`. |
| `test_index_multiarch_sans_attestations.py` | N/A: tests OCI indexes in the absent lab `images-multi-architecture`. |

`test_garde_fous_portes.py` adds passing and failing witnesses for the ported
checks. Existing Proxmox contract, provisioning and controller-message checks
remain wired.

## Hook mapping

All shared Containers hooks are present: file hygiene, YAML, JSON, TOML,
case and merge conflicts, large files, private keys, Ruff, lab declarations,
hints, style, assertions, images, critical requirements, solutions, links,
language, maturity, secrets, briefs, tooling consistency, anchors, structure,
generated catalog, lock file and verdict separation.

Hooks for absent Docker labs and their bootstrap are not installed as dead
commands. Their four modules are listed above. Maturity includes the Proxmox
validator checks.

Hadolint follows this catalog's layout: repository and `solution/` Dockerfiles,
excluding fixtures, learner work and ignored plaintext solutions. Vault files
are decrypted into temporary files before analysis. No Dockerfile is explicitly
reported as `N/A`; a missing key is reported as an unperformed check.
TruffleHog complements the secret-pattern checks. CI installs the Hadolint and
TruffleHog versions used by Containers, verifies their published checksums,
and runs the hooks.

The anchor hook runs at `pre-push` because it uses the network. Its tests use
simulated probes. Existing CI replays both pre-commit stages.

## Debt measured on November 5, 2026

The new checks are **enabled and blocking**. No exemption list was added to
produce a passing result.

| Debt | Measurement | Required correction |
| --- | --- | --- |
| Incomplete hints | 71 failures: 41 labs lack the four expected costs, 15 lack a recognized hint list and 15 lack usable bilingual texts | Write and encode four levels for the affected labs. The last two groups refer to the same 15 labs. |
| Missing solutions | 41 failures | Supply encrypted reference solutions for the 41 labs in progress. All six existing solutions pass encryption checks. |
| Typography | 54 failing files | Replace each em dash according to its sentence. |

The local suite contains 1,880 cases: **1,616 passed, 166 failed, 98 skipped**.
Most skips reflect the explicit brief emoji allowance; others cover absent
skeletons or an absent anchor waiting list. Rejection witnesses pass. Run
`pytest tests/ -q` for individual lab and file diagnostics.

Hook parity also rejects pre-existing issues: `pve-reprendre-hors-site`
metadata, stale generated README tables and French typography. Playbook loading
and test name resolution pass. Ruff passes for the ported checks; global lint
still reports issues in the labs in progress, whose untracked files are not
yet examined by pre-commit's file-based Ruff hook.

None of the 46 populated `doc_url` values currently has a fragment, so the
anchor hook has no real anchor to judge. Its witnesses still exercise failures.
With no staged changes, TruffleHog scanned zero bytes; that run does not establish
that untracked files contain no secrets. The pattern check examined the current
tracked scope.

No Proxmox campaign was run and no lab verdict was changed.
