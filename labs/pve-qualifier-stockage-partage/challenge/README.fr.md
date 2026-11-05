# Allocation, exercice et preuves

Créer `challenge/work/config.json` sur le poste indépendant avec exactement
`hosts=["pve01.lab","pve02.lab","pve03.lab"]`, `guest_ids=[9311]`,
`sources={"nfs":"<hôte indépendant du catalogue>"}`, `console_verified=true`,
`nested_only=true`, `allow_failure="pve-qualifier-stockage-partage"`.
Le placeholder **ne désigne pas** un hôte existant : aucun serveur NFS n’est
déclaré, donc le setup refuse avant toute action tant que ce prérequis n’est
pas fourni séparément. Aucun nœud cluster ni hôte non déclaré ne sera accepté.

Renseigner `service_url="https://<invité>/api/lab/pve-qualifier-stockage-partage"`,
`guest_network` comme sous-réseau attribué dans `10.10.113.0/24`, `marker` comme
marqueur durable du formateur, `denied_export="/n3-denied-shared"` pour la
fixture négative dédiée. GET renvoie `{"sequence":123,"marker":"..."}` ; POST
`{"operation":"append","marker":"..."}` écrit durablement puis renvoie l’état.
Certificat de confiance obligatoire, aucune désactivation TLS. Ressources
préparées et nommées avant setup. Aucun secret dans les URL/fichiers.
SSH utilise l’inventaire dsoxlab ou `N3_SSH_CONFIG` existant, clés connues,
sudo non interactif et console de secours indépendante réellement testée.

```bash
python3 tools/controller.py snapshot --phase qualified
python3 tools/controller.py permissions
python3 tools/controller.py probe --duration 30
python3 tools/controller.py fail --action storage --hosts <hôte-nfs-attribué> --duration 120
python3 tools/controller.py restore
```

Avant `qualified`, écrire le nonce sur un seul nœud dans
`/mnt/pve/n3-shared/.n3-pve-qualifier-stockage-partage-nonce`.
Conserver l’écriture autorisée et le vrai refus de l’opération négative.
Le contrôleur n’arrête que le service NFS attribué, après armement du retour.
Une action à la fois, 10–120 secondes ; `restore` est le retour d’urgence.
Si SSH ne revient pas, démarrer NFS sur cette source depuis la console
indépendante ; conserver verrou/preuves. Aucun arrêt cluster, vote forcé,
abaissement de durabilité ni contournement de verrou.
Archiver `challenge/work/evidence` et rédiger `challenge/work/report.md` avec
les quatre critères de `contract.json`, identités montages/exports, refus,
chronologie I/O/client, empreintes, domaines de panne, limites et retour.
Les tests lisent montages, empreintes, réponses métier et reçus bornés.
La revue humaine vérifie aussi permissions, refus et sûreté des montages.
Le nettoyage restaure ses actions et retire ses seules preuves ; il ne détruit
ni exports, ni volumes, ni invités. Retirer explicitement le nonce après archivage.

## Indices

1. Comparer données et source réelle du montage, pas le nom affiché du stockage.
2. Exports NFS, autorisations clients et permissions invité sont des couches distinctes.
3. Des ID identiques peuvent masquer des disques différents ; des nœuds joignables
   ne disent rien sur les I/O lorsque l’unique serveur NFS disparaît.
