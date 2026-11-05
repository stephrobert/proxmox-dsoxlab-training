# Mission: Build a reliable Ansible inventory

Build a dynamic inventory from the live Proxmox API for only the two tagged lab VMs. Use their actual node management addresses, explicit handling for missing agent/IP data, and refresh rather than stale cache. The test invokes the inventory source and compares it with live cluster resources.

## Acceptance criteria

1. The computed host set is exactly the two tagged lab VMs.
2. Each host maps to its live node and management network; missing guest-agent/IP data is not invented.
3. The uncached inventory reflects current cluster state.

## Prerequisites

Creates two small stopped VMs with the lab-only tag. Requires ansible-inventory and a working, least-privilege Proxmox API credential; setup does not install Ansible.

No PVE installation, host provisioning, or feature installation is performed by this scenario.
