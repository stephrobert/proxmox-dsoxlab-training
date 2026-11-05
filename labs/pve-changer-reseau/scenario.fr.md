# Scénario : Router, traduire et modifier le réseau sans se couper

## État initial

- Réseau extérieur simulé et réseau privé
- Console indépendante
- Service et route de secours documentés
- Ressources attribuées : VMID 206 ; pont isolé vmbr206 ; chaîne nftables N2LAB206 ; aucune route par défaut ni uplink physique.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Mettre en place les flux sortants et une publication contrôlée, puis effectuer un changement réseau réversible.

Utilisez le pont isolé et le réseau privé attribués. Configurez la translation sortante et ne publiez que le port de service indiqué dans une chaîne nftables dédiée. Conservez la route par défaut et le réseau d’administration. Préparez le changement volontairement erroné et prouvez que le retour par console indépendante restaure l’état PVE/réseau initial. Vérifiez la persistance des règles et l’absence de doublons après rechargement ; ne modifiez ni l’uplink, ni le lien cluster, ni la route par défaut.

## Critères d’acceptation

- **sortie** — Le client privé sort avec l’identité réseau prévue.
  - Vérification prévue : Observer source et destination sur le témoin extérieur ; contrôler la route et la traduction appliquées.
- **entree** — Le seul port publié atteint le bon service.
  - Vérification prévue : Tester réponse et nonce depuis l’extérieur, puis vérifier refus d’un port non publié avec son service pourtant actif.
- **retour** — Le changement erroné est annulé par le chemin prévu.
  - Vérification prévue : Injecter une mauvaise passerelle uniquement dans le lab et suivre le retour par console, sans intervention manuelle de l’évaluateur.
- **reboot** — La politique persiste sans doublons de règles.
  - Vérification prévue : Recharger puis redémarrer le nœud ; répéter les tests et vérifier qu’aucune règle répétée n’a été accumulée.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
