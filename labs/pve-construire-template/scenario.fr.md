# Construire un template cloud-init et des clones indépendants

La préparation fournit une image cloud Debian 13 avec son SHA-512 publié, un snippet vendor qui installe le service témoin et deux clés clientes SSH distinctes. Elle ne crée ni template ni clone. Utilisez la VM 197 pour le template et les VM 198 et 199 pour les clones. Gardez un vCPU et 768 Mio par clone, la passerelle et le DNS 10.10.113.1 et le pont vmbr0. Ces bornes réservent la place nécessaire à la sonde de l’évaluateur.

Lisez le manifeste des ressources sur le nœud Proxmox dans `/opt/lab-proxmox/pve-construire-template/manifeste.md`, avec les privilèges d’administration. Il donne l’image, les lignes témoins exactes et, si nécessaire, les chemins des clés SSH. Le service ou le snippet vendor fourni produit le témoin ; aucun script de service n’est à écrire.

## Ce qui est noté

- Donnez à la VM 197 la description dsoxlab-lab=pve-construire-template.
- Donnez à la VM 198 la description dsoxlab-lab=pve-construire-template.
- Donnez à la VM 199 la description dsoxlab-lab=pve-construire-template.
- Convertissez la VM 197 en template PVE.
- Nommez le template 197 debian13-cloud-v1.
- Gardez le template 197 arrêté.
- Raccordez un disque cloud-init au template 197 sur ide2.
- Importez l'image vérifiée du manifeste sur scsi0 sans la démarrer ni la modifier avant conversion.
- Raccordez le snippet vendor cloud-init fourni au template 197 pour que ses clones en héritent.
- Nommez la VM 198 clone-a.
- Attribuez 10.10.113.198/24 par cloud-init à clone-a.
- Configurez uniquement la clé publique fournie pour clone-a comme clé cloud-init de la VM 198.
- Permettez à la clé attribuée à clone-a de se connecter à la VM 198 comme debian.
- Refusez la clé de l’autre clone lors de l’authentification sur clone-a.
- Donnez au système invité de la VM 198 le nom clone-a.
- Terminez cloud-init sans erreur dans clone-a.
- Servez la ligne témoin exacte du manifeste pour le VMID 198 depuis 10.10.113.198:8080.
- Nommez la VM 199 clone-b.
- Attribuez 10.10.113.199/24 par cloud-init à clone-b.
- Configurez uniquement la clé publique fournie pour clone-b comme clé cloud-init de la VM 199.
- Permettez à la clé attribuée à clone-b de se connecter à la VM 199 comme debian.
- Refusez la clé de l’autre clone lors de l’authentification sur clone-b.
- Donnez au système invité de la VM 199 le nom clone-b.
- Terminez cloud-init sans erreur dans clone-b.
- Servez la ligne témoin exacte du manifeste pour le VMID 199 depuis 10.10.113.199:8080.
- Donnez aux deux clones des adresses MAC distinctes.
- Donnez aux deux clones des valeurs machine-id distinctes.
- Donnez aux deux clones des clés hôte SSH distinctes.
- Faites démarrer un clone neuf et son service témoin depuis la recette du template, sans intervention manuelle dans l’invité.
- Configurez la VM 198 avec 768 Mio de mémoire.
- Configurez la VM 198 avec un vCPU.
- Configurez la VM 198 avec l’utilisateur cloud-init debian.
- Configurez la VM 198 avec le DNS 10.10.113.1.
- Configurez la VM 198 avec le pont vmbr0.
- Configurez la VM 198 avec la passerelle 10.10.113.1.
- Configurez la VM 199 avec 768 Mio de mémoire.
- Configurez la VM 199 avec un vCPU.
- Configurez la VM 199 avec l’utilisateur cloud-init debian.
- Configurez la VM 199 avec le DNS 10.10.113.1.
- Configurez la VM 199 avec le pont vmbr0.
- Configurez la VM 199 avec la passerelle 10.10.113.1.

L’évaluateur crée le clone complet temporaire 196 avec le profil clone-b et l’adresse 10.10.113.196, contrôle son service puis le supprime. Gardez ce VMID libre. Le snippet vendor est fourni par le lab ; vous n’avez pas à l’écrire. Les clés privées restent locales. L’image initiale et le disque du template doivent rester inchangés.

Compatibilité mesurée sur Proxmox VE 9.2.25 le 2026-11-06 : les données utilisateur cloud-init générées emploient le champ scalaire `user`, déprécié. Le contrôle exige le statut JSON `done`, aucune phase en échec et aucune erreur fatale. Le code 2 est admis uniquement pour l’avertissement exact de dépréciation de ce champ (dépréciation en 22.2, retrait prévu en 27.2, remplacement par la liste `users`). Tout autre avertissement ou toute autre erreur est refusé. Cet avertissement de la plateforme n’ajoute aucun travail à l’apprenant.
