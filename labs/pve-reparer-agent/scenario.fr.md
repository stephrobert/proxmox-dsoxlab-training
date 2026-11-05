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

## Exigences notées

1. Rétablissez un ping réussi de l’agent invité.
2. Activez le périphérique de l’agent invité dans la configuration de la VM 180.
3. Rendez présent /dev/virtio-ports/org.qemu.guest_agent.0 dans la VM 180.
4. Faites remonter 10.10.113.180 par l’agent, hors de l’interface de boucle locale.
5. Évitez toute tâche qmstop sur la VM 180 depuis le début du lab.
6. Conservez la page témoin de la VM 180 accessible avec sa ligne de session exacte.

Les contrôles de persistance effectuent un arrêt propre puis un démarrage et constatent les deux états. Les lectures impossibles refusent la mesure. Les contrôles de préservation ne sont comptés qu’une fois le rapport présent, le réseau rétabli ou l’agent joignable, selon le lab.

## Recommencer

`dsoxlab clean pve-reparer-agent` détruit la VM 180. Un nouveau `run` tire une
nouvelle panne, peut-être l'autre.

Pour vérifier l’origine de la page, l’évaluateur désactive temporairement l’interface virtuelle de l’invité, constate que le service devient inaccessible, puis restaure l’interface. Il ne modifie pas l’interface de gestion du nœud.
