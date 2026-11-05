# Mission

Initial state: cluster with explicit budgets, two loads to separate and a
stopped candidate, measured host memory and dedicated `n3-capacity` storage.
IDs 9331, 9332, 9333 must be named `n3-pve-reserver-capacite-<id>`.

1. Measure each host's memory usage/maximum, guest configured maxima, host
   overhead and disk availability. Simulate losing the largest node, not an
   average node. Separate assumptions from measurements.
2. Configure the supported version's effective placement/anti-affinity rule
   for the two loads. Show separation before and after an allowed move.
3. Present a candidate whose demand exceeds residual recovery reserve.
   Refuse or explicitly defer it; do not start an unbounded memory stressor.
4. Run a bounded transaction load, remeasure headroom and publish hardware limits.

Only allocated IDs/storage/networks may change. Keep before observations,
verified SSH/TLS, rescue console and masked secrets. Equivalent constraints
meeting the criteria are acceptable. No quorum forcing or undisclosed
overcommit; capacity planning is not a tested physical-node HA claim.
