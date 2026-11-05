# Scénario : Segmenter et diagnostiquer les VLAN

## État initial

- Deux VLAN disponibles dans un lab fermé
- Routeur de fixture
- Clients et service avec ports identifiés
- Ressources attribuées : VMID 205 ; pont isolé vmbr205 ; VLAN 285 et 286 ; aucun uplink physique.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Construire deux segments et appliquer une exception routée explicite sans exposer le management.

Créez les segments VLAN isolés 285 et 286 sur le pont de lab nommé, affectez les cartes de test à leurs tags attendus et n’implémentez que la route inter-VLAN demandée. Gardez l’administration sur son chemin initial. Corrigez le tag invité erroné, puis vérifiez la configuration effective des cartes/ponts PVE et la matrice de connectivité. Ne modifiez pas l’uplink physique et ne redémarrez pas le réseau de l’hôte.

## Critères d’acceptation

- **l2** — Les trames restent dans le VLAN attendu.
  - Vérification prévue : Comparer bridge vlan show et captures sur les points prévus ; vérifier la communication intra-VLAN.
- **routage** — Seul le flux inter-VLAN demandé passe.
  - Vérification prévue : Tester un port autorisé et un port refusé sur le même service sans supprimer la route.
- **management** — Le réseau des invités ne donne pas accès au management.
  - Vérification prévue : Sonder les services d’administration depuis chaque segment et conserver l’accès du poste admin.
- **diagnostic** — Une erreur de tag est localisée puis corrigée.
  - Vérification prévue : Injecter un tag non autorisé et demander une capture avant correction ; vérifier ensuite la matrice complète.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
