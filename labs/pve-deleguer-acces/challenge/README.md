# Challenge: Delegate pool access without widening scope

Create the two pools and two VM sentinels, then assign a least-privilege role to `equipe-n2@pve` on the assigned pool only. Keep the neighbour and node administration outside that ACL. Prove the allow/deny matrix by querying actual PVE permissions as the delegated principal; do not treat root-side ACL text as proof of effective access.

The assigned object is `VMIDs 201/n2-delegueracc and 216/n2-voisin; pools lab-n2-deleguer and lab-n2-voisin; test accounts equipe-n2@pve, auditeur-n2@pve, and secours-n2@pve.`. Implement the native Proxmox state described in `scenario.md`; do not submit command logs or self-reported evidence. Run the functional tests against the assigned PVE target only after all stated external fixtures are available. Tests make no changes.

## Feedback

- A passing check means only that the queried Proxmox state matches its assertion.
- A missing PBS/CT/ZFS/thin-pool fixture is a prerequisite failure, not a pass.
- Keep secrets out of the evidence and test output.
