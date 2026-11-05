# pve-suivre-tache

Write /root/rapport-taches.txt with demarrage-191, demarrage-192 and etat-190 keys. The lab supplies the initial tasks and the sentinel.

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
