# Challenge : un conteneur non privilégié, borné, et un service qui n'est pas root

Vous travaillez sur `pve.lab`. Le manifeste est dans
`/opt/lab-proxmox/pve-creer-lxc/manifeste.md`.

## Ce qui est attendu

1. Le conteneur 170 est non privilégié et tourne.
2. `http://10.10.113.170:8080/` sert la ligne témoin, et le processus du
   service appartient à l'utilisateur `web`.
3. Le conteneur a 1 cœur, 512 Mo de RAM et pas de swap, et ces limites sont
   appliquées par ses cgroups.
4. Après un redémarrage du conteneur, un fichier écrit avant est toujours là,
   et la page revient seule.

## Ce qui est prouvé

Les tests lisent la configuration du conteneur, sa table d'UID et ses cgroups
depuis le nœud, interrogent le service depuis le nœud, puis redémarrent le
conteneur avant de vérifier le fichier et la page.
