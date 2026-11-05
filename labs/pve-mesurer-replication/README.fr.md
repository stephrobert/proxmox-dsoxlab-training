# Mesurer la réplication

Configurer la réplication ZFS et établir la séquence exacte récupérable.
Cible `proxmox-cluster` : `pve01.lab`, `node2=pve02.lab`, `node3=pve03.lab`, contrôleur/client
sur poste indépendant. [Scénario](scenario.fr.md), [consigne](challenge/README.fr.md).

```bash
dsoxlab run pve-mesurer-replication
dsoxlab check pve-mesurer-replication
dsoxlab clean pve-mesurer-replication
```

Setup exige PVE préparé, volumes ZFS qualifiés et VM avec journal durable ;
prérequis absents refusés clairement, sans provisionnement ni skip. Syntaxe
seulement, durée non calibrée. Réplication ne signifie ni RPO nul, ni backup/HA.
Nettoyage sans destruction de répliques, snapshots ou invités ; retour borné.
