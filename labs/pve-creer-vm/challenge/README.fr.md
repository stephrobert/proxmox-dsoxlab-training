# pve-creer-vm

Créez la VM 150 et son service HTTP témoin. Le lab fournit un installateur Debian 13 comme méthode d’installation conseillée ; la distribution et la méthode d’installation ne sont pas notées séparément. Le résultat exigé est détaillé ci-dessous.

## Exigences notées

1. Réglez la propriété name de la VM 150 à web-temoin.
2. Réglez la propriété machine de la VM 150 à q35.
3. Réglez la propriété bios de la VM 150 à ovmf.
4. Réglez la propriété cpu de la VM 150 à host.
5. Réglez la propriété scsihw de la VM 150 à virtio-scsi-single.
6. Créez le disque efidisk0 de la VM 150 sur le stockage local.
7. Créez le disque scsi0 de la VM 150 sur le stockage local.
8. Utilisez le modèle VirtIO pour net0 de la VM 150.
9. Rattachez net0 de la VM 150 au pont exact vmbr0.
10. Attribuez à la VM 150 une quantité positive de mémoire, au plus 2048 Mo.
11. Attribuez à la VM 150 un nombre positif de CPU virtuels, au plus deux.
12. Retirez l’ISO d’installation de la VM 150.
13. Placez scsi0 en tête de l’ordre de démarrage de la VM 150.
14. Gardez la VM 150 en marche.
15. Servez la ligne témoin exacte de la session à l’adresse et au port du manifeste, accessible depuis le nœud.
16. Faites revenir le service témoin de la VM sans intervention après un arrêt propre et un démarrage effectués par l’évaluateur.

Les contrôles de persistance effectuent un arrêt propre puis un démarrage et constatent les deux états. Les lectures impossibles refusent la mesure. Les contrôles de préservation ne sont comptés qu’une fois le rapport présent, le réseau rétabli ou l’agent joignable, selon le lab.

Pour vérifier l’origine de la page, l’évaluateur désactive temporairement l’interface virtuelle de l’invité, constate que le service devient inaccessible, puis restaure l’interface. Il ne modifie pas l’interface de gestion du nœud.
