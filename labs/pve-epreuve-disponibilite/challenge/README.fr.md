# Allocation d’épreuve et interface de preuves

Le formateur crée `challenge/work/config.json` sur contrôleur indépendant avec
trois `hosts` exacts, `guest_ids=[9381]`, `sources` indépendants distincts du
catalogue pour `pbs_primary`, `pbs_secondary`, `recovery`, `vault`,
`console_verified=true`, `nested_only=true`,
`allow_failure="pve-epreuve-disponibilite"`, `source`, `destination`,
`maintenance_node` parmi les nœuds exacts, `budget` justifié avec
`host_overhead_bytes`, `recovery_bytes`, `disk_reserve_bytes`,
`backup_snapshot="vm/9381/<horodatage UTC>"`, `rto_seconds`,
`rpo_transactions` annoncés, `guest_network` dans `10.10.113.0/24`, `marker`,
`service_url="https://<invité-primaire>/api/lab/pve-epreuve-disponibilite"`,
`recovery_url="https://<invité-restauré>/api/lab/pve-epreuve-disponibilite"`.
**Rôles sources indépendants absents au catalogue.** Setup les refuse ; ni nœud
cluster réutilisé ni endpoint non déclaré inventé.

GET métier renvoie `{"sequence":123,"marker":"..."}` durable ; POST append
acquitte durablement. TLS de confiance, clés SSH connues, sudo non interactif,
inventaire dsoxlab ou `N3_SSH_CONFIG`, console indépendante vérifiée.
Livrer clés/identifiants secondaires sans afficher le contenu ; identifiants
primaires ne doivent pas devenir des dépendances de reprise.
Cible initialement vierge ; seuls ID invité/stockage attribués peuvent servir.

Interface contrôleur depuis le répertoire du lab :

```text
python3 tools/controller.py snapshot --phase <phase>
python3 tools/controller.py probe --duration <1..180>
python3 tools/controller.py fail --action <action> --hosts <hôtes-attribués> --duration <10..120>
python3 tools/controller.py restore
```

Observations : `qualified`, `replicated`, `load`, `failover`,
`preflight-rejected`, `maintenance`, `reintegrated`, `restored`.
Actions : partition d’un nœud, perte de majorité, lien de réplication,
isolation primaire sur cible indépendante. Retour armé avant, action concurrente
refusée. Urgence `restore` ; échec SSH conserve verrou/preuves et impose console
indépendante pour restaurer uniquement Corosync/nft attribués.
Ne pas vider firewall, abaisser votes ni contourner fencing. Reprise pendant
blocage primaire sans second écrivain. Si la recette qualifiée dépasse la
borne, interrompre et recalibrer avant l’épreuve, pas retirer les protections.

Rédiger `challenge/work/report.md`, conserver `challenge/work/evidence` brut
pour les cinq critères : identités configurées/mesurées, stockage/réserve N-1,
HA/watchdog/fencing et propriétaires disques/processus, chronologie externe
et données exactes, distinctions réplication/backup, maintenance/tâches refusées,
manifeste secondaire, identité clé, refus d’accès primaire, RPO/RTO et domaines
physiques non testés. Tests sur états, tâches, données durables et reçus réels.
Évaluation humaine sur fencing, indépendance complète, limites physiques et
runbooks. Archiver avant nettoyage : actions/preuves seulement, jamais invités,
stockage, backups ou secrets. Revenir à un écrivain via le runbook de réseaux
primaire/reprise séparés convenu.

## Politique d’aide

Aucun indice progressif ni solution pendant l’épreuve conformément au catalogue.
Convenir des documents autorisés avant démarrage. Corrigés réservés au formateur,
hors du lab apprenant.
