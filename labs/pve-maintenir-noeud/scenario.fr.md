# Scénario : Maintenir un nœud et préparer une montée de version

## État initial

- Copie jetable de nœud sur version qualifiée
- Paquets et guide de changement sélectionnés
- Backups vérifiés et console
- Ressources attribuées : Copie jetable du nœud PVE, version qualifiée, sauvegardes vérifiées et console ; aucun VMID ni paquet n’est modifié par le setup.
- Le manifeste du setup consigne les ressources ; ne substituez pas une ressource voisine.

## Mission

Maintenir un nœud de laboratoire avec précontrôles, recette et procédure de reprise documentée.

Utilisez uniquement le nœud jetable et qualifié par version nommé dans le manifeste. Exécutez le précontrôle adapté à la version et consignez son résultat réel avant maintenance ; levez les blocages ou arrêtez-vous. Appliquez uniquement le changement de paquets préapprouvé, puis vérifiez la version du nœud, la santé cluster/API, les charges représentatives et l’accès aux sauvegardes. Le test ne fait que lire l’état PVE et ne met jamais à niveau le nœud. Si le nœud jetable et les sauvegardes vérifiées ne sont pas fournis, ne tentez pas de mise à niveau sur un nœud partagé.

## Critères d’acceptation

- **precontrole** — Les incompatibilités bloquantes sont détectées.
  - Vérification prévue : Présenter une fixture avec défaut de capacité ou dépôt ; vérifier le no-go sans commencer la modification.
- **version** — La version active correspond au changement prévu.
  - Vérification prévue : Lire paquets, noyau démarré et services après redémarrage, pas seulement le journal apt.
- **recette** — Les charges, accès et sauvegardes fonctionnent après maintenance.
  - Vérification prévue : Rejouer un sous-ensemble représentatif de tests applicatifs, RBAC et backup.
- **reprise** — Une panne de maintenance possède un chemin de retour éprouvé.
  - Vérification prévue : Sur copie dédiée, appliquer la reconstruction ou restauration prévue et vérifier la récupération des charges.

Les tests exécutables ne couvrent que l’état observable depuis la cible PVE attribuée. La procédure humaine, la provenance des preuves, la cohérence métier et la revue de sécurité restent des contrôles explicites de l’opérateur ; un test vert ne constitue pas une attestation du lab.

## Contraintes du contrat

- Agir uniquement sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une autre configuration convient si elle respecte les contraintes et produit les états observés attendus.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.
- Garder la vérification TLS/SSH sur le chemin nominal. Toute exception d’expérience doit rester bornée et être supprimée avant l’acceptation.

## Limites et nettoyage

Ne touchez ni aux VMID non attribués, ni aux uplinks physiques, à la configuration cluster, au stockage de production, aux identifiants ou aux disques non attribués. Gardez la vérification TLS/SSH. Arrêtez-vous si un prérequis externe déclaré manque. Exécutez `cleanup.yaml` uniquement après avoir conservé les preuves nécessaires.
