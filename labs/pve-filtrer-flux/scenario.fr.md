# Scénario : Filtrer le management et les invités

## État initial

- Nœud avec backend pare-feu identifié
- Trois positions de test indépendantes
- Services témoin connus ouverts avant filtrage
- Ressources attribuées : VMID 203 et son fichier pare-feu /etc/pve/firewall/203.fw ; aucun uplink physique ni réseau externe n’est attribué.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Appliquer une politique de flux minimale entre administration, invités et client non autorisé.

Activez le pare-feu PVE sur la VM attribuée et définissez une liste explicite des flux d’administration et invités autorisés. Gardez la politique entrante par défaut sur DROP et préservez la console indépendante. Laissez un service de test à l’écoute pendant la vérification des origines autorisées et refusées. Contrôlez l’état effectif du pare-feu, pas seulement un brouillon local.

## Critères d’acceptation

- **autorise** — Les flux nécessaires restent fonctionnels.
  - Vérification prévue : Tester API, console prévue et service depuis les bonnes origines avec une véritable réponse applicative.
- **interdit** — Les autres origines sont bloquées par la politique.
  - Vérification prévue : Garder le service en écoute et sonder depuis le client interdit en IPv4 et IPv6 quand ces piles sont activées.
- **activation** — Les règles sont appliquées aux bons niveaux.
  - Vérification prévue : Lire état du backend et compteurs ou logs correspondants ; un fichier de règles seul ne vaut pas validation.
- **persistance** — Le filtrage et le secours survivent au redémarrage.
  - Vérification prévue : Redémarrer le nœud de lab puis refaire la matrice et accéder à la console extérieure.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
