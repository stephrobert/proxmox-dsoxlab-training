# Scénario : Restaurer un service et mesurer RPO et RTO

## État initial

- Sauvegarde contenant données et dépendance déclarées
- Journal d’écritures détenu par l’évaluateur
- Réseau de restauration sans accès production
- Ressources attribuées : VM de reprise vide 209 nommée n2-restored-209 ; stockage PBS lab-pbs-n2-209 ; sauvegarde/journal évaluateur et réseau de reprise isolé.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Rétablir une application depuis PBS avec source indisponible et rendre un bilan de reprise vérifiable.

Restaurez la charge attribuée sur le réseau de reprise isolé alors que les volumes source sont indisponibles. Validez l’application à l’aide du journal d’écritures détenu par l’évaluateur et relevez le dernier enregistrement confirmé comme preuve du RPO. Mesurez le RTO à partir des horodatages observés des tâches jusqu’à la disponibilité applicative, pas d’une estimation saisie. Vérifiez que la VM de production et les ressources voisines restent inchangées. Si les fixtures PBS/de reprise manquent, arrêtez-vous et signalez le prérequis manquant.

## Critères d’acceptation

- **source-absente** — La reprise fonctionne sans les volumes initiaux.
  - Vérification prévue : Retirer l’accès au volume source avant le lancement ; vérifier les identifiants des volumes restaurés.
- **donnees** — L’application retrouve un état métier cohérent.
  - Vérification prévue : Exécuter lecture et écriture applicatives, vérifier les relations et les marqueurs sauvegardés.
- **mesures** — Les RPO/RTO viennent des observations.
  - Vérification prévue : Comparer timestamps de la sonde externe, séquence d’écritures et dernier point restauré ; ne pas accepter un temps saisi sans trace.
- **isolement** — La recette ne modifie aucune charge voisine.
  - Vérification prévue : Contrôler réseau isolé, secrets de test et intégrité d’une sentinelle avant/après.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
