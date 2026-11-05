# Mission

Form one three-node cluster and demonstrate behavior with and without a majority.
Initial state: compatible preinstalled nodes, isolated Corosync network and an
independent controller with verified SSH identities and a rescue console.

1. Compare node identities, versions, distributed configuration and votes
   before joining. Record observations before any correction. Form the cluster
   using the allocated Corosync network, not an arbitrary production interface.
2. Observe the healthy cluster from all three nodes.
3. Remove one voter from the external controller; observe two surviving voters.
4. Restore, then remove two voters; measure a genuine pmxcfs write refusal on
   the survivor. Never run `pvecm expected`, local pmxcfs mode or lock bypasses.
5. Restore all voters and compare configuration, members and pending tasks.
   Escalate split configuration or failed recovery through the rescue console.

Only allocated hosts, networks and resources may change. Preserve observations
and mask secrets without hiding resource identities. An alternative configuration
is accepted if it meets the same contract. Document virtual versus physical
failure domains: nested node loss does not prove physical-server/site tolerance.
See the challenge for bounded controller commands, rollback and progressive hints.
