# Challenge : un Proxmox VE que vous avez installé vous-même

Vous travaillez sur `pve.lab`, une Debian 13 nue. Le cahier des charges complet
est sur la machine, dans `/opt/lab-proxmox/cahier-des-charges.md`.

## Ce qui est attendu

1. Proxmox VE est installé, en version 9 ou plus, et `pveversion` répond.
2. Les services `pve-cluster`, `pvedaemon` et `pveproxy` sont actifs, et
   l'interface web répond sur le port 8006.
3. Le pont `vmbr0` existe et porte l'adresse IPv4 du serveur.
4. Le dépôt `pve-no-subscription` est configuré, et `apt-get update` passe.

## Ce qui est prouvé

Les tests interrogent la machine : la version installée, les services, le port
qui répond, l'adresse portée par le pont et le résultat réel d'`apt-get
update`. Ils ne lisent pas les commandes que vous avez tapées, et chaque poste
en défaut est nommé avec ce qu'il faut corriger.
