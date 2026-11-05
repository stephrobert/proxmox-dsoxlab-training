# pve-creer-lxc

Créez le conteneur 170 à partir du modèle Debian 13 fourni et exécutez son service HTTP témoin sous web.

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

Pour vérifier l’origine de la page, l’évaluateur désactive temporairement l’interface virtuelle de l’invité, constate que le service devient inaccessible, puis restaure l’interface. Il ne modifie pas l’interface de gestion du nœud.
