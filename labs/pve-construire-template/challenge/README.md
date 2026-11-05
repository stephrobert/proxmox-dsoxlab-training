# What is expected

Produire un template versionné et deux clones distincts utilisables sans configuration manuelle après démarrage.

# What is proven

- **Le template est relié à son image et sa recette.** — Comparer empreinte de l’image, version de recette et identifiant du template via l’inventaire de l’évaluateur.
- **Les clones possèdent des identités indépendantes.** — Comparer VMID, MAC, machine-id, clés hôte et adresses ; refuser une duplication non prévue.
- **Chaque clone reçoit uniquement ses paramètres.** — Se connecter avec chaque clé et vérifier nom, service, cloud-init terminé et refus de la clé de l’autre clone.
- **Une recréation donne le même comportement attendu.** — Détruire un clone autorisé puis le recréer à partir de la recette ; ne pas accepter une correction manuelle résiduelle.

Criteria requiring human observation need a separate review before attestation.
