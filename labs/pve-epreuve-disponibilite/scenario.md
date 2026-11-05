# Assessment mission

Operate three qualified nodes with recovery reserve, demonstrate service behavior
under externally imposed failure, then recover from an external backup.
Initial state: qualified cluster/storage, external transactional client,
independent power/network controller and emergency abort, primary PBS,
secondary copy, empty recovery target and announced RPO/RTO.
VM 9381 is `n3-pve-epreuve-disponibilite-9381`; storage `n3-availability`.
The independent PBS/recovery/vault hosts are not currently declared.

Deliver configuration/allocation, service/data evidence including failures and
refusals, and a handover dossier with limits, return, recovery and cleanup.
Demonstrate the five catalog criteria in `contract.json`: architecture,
failover, data model, maintenance/incompatible-migration refusal, independent recovery.

Never force quorum or reduce durability. Failure must be genuinely imposed from
outside; orderly guest stop proves no fencing. Restrict all actions to allocated
hosts/resources and preserve rescue access, TLS/SSH identity and secret masking.
Distinguish virtual-node, physical-server and site loss: nested does not prove all
three. **No hints or solution during assessment.** Agree permitted documentation
and stop conditions before starting. Only the operational evidence interface is
provided, not an assessment answer.
