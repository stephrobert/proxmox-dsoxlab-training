# Back up and restore a first VM on an isolated network

Source VM 198 already serves a session-specific witness on 10.10.113.198:8080. The preparation supplies isolated bridge vmbr9 and client namespace dsox-restore (10.10.113.240/24). Back up to /var/lib/vz/dump/pve-restaurer-premiere-instance and restore to VM 199. Keep the restored guest IP unchanged: the source and restore use different Ethernet segments. Do not connect the isolated bridge to the host network.

Read [scenario.md](./scenario.md) before starting.

```bash
dsoxlab run pve-restaurer-premiere-instance
dsoxlab challenge pve-restaurer-premiere-instance
dsoxlab check pve-restaurer-premiere-instance
```
