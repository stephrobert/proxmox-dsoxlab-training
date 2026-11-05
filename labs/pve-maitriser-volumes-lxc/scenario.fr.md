# Scénario : Gérer les volumes et identités des LXC

## État initial

- CT non privilégié et utilisateur applicatif
- Un volume géré et un bind mount contenant deux marqueurs
- Sauvegarde externe fournie
- Ressources attribuées : CT non privilégié jetable 384 nommé lab-n2-volumes ; volume géré lab-n2-volumes ; bind mount /srv/lab-n2-share.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Corriger un accès aux données d’un CT et prouver la restauration de tous les volumes demandés.

Sur le CT non privilégié 384 fourni, corrigez le mapping d’identifiants afin que seule l’identité applicative accède aux données. Préservez les restrictions du conteneur. Rendez explicites le volume géré et le bind mount, y compris leur périmètre de sauvegarde. Reconstruisez le CT depuis la sauvegarde fournie et vérifiez les deux marqueurs de données distincts dans le CT restauré. Si le CT ou son modèle attribué est absent, arrêtez-vous et signalez ce prérequis ; ne créez pas de remplacement sur un hôte partagé.

## Critères d’acceptation

- **identites** — Le mapping autorise uniquement le bon utilisateur.
  - Vérification prévue : Écrire via le service, lire propriétaire côté hôte et tester le refus pour un autre UID.
- **isolation** — Le CT conserve ses restrictions.
  - Vérification prévue : Contrôler unprivileged, features et permissions ; refuser privileged, montage système ou écriture globale.
- **perimetre** — Le périmètre de chaque sauvegarde est explicite.
  - Vérification prévue : Comparer manifeste et présence des deux marqueurs ; un rootfs restauré sans les données externes ne suffit pas.
- **restauration** — Le service retrouve ses données après reconstruction.
  - Vérification prévue : Restaurer le CT et sa sauvegarde complémentaire sur un réseau isolé, puis vérifier les marqueurs et les permissions.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
