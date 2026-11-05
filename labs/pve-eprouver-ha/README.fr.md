# Éprouver la HA

Mesurer une vraie perte imposée du nœud porteur et la reprise durable du service
sans double démarrage ni quorum contourné. Cible `proxmox-cluster` : `pve01.lab`, rôles
`node2=pve02.lab`, `node3=pve03.lab` ; client/contrôleur local indépendant.

```bash
dsoxlab run pve-eprouver-ha
dsoxlab check pve-eprouver-ha
dsoxlab clean pve-eprouver-ha
```

[Scénario](scenario.fr.md), [consigne](challenge/README.fr.md).
Cluster préparé, stockage/réserve qualifiés, watchdog documenté et secours sont
des prérequis, jamais provisionnés par le setup. Absences refusées explicitement.
Syntaxe locale seulement, durée non calibrée. Aucune tolérance HA au-delà des
mesures nested. Le nettoyage préserve invités/disques.
