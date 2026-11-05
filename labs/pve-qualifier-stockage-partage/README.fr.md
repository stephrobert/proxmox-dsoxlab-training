# Qualifier le stockage partagé

Mettre un volume NFS dédié à disposition du cluster et qualifier son identité
et ses limites de disponibilité. Cible `proxmox-cluster` : `pve01.lab`, rôles
`node2=pve02.lab`, `node3=pve03.lab` ; contrôleur sur le poste indépendant.

```bash
dsoxlab run pve-qualifier-stockage-partage
dsoxlab check pve-qualifier-stockage-partage
dsoxlab clean pve-qualifier-stockage-partage
```

**Bloqué actuellement :** aucun serveur NFS indépendant n’est déclaré au catalogue.
Le setup refuse explicitement ce prérequis, sans inventer d’hôte, réutiliser un nœud
ni provisionner. [Scénario](scenario.fr.md) et [consigne](challenge/README.fr.md)
décrivent la recette complète pour une source qualifiée séparément.
Contrôles locaux seulement, aucune exécution PVE ; durée non calibrée.
Le nettoyage préserve invités, exports, volumes et backups du formateur.
