# Scénario : Exploiter un miroir ZFS et récupérer un disque

## État initial

- Deux disques de miroir et un remplacement autorisé
- Corpus à empreintes détenues par l’évaluateur
- Accès à la configuration ARC
- Ressources attribuées : Miroir ZFS jetable à deux disques labmirror-n2-214 et corpus empreinté ; le setup ne crée ni ne dégrade de pool.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Maintenir un service sur un miroir de lab dégradé puis retrouver une redondance saine.

Utilisez uniquement le miroir jetable à deux périphériques nommé. Identifiez le membre défaillant à partir de l’état ZFS réel, confirmez que les données du service restent lisibles en mode dégradé, remplacez uniquement le périphérique virtuel attribué et attendez la fin du resilver. Vérifiez que le pool est ONLINE, que le miroir possède deux membres sains et qu’aucune erreur de données ne subsiste. Précisez qu’un remplacement de périphérique virtuel ne simule pas une panne de disque physique. Si la fixture miroir dédiée manque, arrêtez-vous ; ne créez/n’altérez jamais un pool sur un disque de production.

## Critères d’acceptation

- **identification** — Le disque défaillant est correctement identifié.
  - Vérification prévue : Comparer GUID, chemin stable et manifeste extérieur avant toute opération de remplacement.
- **continuite** — Les données restent accessibles pendant la panne tolérée.
  - Vérification prévue : Lire le corpus par le service pendant le retrait d’un seul disque virtuel.
- **reconstruction** — Le resilver se termine et le pool redevient sain.
  - Vérification prévue : Attendre l’état final et vérifier redondance et empreintes, pas seulement le lancement de la commande.
- **limites** — Le rapport distingue expérience logique et panne matérielle.
  - Vérification prévue : Exiger le domaine de panne réel, les limites de la simulation et la lecture du paramétrage ARC sans valeur supposée.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
