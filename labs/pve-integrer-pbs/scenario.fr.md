# Scénario : Déployer PBS et réaliser une sauvegarde vérifiable

## État initial

- VM Debian dédiée au PBS
- Volume datastore distinct
- VM et CT contenant des données de référence
- Ressources attribuées : Stockage PVE lab-pbs-n2-207 ; endpoint/datastore PBS et workloads VM/CT fournis en externe.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Installer un PBS de lab, l’intégrer au nœud et sauvegarder deux charges avec des identités limitées.

Intégrez uniquement le point de terminaison et le datastore PBS attribués dans le manifeste. Utilisez son empreinte TLS enregistrée et une identité de sauvegarde dédiée au moindre privilège. Sauvegardez la VM et le CT nommés, avec leurs volumes déclarés, puis consultez l’inventaire réel des snapshots PBS. Confirmez la réutilisation/déduplication par les statistiques PBS, pas par une affirmation saisie. Si aucun endpoint/datastore PBS n’est fourni, arrêtez-vous : ce lab n’installe pas PBS et n’invente pas d’autre hôte.

## Critères d’acceptation

- **serveur** — Le PBS est joignable avec une identité TLS vérifiée.
  - Vérification prévue : Contrôler service, nom/certificat et refus d’un fingerprint incorrect depuis PVE.
- **droits** — Le compte de sauvegarde respecte le périmètre PBS.
  - Vérification prévue : Sauvegarder dans son namespace et tester une opération administrative ou un namespace voisin refusés.
- **contenu** — Les deux charges et leurs volumes prévus sont sauvegardés.
  - Vérification prévue : Lire jobs et manifestes puis restaurer un échantillon de chaque charge ; ne pas se contenter du nombre de snapshots.
- **incremental** — La réutilisation est mesurée et interprétée.
  - Vérification prévue : Rejouer puis modifier un fichier ; relever octets transférés/réutilisés sans imposer un ratio constant.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
