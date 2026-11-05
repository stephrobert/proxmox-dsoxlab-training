# pve-reparer-agent

Rétablissez l’agent invité de la VM 180 tout en préservant la charge fournie.

## Exigences notées

1. Rétablissez un ping réussi de l’agent invité.
2. Activez le périphérique de l’agent invité dans la configuration de la VM 180.
3. Rendez présent /dev/virtio-ports/org.qemu.guest_agent.0 dans la VM 180.
4. Faites remonter 10.10.113.180 par l’agent, hors de l’interface de boucle locale.
5. Évitez toute tâche qmstop sur la VM 180 depuis le début du lab.
6. Conservez la page témoin de la VM 180 accessible avec sa ligne de session exacte.

Les contrôles de persistance effectuent un arrêt propre puis un démarrage et constatent les deux états. Les lectures impossibles refusent la mesure. Les contrôles de préservation ne sont comptés qu’une fois le rapport présent, le réseau rétabli ou l’agent joignable, selon le lab.

Pour vérifier l’origine de la page, l’évaluateur désactive temporairement l’interface virtuelle de l’invité, constate que le service devient inaccessible, puis restaure l’interface. Il ne modifie pas l’interface de gestion du nœud.
