# Challenge: an accurate task report, and a node put back in order

You work on `pve.lab`. The instructions are in
`/opt/lab-proxmox/pve-suivre-tache/consigne.md`.

## What is expected

1. `/root/rapport-taches.txt` gives the exact UPID of the start tasks of VMs
   191 and 192.
2. The start of 191 is reported `OK`, the one of 192 carries the final error
   message of its task.
3. The state reported for 190 is its current state.
4. VMs 191 and 192 are deleted, 190 is untouched.

## What is proven

The tests compare the report with the UPID register kept by the lab, read the
final status of each task through the API, the state of 190 with `qm status`,
and the fingerprint of its configuration.
