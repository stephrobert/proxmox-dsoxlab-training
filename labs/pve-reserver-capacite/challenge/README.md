# Allocation and evidence

Create independent-controller `challenge/work/config.json` with
`hosts=["pve01.lab","pve02.lab","pve03.lab"]`, `guest_ids=[9331,9332,9333]`,
`sources={}`, `console_verified=true`, `nested_only=true`,
`destination="pve02.lab"`, `candidate_bytes` as its declared demand, and:

```json
{
  "budget": {
    "host_overhead_bytes": 536870912,
    "recovery_bytes": 1073741824,
    "disk_reserve_bytes": 1073741824
  },
  "guest_network": "10.10.113.0/24",
  "service_url": "https://<guest>/api/lab/pve-reserver-capacite",
  "marker": "<durable marker>"
}
```

Numbers are examples, **not measurements**; replace them with justified budgets.
Guest GET returns durable `{"sequence":123,"marker":"..."}`; POST append returns
the updated durable sequence. Trusted TLS and known SSH keys/noninteractive sudo
are mandatory; use provisioned dsoxlab inventory or existing `N3_SSH_CONFIG`.
No missing node/service is provisioned. Validate the independent rescue console.

```bash
python3 tools/controller.py snapshot --phase migrated
python3 tools/controller.py snapshot --phase candidate-rejected
python3 tools/controller.py probe --duration 30
```

Take snapshots after the allowed move and after the decision to defer/refuse the
candidate. Keep 9333 stopped. Probe is bounded to 1–180 seconds. No physical
failure or quorum manipulation is necessary for the N-1 arithmetic.
Machine checks compare measured memory/disk headroom, guest maxima, separation
and candidate inactivity. Human review must also verify the effective
version-specific placement rule and documented admission/referral decision.
Write `challenge/work/report.md` for all `contract.json` criteria, including
units, host/guest/storage calculations, observations under load, hypothetical
largest-node loss, rules, candidate demand, limits and return steps.
Archive evidence before cleanup; cleanup removes only controller evidence and
restores its actions, never deletes guests or rules. Revert only owned rules
and placements through the documented runbook. No unbounded load or lock bypass.

## Hints

1. Measure the largest node and actual free storage.
2. Configured guest maxima and host overhead differ from current guest usage.
3. Free capacity before failure is not free capacity after losing the largest host;
   a displayed affinity preference need not be an enforced separation rule.
