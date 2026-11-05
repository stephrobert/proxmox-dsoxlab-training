# Construire et éprouver le cluster

**L’apprenant forme le cluster.** La sélection de `proxmox-cluster` fait
provisionner par le backend KVM trois VM Debian 13 : `pve01.lab`, `pve02.lab`
et `pve03.lab` (8 Gio de RAM, 4 vCPU, disques 40+40 Gio chacune). Ce lab
n’exécute pas `pvecm` et ne joint aucun nœud automatiquement. Installez et
vérifiez Proxmox VE sur chaque nœud, configurez le réseau Corosync isolé et
préparez l’allocation du formateur. Le poste local est le contrôleur extérieur,
jamais un nœud du cluster.

```bash
dsoxlab start pve-eprouver-cluster --target proxmox-cluster
dsoxlab check pve-eprouver-cluster
dsoxlab clean pve-eprouver-cluster
```

Avant `run`, fournir l’allocation du formateur décrite dans
[challenge/README.fr.md](challenge/README.fr.md). Nœuds, PVE, inventaire SSH
vérifié ou console absents produisent des erreurs de précondition, jamais un skip.
Lire [scenario.fr.md](scenario.fr.md). Durée non calibrée ; aucune exécution ni
certification HA n’est revendiquée.

Le nettoyage restaure les actions armées par ce contrôleur et retire ses preuves ;
il ne détruit ni cluster, ni invités, ni disques, ni sauvegardes du formateur.
