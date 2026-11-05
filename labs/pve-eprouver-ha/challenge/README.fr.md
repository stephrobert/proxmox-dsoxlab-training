# Allocation, panne bornée et acceptation

Allocation `challenge/work/config.json` sur contrôleur : trois `hosts` exacts,
`guest_ids=[9351]`, `sources={}`, `console_verified=true`, `nested_only=true`,
`allow_failure="pve-eprouver-ha"`, `destination="pve02.lab"`,
`guest_network="10.10.113.0/24"`,
`service_url="https://<invité>/api/lab/pve-eprouver-ha"`, `marker` durable.
GET renvoie `{"sequence":123,"marker":"..."}`, POST append acquitte durablement.
TLS de confiance, clés SSH connues, sudo non interactif et console extérieure
obligatoires. Inventaire dsoxlab ou `N3_SSH_CONFIG`. Le formateur documente
watchdog et qualifie réserve/stockage avant setup.

```bash
python3 tools/controller.py probe --duration 120
python3 tools/controller.py fail --action one-node --hosts pve01.lab --duration 120
python3 tools/controller.py snapshot --phase failover
python3 tools/controller.py fail --action no-majority --hosts pve02.lab pve03.lab --duration 120
python3 tools/controller.py restore
```

Remplacer pve01.lab uniquement par le **porteur observé** parmi les trois nœuds.
Sonde externe et capture `failover` dans un autre terminal, pendant la fenêtre
imposée quand la reprise est réellement observée. `one-node` arrête Corosync,
pas l’invité : cette partition ne compte que si fencing réellement observé et
propriété non ambiguë. Aucun succès HA déduit de l’arrêt Corosync seul.
Retours armés avant changement, pannes 10–120 secondes, sondes 1–180 secondes,
une action active à la fois. `restore` est le retour d’urgence ; si watchdog
redémarre un nœud et SSH échoue, utiliser la console, garder verrou/preuves.

Rédiger `challenge/work/report.md` pour les quatre critères de `contract.json` :
perte réelle du porteur, journaux watchdog/fencing, propriété disque/processus,
transactions/empreintes et intervalle de coupure, refus négatif et retour.
Les tests exigent reçus de contrôle réel, QEMU multi-nœuds, réponses durables
et votes inchangés. La revue vérifie sens du fencing, propriétaire indisponible
et sémantique du stockage. Ni votes forcés, ni verrous contournés, ni durabilité
réduite. Distinguer virtuel/physique, ne revendiquer que les mesures.
Archiver avant nettoyage : seules actions/preuves du contrôleur sont retirées,
jamais invités, stockage ou politique HA. Annuler uniquement la politique de
cette VM selon le runbook approuvé.

## Indices

1. Identifier le porteur et mesurer les transactions avant panne.
2. Corréler watchdog/fencing, QEMU et propriétaire HA sur les survivants.
3. Migration n’est pas panne ; un porteur injoignable n’est pas automatiquement
   clôturé. Sans majorité, conserver le refus, pas réduire les votes attendus.
