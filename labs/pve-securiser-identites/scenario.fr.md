# Scénario : Sécuriser les identités, jetons et connexions

## État initial

- Nœud et CA de laboratoire
- Compte humain et compte machine limités
- Accès console hors du réseau filtré
- Ressources attribuées : Compte automation-n2@pve et jeton à privilèges séparés lab-n2 ; VMID 202 comme seul périmètre ACL attribué.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Mettre en place les accès humains et machine avec confiance TLS, secours et rotation de token testés.

Configurez l’identité d’automatisation nommée, une voie humaine de secours et un jeton API à séparation de privilèges. Accordez uniquement le périmètre lecture/gestion d’énergie de la VM attribuée. Faites tourner le jeton : conservez son identifiant, remplacez son secret par la procédure PVE prévue et prouvez que l’ancien secret est refusé sans afficher les secrets. Gardez la vérification TLS active ; ne désactivez pas les contrôles de certificat et ne déposez aucun secret dans le dossier de preuves.

## Critères d’acceptation

- **tls** — Le client vérifie l’identité du nœud.
  - Vérification prévue : Réussir avec la CA prévue puis présenter un certificat de nom ou de chaîne incorrects ; la connexion doit être rejetée.
- **token** — Le token séparé n’hérite pas de droits supplémentaires.
  - Vérification prévue : Élargir les seuls droits du porteur dans une variante et vérifier le refus des actions non attribuées au token.
- **rotation** — Le nouveau token fonctionne et l’ancien est refusé.
  - Vérification prévue : Effectuer une opération légitime avant et après rotation, puis rejouer la requête avec l’ancien secret.
- **secours** — Le secours humain est documenté et testé.
  - Vérification prévue : Tester MFA puis la procédure de secours autorisée sans déposer de code de récupération dans le rapport.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
