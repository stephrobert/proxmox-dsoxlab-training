# Construire des templates et cloner avec cloud-init

## Mission

Produire un template versionné et deux clones distincts utilisables sans configuration manuelle après démarrage.

## État initial

- Image cloud avec empreinte
- Stockage compatible et snippets fournis
- Deux clés clientes distinctes générées par le setup et des VMID réservés (197 à 199)

## Contraintes

- N’agir que sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une configuration différente du corrigé est acceptée si elle respecte les contraintes et produit toutes les preuves.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.

## Critères d'acceptation

- **Le template est relié à son image et sa recette.** — Comparer empreinte de l’image, version de recette et identifiant du template via l’inventaire de l’évaluateur.
- **Les clones possèdent des identités indépendantes.** — Comparer VMID, MAC, machine-id, clés hôte et adresses ; refuser une duplication non prévue.
- **Chaque clone reçoit uniquement ses paramètres.** — Se connecter avec chaque clé et vérifier nom, service, cloud-init terminé et refus de la clé de l’autre clone.
- **Une recréation donne le même comportement attendu.** — Détruire un clone autorisé puis le recréer à partir de la recette ; ne pas accepter une correction manuelle résiduelle.

Les tests automatisés prouvent uniquement l'état observable du système. Les étapes nécessitant une observation humaine (provenance ISO, accès console ou panne imposée) doivent être revues séparément avant toute attestation.
