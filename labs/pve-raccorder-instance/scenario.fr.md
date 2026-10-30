# Une VM qui tourne, et que personne ne joint

La VM témoin 160 a été livrée hier. Proxmox la montre en marche, son service
écoute sur le port 8080, et pourtant l'équipe qui doit s'en servir ne la joint
pas : `http://10.10.113.160:8080/` ne répond pas, ni depuis son poste, ni
depuis le nœud.

Le manifeste du lab, dans `/opt/lab-proxmox/pve-raccorder-instance/manifeste.md`,
donne l'adresse réservée et le réseau du lab. Le disque de la VM porte la page
témoin de cette session : recréer la VM ne la rendrait pas.

## Mission

1. Depuis le nœud, trouvez pourquoi la VM est injoignable. Regardez le trajet
   dans l'ordre : la carte de la VM, le pont auquel elle est branchée, puis ce
   que ce pont relie.
2. Corrigez au bon étage : c'est la carte de **cette** VM qui doit rejoindre
   `vmbr0`. Ne recréez pas la VM, et ne donnez pas de carte physique au pont
   isolé.
3. Vérifiez depuis le nœud que la page témoin répond.

## Ce qui est noté

| # | Ce qui est vérifié | Comment |
|---|---|---|
| 1 | La topologie | `net0` porte `bridge=vmbr0`, et `tap160i0` est un port effectif de `vmbr0` |
| 2 | La bonne instance | la page lue depuis le nœud contient le nonce de la session |
| 3 | Le bon étage | la VM est joignable, et le pont isolé n'a reçu aucun port physique |
| 4 | La persistance | après un redémarrage de l'invité et un `ifreload -a` du nœud, la page revient |

## Recommencer

`dsoxlab clean pve-raccorder-instance` détruit la VM 160 et retire le pont
isolé. Le nœud reste en place.
