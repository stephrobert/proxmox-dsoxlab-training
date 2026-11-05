# verifier-son-installation

Installez Proxmox VE sur le nœud Debian nu. Debian, KVM, le dimensionnement du nœud et le second disque brut sont des prérequis fournis, pas du travail noté.

## Exigences notées

1. Installez Proxmox VE pour que pveversion annonce pve-manager.
2. Utilisez Proxmox VE en version 9 ou ultérieure.
3. Gardez le service pve-cluster actif.
4. Gardez le service pvedaemon actif.
5. Gardez le service pveproxy actif.
6. Servez une réponse HTTP 200 en HTTPS sur le port 8006.
7. Faites tenir le port 8006 par pveproxy.
8. Placez sur vmbr0 l’adresse IPv4 du serveur, résolue depuis son nom d’hôte.
9. Activez une entrée APT complète du dépôt pve-no-subscription.
10. Téléchargez tous les index APT sans ignorer une erreur de téléchargement d’un dépôt.

Les contrôles de persistance effectuent un arrêt propre puis un démarrage et constatent les deux états. Les lectures impossibles refusent la mesure. Les contrôles de préservation ne sont comptés qu’une fois le rapport présent, le réseau rétabli ou l’agent joignable, selon le lab.
