# Mission

Initial state: a healthy cluster, two qualified destinations, VM 9321 and CT
9322 with durable witness services, external request generator. Instructor
names: `n3-pve-migrer-instance-9321` and `n3-pve-migrer-instance-9322`.

1. Inventory storage, CPU compatibility, bridges, ISO/snippet/mount dependencies.
   On the allocated guest only, introduce a dedicated source-only dependency;
   attempt migration and retain the failed task's UPID, final error and unchanged
   owner. Do not remove another guest's disk or alter shared storage globally.
2. Remove that negative fixture safely. Move VM and CT to the requested node
   using their respective supported live/offline/restart migration methods.
3. Run external transactions during migration; compare durable markers,
   fingerprints, sequences and session behavior. Publish actual response gaps.
4. Really stop/start both guests on the destination; detect residual source
   dependencies and confirm one active owner per guest.

Restrict actions to assigned resources; preserve diagnostics before correction,
mask secrets not identities, retain verified TLS/SSH and rescue console.
Equivalent implementations meeting all criteria are accepted. Do not force
quorum/unlock or label migration a failure/fencing experiment. Report measured
versus assumed continuity and an explicit return plan.
