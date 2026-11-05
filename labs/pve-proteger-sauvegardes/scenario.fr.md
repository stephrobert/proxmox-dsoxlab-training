# Scénario : Chiffrer, conserver et vérifier les sauvegardes

## État initial

- PBS et identité limitée
- Série de backups datés de fixture
- Coffre de clés de lab séparé
- Ressources attribuées : Stockage PBS lab-pbs-n2-208, VM 208, sauvegardes datées, identité limitée et coffre de clés hors ligne fournis.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Configurer chiffrement, rétention et vérification, puis prouver qu’une clé récupérée permet la restauration.

Utilisez uniquement PBS et le coffre de clés hors ligne fournis. Configurez le job de sauvegarde attribué avec chiffrement, rétention finie et vérification périodique. Restaurez une sauvegarde de test avec la clé récupérée, puis contrôlez le marqueur de données attendu. Lancez la vérification sur la fixture corrompue jetable fournie et confirmez qu’une tâche ou un enregistrement PBS/PVE rapporte l’échec. Ne déposez jamais la clé ni son contenu sur le nœud PVE.

## Critères d’acceptation

- **chiffrement** — La sauvegarde demandée est réellement chiffrée.
  - Vérification prévue : Inspecter son manifeste et tenter la lecture sur un client sans clé ; le transport TLS seul ne valide pas ce critère.
- **cle** — La clé récupérée restaure les bonnes données.
  - Vérification prévue : Utiliser un client vierge, récupérer la clé de secours puis restaurer le marqueur connu de l’évaluateur.
- **retention** — La politique conserve les points attendus.
  - Vérification prévue : Comparer la sélection sur des dates de fixture à la table attendue ; vérifier qu’un point protégé n’est pas supprimé.
- **verification** — Une corruption est détectée et signalée.
  - Vérification prévue : Utiliser une copie jetable de datastore altérée par l’évaluateur ; attendre un échec verify et une notification reçue, sans altérer le datastore sain.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
