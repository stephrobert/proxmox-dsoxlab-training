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

## Exigences notées

1. Réglez la propriété hostname du conteneur 170 à ct-web.
2. Réglez la propriété unprivileged du conteneur 170 à 1.
3. Réglez la propriété memory du conteneur 170 à 512.
4. Réglez la propriété swap du conteneur 170 à 0.
5. Réglez la propriété cores du conteneur 170 à 1.
6. Créez le système de fichiers racine du conteneur sur le stockage local.
7. Réglez la propriété bridge de net0 du conteneur à vmbr0.
8. Réglez la propriété ip de net0 du conteneur à 10.10.113.170/24.
9. Réglez la propriété gw de net0 du conteneur à 10.10.113.1.
10. Configurez le DNS du conteneur à 10.10.113.1.
11. Gardez le conteneur 170 en marche.
12. Projetez l’UID 0 du conteneur sur un UID non privilégié de l’hôte, au moins égal à 100000.
13. Exécutez Debian 13 dans le conteneur.
14. Installez un python3 exécutable dans le conteneur.
15. Créez web comme compte système non root avec un UID inférieur à UID_MIN.
16. Servez la ligne témoin exacte de la session à l’adresse et au port du manifeste, accessible depuis le nœud.
17. Exécutez sous web le processus qui écoute réellement sur le port 8080 du conteneur.
18. Appliquez effectivement la valeur 536870912 au fichier cgroup memory.max.
19. Appliquez effectivement la valeur 0 au fichier cgroup memory.swap.max.
20. Limitez l’ensemble effectif des CPU du conteneur à exactement un CPU.
21. Préservez un fichier lors d’un arrêt propre puis d’un démarrage du conteneur ; l’évaluateur crée et retire ce fichier de mesure.
22. Faites revenir le service témoin du conteneur sans intervention après un arrêt propre et un démarrage.

Les contrôles de persistance effectuent un arrêt propre puis un démarrage et constatent les deux états. Les lectures impossibles refusent la mesure. Les contrôles de préservation ne sont comptés qu’une fois le rapport présent, le réseau rétabli ou l’agent joignable, selon le lab.

## Recommencer

`dsoxlab clean pve-creer-lxc` détruit le conteneur 170. Le nœud et le modèle
restent en place.

Pour vérifier l’origine de la page, l’évaluateur désactive temporairement l’interface virtuelle de l’invité, constate que le service devient inaccessible, puis restaure l’interface. Il ne modifie pas l’interface de gestion du nœud.
