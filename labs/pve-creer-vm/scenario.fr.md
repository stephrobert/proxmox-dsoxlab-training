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
2. Installez Debian depuis l'ISO fournie, avec l'adresse statique du manifeste.
3. Une fois l'installation finie, retirez l'ISO et faites démarrer la VM sur
   son disque.
4. Dans la VM, mettez en service la page témoin décrite par le manifeste, sur
   le port 8080, et faites-la redémarrer avec la machine.

## Ce qui est noté

| # | Ce qui est vérifié | Comment |
|---|---|---|
| 1 | Le contrat matériel | la configuration de la VM, lue par `qm config` |
| 2 | Le démarrage sur disque | aucune ISO insérée, `scsi0` en tête de l'ordre de démarrage, VM en marche |
| 3 | Le service | la page lue depuis le nœud contient la ligne témoin du manifeste |
| 4 | La tenue au redémarrage | la VM est redémarrée, et la page revient seule |

Le lab ne regarde pas comment vous avez installé Debian : seul compte l'état
obtenu.

## Recommencer

`dsoxlab clean pve-creer-vm` détruit la VM 150 et ses disques. Le nœud et
l'ISO restent en place.
