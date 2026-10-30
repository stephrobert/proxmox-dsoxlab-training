# Challenge : une VM qui démarre sur son disque, et un service qui répond

Vous travaillez sur `pve.lab`. Le manifeste est dans
`/opt/lab-proxmox/pve-creer-vm/manifeste.md`.

## Ce qui est attendu

1. La VM 150 respecte le contrat matériel de la leçon : `q35`, OVMF avec
   `efidisk0`, CPU `host`, `virtio-scsi-single`, carte `virtio` sur `vmbr0`,
   au plus 2 cœurs et 2048 Mo.
2. Aucune ISO n'est insérée, `scsi0` est en tête de l'ordre de démarrage, et
   la VM tourne.
3. `http://10.10.113.150:8080/` sert la ligne témoin du manifeste.
4. Après un redémarrage de la VM, la page revient sans intervention.

## Ce qui est prouvé

Les tests lisent la configuration de la VM par `qm config`, interrogent le
service depuis le nœud, qui n'est pas l'invité, puis redémarrent la VM et
attendent que la page revienne. Ils ne lisent pas les commandes que vous avez
tapées.
