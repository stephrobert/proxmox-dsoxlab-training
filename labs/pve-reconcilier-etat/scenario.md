# Mission: Manage state, drift and destructive changes

Import the existing lab VM without recreating it, capture a plan after a controlled live configuration drift, then correct the declared configuration. Keep a saved safe plan that does not destroy or replace the VM, and show that the final state converges to the real VM.

## Acceptance criteria

1. Terraform state identifies the exact pre-existing VMID.
2. The drift plan records a real change while keeping delete out of the action list.
3. The final live config matches state and the safe plan contains no replacement.

## Prerequisites

Creates only stopped VM 1738 and records its original configuration hash. Do not apply a plan containing delete/replace; state and plan files must remain private.

No PVE installation, host provisioning, or feature installation is performed by this scenario.
