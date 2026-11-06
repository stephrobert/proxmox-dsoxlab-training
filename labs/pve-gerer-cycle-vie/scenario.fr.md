# Redimensionner une VM et prouver un retour local

La VM applicative fonctionne avec 1 vCPU, 1024 Mio de mémoire et un disque système de 4 Gio. Préservez un point de retour local avant de lui allouer 2 vCPU, 2048 Mio et un disque de 8 Gio. Étendez aussi la partition et le système de fichiers dans Debian. Le témoin initial, l’agent invité et le réseau fixe sont fournis.

Lisez le manifeste des ressources sur le nœud Proxmox dans `/opt/lab-proxmox/pve-gerer-cycle-vie/manifeste.md`, avec les privilèges d’administration. Il donne l’image, les lignes témoins exactes et, si nécessaire, les chemins des clés SSH. Le service ou le snippet vendor fourni produit le témoin ; aucun script de service n’est à écrire.

## Ce qui est noté

- Configurez la VM 195 avec 2048 Mio de mémoire.
- Configurez la VM 195 avec deux vCPU.
- Configurez la VM 195 avec le démarrage automatique activé.
- Configurez la VM 195 avec l'ordre de démarrage 20.
- Faites fonctionner la VM 195 avec 2048 Mio de mémoire réellement alloués par QEMU.
- Faites fonctionner la VM 195 avec deux vCPU réellement alloués par QEMU.
- Portez la taille PVE du disque scsi0 à 8 Gio.
- Faites reconnaître un disque /dev/sda de 8 Gio par l'invité.
- Étendez le système de fichiers racine invité à au moins 7 Gio.
- Gardez la racine invitée inscriptible ; l'évaluateur écrit puis retire une sonde de 8 Mio.
- Créez avant-changement quand la VM possède encore 1024 Mio de mémoire.
- Créez avant-changement quand la VM possède encore un vCPU.
- Conservez le disque initial de 4 Gio dans avant-changement.
- Faites restituer le nonce initial dans /srv/temoin/retour.txt par avant-changement.
- Gardez le service de la VM 195 disponible sur 10.10.113.195:8080 avec la ligne témoin exacte du manifeste.
- Gardez le service témoin disponible après un arrêt propre puis un démarrage de la VM 195.

L’évaluateur écrit puis retire une sonde bornée, revient temporairement au snapshot, puis restitue tout l’état courant grâce à un snapshot temporaire. Il effectue aussi un redémarrage propre de l’invité. L’ordre de démarrage est contrôlé dans la configuration PVE ; aucun redémarrage du nœud n’est revendiqué. Un snapshot local ne protège pas contre la perte de son disque.
