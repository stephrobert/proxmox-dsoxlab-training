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

## Graded requirements

1. Report the exact start-task UPID for VM 191.
2. Report the exact start-task UPID for VM 192.
3. Report the complete final result of the start task for VM 191, preserving its text.
4. Report the complete final result of the start task for VM 192, preserving its text.
5. Report the current state of VM 190, rather than its historical start result.
6. Delete temporary VM 191.
7. Delete temporary VM 192.
8. Keep sentinel VM 190 present.
9. Preserve the initial configuration of sentinel VM 190.

Persistence checks perform a clean stop and start and observe both states. Unreadable measurements fail. Preservation checks only count once the report exists, the network is repaired or the agent answers, depending on the lab.

## Starting over

`dsoxlab clean pve-suivre-tache` removes the three VMs and the report. A new
`run` triggers fresh tasks, with new UPIDs.
