# Livrer et restaurer un premier service virtualisé

## Mission

À partir d’un nœud vide installé par vos soins, livrer une VM et un CT Linux répondant au cahier des charges, puis restaurer les données du service dans une nouvelle instance.

## État initial

- ISO et disque cible identifiés, console extérieure accessible
- Plan d’adressage réservé, images et service de test fournis
- Destination de sauvegarde indépendante du disque des instances ; aucun PBS à configurer dans cette épreuve
- Nœud Proxmox VE installé par l'apprenant, modèle Debian 13 attribué et bridge isolé de restauration disponible

## Contraintes

- Ne pas utiliser une image PVE déjà installée pour valider l’installation.
- La recette accède aux services depuis un client extérieur ; aucun succès fondé seulement sur l’état running.
- Le RPO/RTO de cette première épreuve est observé et expliqué ; les exigences avancées de N2 ne sont pas anticipées.

## Critères d'acceptation

- **Le nœud démarre sur le disque attendu, présente les versions et réseaux documentés et conserve un accès de secours.** — Inspecter installation, stockage et accès après redémarrage ; vérifier que les disques hors périmètre n’ont pas été touchés.
- **VM et CT non privilégié exécutent les services demandés avec des identités distinctes.** — Créer une transaction avec nonce depuis le client dans chaque invité, comparer identités réseau et machine, vérifier l’isolation du CT.
- **L’agent fonctionne et une modification de ressources est appliquée sans perte de données.** — Observer le canal agent, une extinction propre et la ressource réellement utilisable dans l’invité ; un simple changement de configuration ne suffit pas.
- **Une nouvelle instance restaurée contient les données attendues et rend le service.** — Produire des données horodatées, sauvegarder, rendre la source inaccessible puis restaurer sous un nouvel identifiant sur réseau isolé ; contrôler le contenu depuis le client.
- **Un autre opérateur peut retrouver la topologie et rejouer les vérifications.** — Suivre le dossier remis sans utiliser l’historique du terminal de l’élève ; vérifier limites, captures de preuve et nettoyage du périmètre autorisé.

Les tests automatisés prouvent uniquement l'état observable du système. Les étapes nécessitant une observation humaine (provenance ISO, accès console ou panne imposée) doivent être revues séparément avant toute attestation.
