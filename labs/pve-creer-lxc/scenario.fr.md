# Un service léger, dans un conteneur qui ne déborde pas

Une équipe veut héberger un petit service web, et une VM entière serait trop
lourde pour lui. Un conteneur LXC suffit, à trois conditions : qu'il reste
**non privilégié**, que ses **ressources soient bornées** pour ne pas gêner
ses voisins, et que le service ne tourne **pas sous root**.

Le manifeste du lab, dans `/opt/lab-proxmox/pve-creer-lxc/manifeste.md`,
donne le CTID, le modèle déjà téléchargé et vérifié, l'adresse, les limites et
la page à servir.

## Mission

1. Créez le conteneur 170 depuis le modèle Debian 13 du manifeste, non
   privilégié, avec 1 cœur, 512 Mo de RAM et pas de swap, sur `vmbr0` avec
   l'adresse du manifeste.
2. Dans le conteneur, installez `python3`, créez l'utilisateur système `web`,
   et servez la page témoin sur le port 8080 sous cet utilisateur.
3. Faites redémarrer le service avec le conteneur.

## Ce qui est noté

| # | Ce qui est vérifié | Comment |
|---|---|---|
| 1 | L'isolation | `unprivileged: 1`, et root du conteneur projeté sur un UID d'hôte au moins égal à 100000 |
| 2 | Le service | la page lue depuis le nœud porte le marqueur du conteneur, servie par l'utilisateur `web` |
| 3 | Les limites | la configuration ET les cgroups effectifs : 512 Mo de mémoire, un seul cœur, pas de swap |
| 4 | Le redémarrage | un fichier écrit avant le redémarrage est relu après, et la page revient seule |

## Recommencer

`dsoxlab clean pve-creer-lxc` détruit le conteneur 170. Le nœud et le modèle
restent en place.
