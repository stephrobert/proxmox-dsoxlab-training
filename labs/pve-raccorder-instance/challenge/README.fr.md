# Challenge : rebrancher une VM sur le bon pont

Vous travaillez sur `pve.lab`. Le manifeste est dans
`/opt/lab-proxmox/pve-raccorder-instance/manifeste.md`.

## Ce qui est attendu

1. La carte `net0` de la VM 160 est sur `vmbr0`, et `tap160i0` est un port
   effectif de ce pont.
2. `http://10.10.113.160:8080/` sert la ligne témoin de la session.
3. Le pont isolé `vmbr9` n'a reçu aucun port physique, et la VM n'a pas été
   recréée.
4. Après un redémarrage de la VM et un `ifreload -a` du nœud, la page revient.

## Ce qui est prouvé

Les tests lisent la configuration de la VM et les ports effectifs des ponts,
interrogent le service depuis le nœud, puis redémarrent l'invité et rechargent
le réseau du nœud avant de l'interroger de nouveau.
