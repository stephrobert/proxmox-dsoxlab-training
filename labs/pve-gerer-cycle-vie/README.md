# Resize a VM and prove a local rollback

The application VM is running with 1 vCPU, 1024 MiB RAM and a 4 GiB system disk. Preserve a local return point before allocating 2 vCPUs, 2048 MiB RAM and an 8 GiB disk. Extend the partition and filesystem inside Debian as well. The original witness, guest agent and static network are supplied.

Read [scenario.md](./scenario.md) before starting.

```bash
dsoxlab run pve-gerer-cycle-vie
dsoxlab challenge pve-gerer-cycle-vie
dsoxlab check pve-gerer-cycle-vie
```
