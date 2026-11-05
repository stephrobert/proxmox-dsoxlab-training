# Scénario : Déléguer les droits sans élargir le périmètre

## État initial

- Deux pools et deux VM sentinelles
- Trois comptes de test
- Matrice des opérations autorisées et interdites
- Ressources attribuées : Pools lab-n2-deleguer et lab-n2-voisin ; VM sentinelles 201 et 216 ; comptes equipe-n2@pve, auditeur-n2@pve et secours-n2@pve.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Déléguer l’exploitation d’un pool à une équipe et conserver une séparation vérifiable avec le pool voisin.

Créez les deux pools et leurs VM sentinelles, puis attribuez un rôle de moindre privilège à `equipe-n2@pve` uniquement sur le pool attribué. Gardez le pool voisin et l’administration du nœud hors de cette ACL. Prouvez les autorisations et refus en interrogeant les permissions PVE effectives avec l’identité déléguée ; une ACL lue par root ne constitue pas une preuve d’accès effectif.

## Critères d’acceptation

- **positif** — L’opérateur effectue les gestes autorisés sur son pool.
  - Vérification prévue : Appeler réellement lecture, démarrage et arrêt avec son identité ; vérifier les résultats finaux des tâches.
- **negatif** — Les mêmes gestes échouent hors périmètre.
  - Vérification prévue : Tester VM voisine, console, stockage et administration sans utiliser le compte évaluateur comme sujet.
- **priorites** — La décision d’ACL est expliquée et reproduite.
  - Vérification prévue : Faire varier groupe, ACL plus spécifique et propagation dans une fixture bornée ; comparer prévision et réponse effective.
- **revocation** — Le retrait d’un accès coupe réellement les opérations.
  - Vérification prévue : Retirer le rattachement prévu puis retester avec les identifiants encore connus ; vérifier aussi les ACL orphelines.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
