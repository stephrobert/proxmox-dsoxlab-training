# Migrer une VM et un CT

Déplacer VM et CT selon leurs méthodes supportées, préserver les données et
mesurer l’impact client extérieur. Cible `proxmox-cluster` ancrée sur `pve01.lab`,
rôles `node2=pve02.lab`, `node3=pve03.lab` ; poste local comme client indépendant.

```bash
dsoxlab run pve-migrer-instance
dsoxlab check pve-migrer-instance
dsoxlab clean pve-migrer-instance
```

[Scénario](scenario.fr.md), [allocation/consigne](challenge/README.fr.md).
Setup exige nœuds préinstallés, destinations qualifiées et services VM/CT préparés ;
il refuse explicitement, sans provisionnement ni skip. Syntaxe locale seulement,
aucune garantie de zéro interruption ni attestation PVE. Durée non calibrée.
Le nettoyage ne détruit jamais les invités ni leurs disques.
