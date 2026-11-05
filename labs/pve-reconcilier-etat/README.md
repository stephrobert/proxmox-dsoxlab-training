# pve-reconcilier-etat

Import the existing lab VM without recreating it, capture a plan after a controlled live configuration drift, then correct the declared configuration. Keep a saved safe plan that does not destroy or replace the VM, and show that the final state converges to the real VM.

**Prerequisites / blocked conditions:** Creates only stopped VM 1738 and records its original configuration hash. Do not apply a plan containing delete/replace; state and plan files must remain private.

```bash
dsoxlab run pve-reconcilier-etat
dsoxlab check pve-reconcilier-etat
dsoxlab clean pve-reconcilier-etat
```

Cleanup is limited to this lab's declared VMIDs, tag, and dedicated lab objects. It never removes a template, source workload, shared storage, or cluster node.
