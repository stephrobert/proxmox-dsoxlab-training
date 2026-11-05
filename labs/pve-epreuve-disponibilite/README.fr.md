# Épreuve de disponibilité

Exploiter trois nœuds avec réserve, mesurer une panne imposée et effectuer une
reprise indépendante. Cible `proxmox-cluster` : `pve01.lab`, `node2=pve02.lab`,
`node3=pve03.lab` ; poste extérieur comme contrôleur/client.

```bash
dsoxlab run pve-epreuve-disponibilite
dsoxlab check pve-epreuve-disponibilite
dsoxlab clean pve-epreuve-disponibilite
```

**Bloqué :** aucun PBS primaire/secondaire indépendant, cible vierge de reprise
ou coffre au catalogue. Setup refuse explicitement sans inventer de rôles ni provisionner.
[Scénario](scenario.fr.md), [consigne d’épreuve](challenge/README.fr.md).
Aucune aide/solution pendant l’épreuve ; documentations autorisées convenues avant.
Syntaxe locale seulement, durée non calibrée, aucune attestation HA/hors-site.
Nettoyage sans suppression des données/ressources du formateur.
