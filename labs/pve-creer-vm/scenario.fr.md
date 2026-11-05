# Une VM à livrer, et un service qui doit répondre

Le nœud Proxmox est prêt. Une équipe vous demande une machine virtuelle pour y
héberger un petit service web, et elle a déjà réservé ses ressources : le
manifeste du lab, dans `/opt/lab-proxmox/pve-creer-vm/manifeste.md`, donne le
VMID, le stockage, l'ISO, le pont et l'adresse de la VM.

L'équipe ne se contentera pas d'une VM qui tourne. Elle veut une machine qui
**démarre sur son propre disque**, sans plus dépendre de l'ISO d'installation,
et un service qu'elle peut joindre **depuis son poste**, pas seulement depuis
la console de la VM.

## Mission

1. Créez la VM 150 avec le contrat matériel de la leçon : type de machine
   `q35`, firmware OVMF et son disque EFI, CPU `host`, contrôleur
   `VirtIO SCSI single`, carte réseau `VirtIO` sur `vmbr0`, au plus 2 cœurs et
   2048 Mo de RAM. Ses disques vont sur le stockage `local` : ce nœud n'a pas
   de `local-lvm`.
2. Installez le système invité. Debian 13 depuis l’ISO fournie est la méthode conseillée ; la distribution et la méthode ne sont pas notées séparément. Le résultat réseau et HTTP exigé est détaillé ci-dessous.
3. Une fois l'installation finie, retirez l'ISO et faites démarrer la VM sur
   son disque.
4. Dans la VM, mettez en service la page témoin décrite par le manifeste, sur
   le port 8080, et faites-la redémarrer avec la machine.

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

## Recommencer

`dsoxlab clean pve-creer-vm` détruit la VM 150 et ses disques. Le nœud et
l'ISO restent en place.

Pour vérifier l’origine de la page, l’évaluateur désactive temporairement l’interface virtuelle de l’invité, constate que le service devient inaccessible, puis restaure l’interface. Il ne modifie pas l’interface de gestion du nœud.
