# Un agent qui ne répond pas, et une VM qu'on ne coupe pas

La VM 180 sert une page à une équipe, et son service fonctionne. Mais Proxmox
ne voit pas son adresse, la sauvegarde ne peut pas geler ses systèmes de
fichiers, et `qm agent 180 ping` échoue : l'**agent invité QEMU** ne répond
pas.

Deux causes sont possibles, et le lab en a tiré une au hasard. Le manifeste,
dans `/opt/lab-proxmox/pve-reparer-agent/manifeste.md`, donne l'adresse de la
VM et la façon d'y entrer.

## Mission

1. Trouvez pourquoi l'agent ne répond pas. Regardez des deux côtés : la
   configuration de la VM dans Proxmox, et l'invité lui-même.
2. Corrigez la cause. Si la VM doit redémarrer, faites-le **proprement** : sa
   charge doit se fermer correctement, comme sur un vrai serveur.
3. Vérifiez depuis le nœud que l'agent répond et remonte l'adresse de la VM.

## Ce qui est noté

| # | Ce qui est vérifié | Comment |
|---|---|---|
| 1 | L'agent | périphérique activé, `qm agent 180 ping` répond, canal présent dans l'invité |
| 2 | L'adresse | l'agent remonte `10.10.113.180`, en ignorant la boucle locale |
| 3 | L'intégrité de la charge | aucune tâche `qmstop` (arrêt forcé) depuis le début du lab, et la page témoin répond avec les données de la session |

## Recommencer

`dsoxlab clean pve-reparer-agent` détruit la VM 180. Un nouveau `run` tire une
nouvelle panne, peut-être l'autre.
