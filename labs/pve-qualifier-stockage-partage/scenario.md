# Mission and initial state

Healthy three-node cluster, separate lab NFS server, dedicated volume/exports,
and guest 9311 named `n3-pve-qualifier-stockage-partage-9311` with a durable
business witness. Storage ID is `n3-shared`; a shared flag alone proves nothing.

1. Verify each mount's real NFS server/export identity. Write a controlled nonce
   on the allocated volume from one node; read and hash it from the other nodes.
2. Perform an authorized write and a genuinely refused out-of-scope lab-export
   operation. Do not test random production exports or make global export changes.
3. From the independent controller, stop only the dedicated lab NFS service.
   Observe actual I/O and the external business service, not just responding PVE UIs.
4. Restore the server; re-read hashes, perform business transactions and verify
   that mounts have not been duplicated or retargeted.

Change only allocated hosts, networks, guests and volumes. Preserve before
observations; mask secrets, not identities. Equivalent configurations are
accepted. Keep verified SSH/TLS and rescue access. Distinguish storage failure
from HA: a surviving quorum does not make an unavailable NFS service highly available.
Report virtual/physical domains and return/cleanup limits.
