# Challenge : un rapport de tâches juste, et un nœud remis en ordre

Vous travaillez sur `pve.lab`. La consigne est dans
`/opt/lab-proxmox/pve-suivre-tache/consigne.md`.

## Ce qui est attendu

1. `/root/rapport-taches.txt` donne l'UPID exact des tâches de démarrage des
   VM 191 et 192.
2. Le démarrage de la 191 est noté `OK`, celui de la 192 porte le message
   d'erreur final de sa tâche.
3. L'état rapporté pour la 190 est son état actuel.
4. Les VM 191 et 192 sont supprimées, la 190 est intacte.

## Ce qui est prouvé

Les tests confrontent le rapport au registre des UPID gardé par le lab, lisent
le statut final de chaque tâche par l'API, l'état de la 190 par `qm status`,
et l'empreinte de sa configuration.
