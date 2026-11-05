# Mission: Operate a Windows VM with VirtIO

Use only a Windows ISO you are licensed and authorized to use and the official VirtIO driver ISO. Install a supported selected build, load disk/network drivers, verify guest agent and network after reboot, remove installation media, and restore a backup that includes EFI and TPM state.

## Acceptance criteria

1. Live VM configuration has EFI, TPM 2.0, VirtIO disk/network, and no installation media.
2. The guest agent reports a live network interface/address after reboot.
3. A real restore retains the EFI and TPM devices.

## Prerequisites

BLOCKED unless both ISO paths and an explicit license authorization are recorded in /etc/lab-proxmox/pve-integrer-windows.yml. Setup never downloads Windows media or bypasses activation/OOBE.

No PVE installation, host provisioning, or feature installation is performed by this scenario.
