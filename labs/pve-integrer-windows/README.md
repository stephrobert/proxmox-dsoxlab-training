# pve-integrer-windows

Use only a Windows ISO you are licensed and authorized to use and the official VirtIO driver ISO. Install a supported selected build, load disk/network drivers, verify guest agent and network after reboot, remove installation media, and restore a backup that includes EFI and TPM state.

**Prerequisites / blocked conditions:** BLOCKED unless both ISO paths and an explicit license authorization are recorded in /etc/lab-proxmox/pve-integrer-windows.yml. Setup never downloads Windows media or bypasses activation/OOBE.

```bash
dsoxlab run pve-integrer-windows
dsoxlab check pve-integrer-windows
dsoxlab clean pve-integrer-windows
```

Cleanup is limited to this lab's declared VMIDs, tag, and dedicated lab objects. It never removes a template, source workload, shared storage, or cluster node.
