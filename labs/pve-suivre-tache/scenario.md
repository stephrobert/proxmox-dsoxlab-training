# What happened on this node, and what is true now

A colleague handled three VMs on this node before leaving: sentinel 190, and
two temporary VMs, 191 and 192. They leave you a simple question, "what
worked, and what did not?", and a node to put back in order.

The instructions, in `/opt/lab-proxmox/pve-suivre-tache/consigne.md`, give
the model of the expected report.

## Mission

1. Find the start task of VM 191 and the one of VM 192, by their **UPID**, the
   unique identifier Proxmox gives each task.
2. For each, note its **final result**: `OK`, or the error message Proxmox
   recorded at the end of the task.
3. Give the **current state** of sentinel 190.
4. Write it all into `/root/rapport-taches.txt`, then delete VMs 191 and 192
   without touching 190.

## What is graded

| # | What is checked | How |
|---|---|---|
| 1 | Correlation | every UPID in the report is that of the right start task |
| 2 | The failure | the start of 192 is not reported OK, and its cause matches the task's final message |
| 3 | Current state | the state reported for 190 is its current state, not the one from its old log |
| 4 | Cleanliness | 191 and 192 no longer exist, 190 exists and its configuration did not change |

## Starting over

`dsoxlab clean pve-suivre-tache` removes the three VMs and the report. A new
`run` triggers fresh tasks, with new UPIDs.
