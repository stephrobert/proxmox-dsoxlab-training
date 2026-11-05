# Challenge: Manage state, drift and destructive changes

Import the existing lab VM without recreating it, capture a plan after a controlled live configuration drift, then correct the declared configuration. Keep a saved safe plan that does not destroy or replace the VM, and show that the final state converges to the real VM.

## What the tests observe

- Terraform state identifies the exact pre-existing VMID.
- The drift plan records a real change while keeping delete out of the action list.
- The final live config matches state and the safe plan contains no replacement.

Tests inspect live Proxmox/guest state. They do not grade command history or an unverified claim. Missing required capabilities are reported as blocked, never as success.
