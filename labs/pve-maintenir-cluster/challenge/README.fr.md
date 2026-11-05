# Allocation et maintenance bornée

`challenge/work/config.json` sur contrôleur indépendant : trois `hosts` exacts,
`guest_ids=[9361]`, `sources={}`, `console_verified=true`, `nested_only=true`,
`allow_failure="pve-maintenir-cluster"`, `maintenance_node="pve01.lab"`,
`destination="pve02.lab"`, `budget` justifié avec
`host_overhead_bytes`, `recovery_bytes`, `disk_reserve_bytes`,
`guest_network="10.10.113.0/24"`,
`service_url="https://<invité>/api/lab/pve-maintenir-cluster"`, `marker` durable.
GET renvoie `{"sequence":123,"marker":"..."}` durable, POST append acquitte
l’écriture durable. TLS de confiance, clés SSH connues/sudo non interactif,
inventaire dsoxlab ou `N3_SSH_CONFIG`. Le formateur vérifie secours, backups et
changement autorisé ; aucune mise à jour générique de paquets n’est lancée.

```bash
python3 tools/controller.py snapshot --phase maintenance
python3 tools/controller.py probe --duration 120
python3 tools/controller.py fail --action one-node --hosts pve01.lab --duration 120
python3 tools/controller.py snapshot --phase reintegrated
python3 tools/controller.py snapshot --phase restored
python3 tools/controller.py restore
```

Capturer `maintenance` après évacuation et avant retrait du nœud. Garder la
sonde dans un autre terminal. Le contrôleur refuse les actions simultanées ;
conserver le refus de la seconde demande. Le retrait Corosync constitue
l’intervention d’appartenance autorisée et bornée, pas une preuve de mise à
jour OS ni de panne physique. Ne pas maintenir un second nœud.
Pannes 10–120 secondes, sondes 1–180 secondes. Retour armé avant arrêt ;
`restore` est l’urgence. Échec SSH conserve verrou/preuves pour console.

Après retour, sauvegarder uniquement 9361 et restaurer seulement sur un invité/
réseau de recette explicitement attribué ou via restauration sûre du même ID
arrêté. Aucun ID étranger écrasé ni second écrivain réseau. Capturer `restored`
sur le vrai marqueur restauré, pas l’invité original. Documenter l’allocation
de recette avant usage ; le contrôleur ne choisit jamais un ID libre.
Rédiger `challenge/work/report.md` pour les quatre critères, évacuation/exceptions,
refus concurrent, réserve/quorum mesurés, changement autorisé, identités/stockage,
UPID backup après maintenance, marqueur restauré réel, limites et retour.
Tests sur placement, quorum/stockage, tâches backup et données durables ;
revue sur concurrence, changement borné et identité restaurée.
Archiver avant nettoyage : actions/preuves seulement, jamais invités/backups.
Rétablir les placements attribués selon le runbook.

## Indices

1. Inventorier tout le nœud avant son arrêt.
2. Une seconde maintenance peut supprimer la majorité ; rendre son refus explicite.
3. Réintégration ne signifie pas seulement membres : stockage, service et
   lecture d’un marqueur réellement restauré doivent repasser la recette.
