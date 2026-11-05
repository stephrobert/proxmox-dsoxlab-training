# Mission

Initial state: genuinely separate secondary PBS in the lab model, empty recovery
PVE, external rescue-key vault and write journal. Primary VM 9371 must be named
`n3-pve-reprendre-hors-site-9371`; allocate secondary backup and recovery storage
`n3-offsite` explicitly. These independent hosts are currently absent.

1. Announce RPO/RTO and exact backup snapshot. Read completed sync tasks and
   the actual snapshot manifest from secondary PBS.
2. From the external controller, block primary networks/storage throughout the
   recovery recipe. Verify attempted/established connections, not just intentions.
3. Retrieve only rescue keys from the independent vault without printing key
   contents. Restore on the empty recovery target from secondary PBS alone.
4. Execute external business transactions and compare recovered sequence/marker
   with acknowledged writes and failure/availability timestamps.
5. Keep primary and recovered writers segregated during controlled return.

Only allocated hosts, storage, networks and IDs may change. Preserve before
observations, mask secrets but not resource identities, retain normal TLS/SSH
verification and rescue controls. No forced votes/fencing bypass or weakened
durability. Report untested physical separation explicitly; nested topology does
not prove a physical-site disaster tolerance. Equivalent safe recipes are accepted.
