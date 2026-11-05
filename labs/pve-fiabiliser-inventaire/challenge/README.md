# Challenge: Build a reliable Ansible inventory

Build a dynamic inventory from the live Proxmox API for only the two tagged lab VMs. Use their actual node management addresses, explicit handling for missing agent/IP data, and refresh rather than stale cache. The test invokes the inventory source and compares it with live cluster resources.

## What the tests observe

- The computed host set is exactly the two tagged lab VMs.
- Each host maps to its live node and management network; missing guest-agent/IP data is not invented.
- The uncached inventory reflects current cluster state.

Tests inspect live Proxmox/guest state. They do not grade command history or an unverified claim. Missing required capabilities are reported as blocked, never as success.
