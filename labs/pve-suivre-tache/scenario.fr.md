# Ce qui s'est passé sur ce nœud, et ce qui est vrai maintenant

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

## Exigences notées

1. Rapportez l’UPID exact de la tâche de démarrage de la VM 191.
2. Rapportez l’UPID exact de la tâche de démarrage de la VM 192.
3. Rapportez le résultat final complet de la tâche de démarrage de la VM 191, sans modifier son texte.
4. Rapportez le résultat final complet de la tâche de démarrage de la VM 192, sans modifier son texte.
5. Rapportez l’état actuel de la VM 190, plutôt que le résultat de son ancien démarrage.
6. Supprimez la VM temporaire 191.
7. Supprimez la VM temporaire 192.
8. Conservez la VM sentinelle 190.
9. Préservez la configuration initiale de la VM sentinelle 190.

Les contrôles de persistance effectuent un arrêt propre puis un démarrage et constatent les deux états. Les lectures impossibles refusent la mesure. Les contrôles de préservation ne sont comptés qu’une fois le rapport présent, le réseau rétabli ou l’agent joignable, selon le lab.

## Recommencer

`dsoxlab clean pve-suivre-tache` retire les trois VM et le rapport. Un nouveau
`run` déclenche des tâches neuves, avec de nouveaux UPID.
