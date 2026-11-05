# Réserver la capacité de reprise

Définir le placement et démontrer qu’une charge supplémentaire ne consomme pas
la réserve N-1. Cible `proxmox-cluster` : `pve01.lab`, `node2=pve02.lab`, `node3=pve03.lab`.
Le poste local est client/contrôleur indépendant.

```bash
dsoxlab run pve-reserver-capacite
dsoxlab check pve-reserver-capacite
dsoxlab clean pve-reserver-capacite
```

[Scénario](scenario.fr.md), [consigne](challenge/README.fr.md).
Setup exige explicitement nœuds/invités préparés et budgets, sans provisionnement
ni skip. Syntaxe locale seulement ; durée non calibrée, aucune attestation HA.
Nettoyage sans destruction de cluster, invités, disques ou backups.
