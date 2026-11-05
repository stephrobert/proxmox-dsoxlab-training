# Challenge: Operate a Windows VM with VirtIO

Use only a Windows ISO you are licensed and authorized to use and the official VirtIO driver ISO. Install a supported selected build, load disk/network drivers, verify guest agent and network after reboot, remove installation media, and restore a backup that includes EFI and TPM state.

## What the tests observe

- Live VM configuration has EFI, TPM 2.0, VirtIO disk/network, and no installation media.
- The guest agent reports a live network interface/address after reboot.
- A real restore retains the EFI and TPM devices.

Tests inspect live Proxmox/guest state. They do not grade command history or an unverified claim. Missing required capabilities are reported as blocked, never as success.
