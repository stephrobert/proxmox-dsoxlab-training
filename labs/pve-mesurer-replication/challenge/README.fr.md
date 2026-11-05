# Allocation et mesure sûre

Créer `challenge/work/config.json` sur le contrôleur indépendant avec les trois
`hosts` exacts, `guest_ids=[9341]`, `sources={}`, `source="pve01.lab"`,
`destination="pve02.lab"`, `console_verified=true`, `nested_only=true`,
`allow_failure="pve-mesurer-replication"`, `guest_network="10.10.113.0/24"`,
`service_url="https://<invité>/api/lab/pve-mesurer-replication"`, `marker`.
GET renvoie `{"sequence":123,"marker":"..."}` durable ; POST append acquitte
une séquence durable. TLS de confiance, clés SSH connues, sudo non interactif,
inventaire dsoxlab ou `N3_SSH_CONFIG`. Le formateur qualifie d’abord ZFS,
console indépendante et fencing.
Pour le corrigé RPO, renseigner `failure_mode="power"` et les trois UUID
vérifiés décrits dans [le contrôle cluster](../../pve-eprouver-cluster/challenge/README.fr.md).
Ce contrôle hyperviseur local est indépendant et limité aux nœuds attribués ;
une identité guest-agent non vérifiable est refusée. Aucune formation automatique du cluster.

```bash
python3 tools/controller.py snapshot --phase replicated
python3 tools/controller.py probe --duration 30
python3 tools/controller.py fail --action replication-link --hosts pve01.lab --duration 120
python3 tools/controller.py fail --action one-node --hosts pve01.lab --duration 120
python3 tools/controller.py snapshot --phase source-unavailable
python3 tools/controller.py restore
```

Séparer les expériences. `replication-link` crée une table nft dédiée sur source,
bloquant TCP/22 seulement vers cible exacte, retour armé avant ; aucune modification
globale SSH/firewall. Une partition Corosync seule **ne clôture pas** une VM
non-HA. Ne démarrer la réplique qu’après observation de fencing/perte
d’alimentation par le contrôle indépendant qualifié ; sinon refuser la recette
RPO plutôt que risquer deux écrivains. Capturer `source-unavailable` depuis
un autre terminal pendant la fenêtre, après reprise sûre à cible.
Pannes 10–120 secondes, sondes 1–180 secondes. `restore` est le retour d’urgence ;
échec SSH conserve verrou/preuves et impose la console de secours.

Rédiger `challenge/work/report.md` pour chaque critère de `contract.json` :
job/tâche, volumes/snapshots, dernière synchronisation, séquences/empreintes
acquittées/retrouvées, perte exacte, alerte, fencing, propriétaire unique,
retour et limites. Tests sur jobs, ZFS, données métier externes et QEMU réels ;
revue du journal et de la sûreté retour/fencing. Archiver avant nettoyage.
Celui-ci retire ses seules règles/preuves, jamais snapshots/jobs/invités.
Annuler uniquement job 9341-0 et placement attribué selon le runbook.
Ne contourner ni quorum ni fencing.

## Indices

1. Observer la dernière réplication terminée, pas le prochain déclenchement.
2. Rattacher volumes source/cible et séquence au snapshot terminé.
3. L’état VM ne remplace pas l’erreur de réplication ; une réplique récente peut
   perdre des écritures acquittées et le retour source créer deux écrivains.
