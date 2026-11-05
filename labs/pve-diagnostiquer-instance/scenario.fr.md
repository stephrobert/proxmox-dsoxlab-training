# Scénario : Diagnostiquer une VM indisponible

## État initial

- Instance avec une panne injectée parmi boot, réseau, agent ou volume de test
- Logs accessibles
- Sentinelles de données et de sécurité
- Ressources attribuées : VM jetable préinstallée 211 nommée n2-diagnostique avec disque, agent invité et pare-feu ; panne injectée unique sur vmbr999.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Rétablir une instance indisponible en identifiant la cause et en conservant ses données et protections.

Examinez la VM 211 fournie et l’état des tâches/journaux PVE avant toute modification. La fixture injecte une panne de pont réseau. Identifiez et corrigez cette panne sans remplacer la VM, supprimer son disque ni affaiblir son pare-feu/agent. Vérifiez que la VM fonctionne, que son disque reste attaché, que le pont attribué est rétabli et que l’agent invité répond après le redémarrage pertinent.

## Critères d’acceptation

- **diagnostic** — La cause retenue correspond à la panne injectée.
  - Vérification prévue : Comparer les observations datées et le registre de faute extérieur ; le texte cause corrigée ne suffit pas.
- **service** — Le service cible est réellement rétabli.
  - Vérification prévue : Contrôler une transaction et le nonce depuis le client externe.
- **integrite** — Les données et contrôles de sécurité sont préservés.
  - Vérification prévue : Vérifier les marqueurs, le firewall et les ACL ; refuser recréation destructive, privileged ou désactivation générale.
- **durable** — La réparation résiste au redémarrage pertinent.
  - Vérification prévue : Redémarrer le composant concerné puis refaire la recette ; ne pas exiger un reboot hôte sans rapport avec le défaut.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
