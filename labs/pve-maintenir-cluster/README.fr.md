# Maintenir le cluster

Effectuer une maintenance autorisée, préserver le contrat de service et revenir
à un cluster sain. Cible `proxmox-cluster` : `pve01.lab`, rôles `node2=pve02.lab`,
`node3=pve03.lab` ; contrôleur/sonde locale indépendante.

```bash
dsoxlab run pve-maintenir-cluster
dsoxlab check pve-maintenir-cluster
dsoxlab clean pve-maintenir-cluster
```

[Scénario](scenario.fr.md), [consigne](challenge/README.fr.md).
Setup exige cluster préparé/stable, backups contrôlés et changement autorisé ;
refus explicites, ni provisionnement ni skip. Syntaxe locale seulement,
aucune exécution/attestation ; durée non calibrée. Backups/invités préservés.
