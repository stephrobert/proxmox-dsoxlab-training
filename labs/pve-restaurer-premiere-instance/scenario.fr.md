# Sauvegarder et restaurer une première VM sur un réseau isolé

La VM source 198 sert déjà un témoin propre à la session sur 10.10.113.198:8080. La préparation fournit le pont isolé vmbr9 et le client dsox-restore (10.10.113.240/24). Sauvegardez dans /var/lib/vz/dump/pve-restaurer-premiere-instance puis restaurez vers la VM 199. Gardez l’adresse IP de l’invité restauré : source et restauration utilisent des segments Ethernet distincts. Ne raccordez pas le pont isolé au réseau de l’hôte.

Lisez le manifeste des ressources sur le nœud Proxmox dans `/opt/lab-proxmox/pve-restaurer-premiere-instance/manifeste.md`, avec les privilèges d’administration. Il donne l’image, les lignes témoins exactes et, si nécessaire, les chemins des clés SSH. Le service ou le snippet vendor fourni produit le témoin ; aucun script de service n’est à écrire.

## Ce qui est noté

- Gardez la VM restaurée 199 sans interface réseau supplémentaire.
- Gardez la description dsoxlab-lab=pve-restaurer-premiere-instance sur la VM restaurée 199.
- Conservez une seule sauvegarde VMA/Zstandard complète et lisible de la VM 198 dans le répertoire attribué.
- Incluez le disque système scsi0 complet de 4 Gio dans l’archive de sauvegarde.
- Terminez une tâche PVE de restauration réussie vers le VMID 199 après la préparation du lab.
- Restaurez un disque système distinct et complet, sans fichier de base partagé.
- Faites fonctionner la VM restaurée 199.
- Raccordez la VM restaurée 199 uniquement par net0 sur le pont isolé vmbr9.
- Donnez à la VM restaurée une adresse MAC différente de celle de la source.
- Restaurez la ligne témoin initiale du manifeste dans /srv/temoin/index.html.
- Servez le témoin restauré en HTTP sur le port 8080 au client isolé dsox-restore.
- Gardez le service restauré fonctionnel après son redémarrage pendant que la VM source est arrêtée.
- Préservez la configuration PVE initiale de la VM source 198.
- Préservez le service témoin initial de la VM source 198.
- Gardez les interfaces physiques hors de vmbr9.
- Gardez le client isolé dsox-restore incapable de joindre le service HTTPS de gestion du nœud sur le port 8006.

L’évaluateur lit le VMA à travers une décompression dont les erreurs sont contrôlées. Il arrête temporairement la source, redémarre la VM restaurée, contrôle le service depuis le client isolé, puis redémarre la source. Le disque source n’est pas supprimé. Les contrôles de préservation exigent d’abord une VM restaurée.
