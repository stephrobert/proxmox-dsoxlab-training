# Scénario : Observer la capacité et recevoir les alertes

## État initial

- Nœud et invité sous charge bornée
- Récepteur de notifications local
- Volume de données jetable
- Ressources attribuées : Métriques réelles du nœud PVE ; récepteur local et charge invitée bornée fournis en externe.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Mettre en place la surveillance d’un service et de ses ressources critiques, puis provoquer et résoudre une alerte.

Configurez la chaîne de métriques/alertes PVE pour le service attribué et son volume de données jetable borné. Définissez un seuil avant saturation, configurez le récepteur local et faites franchir le seuil par la charge bornée fournie. Vérifiez un échantillon de métrique PVE réel et la réception de la notification. Résolvez la condition et observez le retour à la normale sans désactiver la surveillance. Un compte rendu saisi par l’apprenant ne prouve pas la réception.

## Critères d’acceptation

- **mesures** — Les mesures correspondent à la bonne ressource.
  - Vérification prévue : Comparer identité et valeurs à une lecture directe indépendante du dashboard.
- **detection** — Le défaut déclenche une alerte utile.
  - Vérification prévue : Franchir le seuil du volume jetable et mesurer l’apparition de l’alerte avec cause et ressource.
- **reception** — La notification atteint le récepteur.
  - Vérification prévue : Lire la réception côté service témoin ; une ligne envoyé dans le nœud ne suffit pas.
- **retour** — La résolution est observée et le contrôle reste actif.
  - Vérification prévue : Corriger la cause, attendre le retour sain puis réinjecter le défaut pour exclure une désactivation du monitoring.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
