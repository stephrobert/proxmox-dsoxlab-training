# Ce qui s'est passé sur ce nœud, et ce qui est vrai maintenant

## La situation

Un collègue a manipulé trois VM sur ce nœud avant de partir : la sentinelle
190, et deux VM temporaires, 191 et 192. Il vous laisse une question simple,
« qu'est-ce qui a marché, et qu'est-ce qui n'a pas marché ? », et un nœud à
remettre en ordre.

La consigne, dans `/opt/lab-proxmox/pve-suivre-tache/consigne.md`, donne le
modèle du rapport attendu.

## Mission

1. Retrouvez la tâche de démarrage de la VM 191 et celle de la VM 192, par
   leur **UPID**, l'identifiant unique que Proxmox donne à chaque tâche.
2. Pour chacune, relevez son **résultat final** : `OK`, ou le message d'erreur
   que Proxmox a enregistré à la fin de la tâche.
3. Donnez l'**état actuel** de la sentinelle 190.
4. Écrivez le tout dans `/root/rapport-taches.txt`, puis supprimez les VM 191
   et 192 sans toucher à la 190.

## Ce qui est noté

| # | Ce qui est vérifié | Comment |
|---|---|---|
| 1 | La corrélation | chaque UPID du rapport est celui de la bonne tâche de démarrage |
| 2 | L'échec | le démarrage de la 192 n'est pas noté OK, et sa cause correspond au message final de la tâche |
| 3 | L'état courant | l'état rapporté pour la 190 est son état actuel, pas celui de son vieux journal |
| 4 | La propreté | la 191 et la 192 n'existent plus, la 190 existe et sa configuration n'a pas changé |

## Recommencer

`dsoxlab clean pve-suivre-tache` retire les trois VM et le rapport. Un nouveau
`run` déclenche des tâches neuves, avec de nouveaux UPID.

## Un rapport de tâches juste, et un nœud remis en ordre

Vous travaillez sur `pve.lab`. La consigne est dans
`/opt/lab-proxmox/pve-suivre-tache/consigne.md`.

### Ce qui est attendu

1. `/root/rapport-taches.txt` donne l'UPID exact des tâches de démarrage des
   VM 191 et 192.
2. Le démarrage de la 191 est noté `OK`, celui de la 192 porte le message
   d'erreur final de sa tâche.
3. L'état rapporté pour la 190 est son état actuel.
4. Les VM 191 et 192 sont supprimées, la 190 est intacte.

### Ce qui est prouvé

Les tests confrontent le rapport au registre des UPID gardé par le lab, lisent
le statut final de chaque tâche par l'API, l'état de la 190 par `qm status`,
et l'empreinte de sa configuration.
