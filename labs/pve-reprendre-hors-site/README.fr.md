# Reprendre hors site

Récupérer une charge depuis PBS secondaire et secrets de secours extérieurs
avec primaire inaccessible. Cible `proxmox-cluster` : `pve01.lab`, rôles
`node2=pve02.lab`, `node3=pve03.lab` ; poste indépendant comme contrôleur.

```bash
dsoxlab run pve-reprendre-hors-site
dsoxlab check pve-reprendre-hors-site
dsoxlab clean pve-reprendre-hors-site
```

**Prérequis bloquants :** aucun PBS secondaire, PVE de reprise vierge séparé ou
coffre déclaré au catalogue. Le setup refuse explicitement, sans inventer de
rôles, réutiliser des nœuds cluster ni provisionner des services.
[Scénario](scenario.fr.md), [consigne](challenge/README.fr.md).
Syntaxe/contenu locaux seulement, durée non calibrée, aucune attestation
hors-site/HA. Nettoyage sans suppression PBS, invités restaurés ou clés de secours.
