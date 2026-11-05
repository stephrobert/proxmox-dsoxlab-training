# Allocation et migration mesurée

Créer `challenge/work/config.json` sur le poste indépendant :

```json
{
  "hosts": ["pve01.lab", "pve02.lab", "pve03.lab"],
  "guest_ids": [9321, 9322], "sources": {},
  "console_verified": true, "nested_only": true,
  "destination": "pve02.lab", "guest_network": "10.10.113.0/24",
  "service_url": "https://<service-vm>/api/lab/pve-migrer-instance",
  "marker": "<marqueur durable du formateur>"
}
```

GET du service VM renvoie `{"sequence":123,"marker":"..."}` durable ;
POST `{"operation":"append","marker":"..."}` écrit durablement. Certificat
de confiance requis, pas de secret dans l’URL. Exercer aussi le service CT
et les sessions client. Noms des invités conformes au scénario.
Renseigner `ct_service_url="https://<service-ct>/api/lab/pve-migrer-instance"`
avec la même interface JSON durable. Les tests comparent aussi séquence/marqueur
CT et propriétaire réel du processus LXC après déplacement et redémarrage.
La seconde destination est pve03.lab ; documenter sa qualification avant de
choisir pve02.lab. Inventaire SSH provisionné ou `N3_SSH_CONFIG` explicite avec
clés connues et sudo non interactif. Contrôleur extérieur à toutes les IP cibles.

```bash
python3 tools/controller.py snapshot --phase preflight-rejected
python3 tools/controller.py probe --duration 120
python3 tools/controller.py snapshot --phase migrated
python3 tools/controller.py snapshot --phase rebooted
```

Relever `preflight-rejected` après une vraie tâche `qmigrate` échouée. Lancer
la sonde bornée dans un autre terminal pendant la migration VM/CT attribuée.
Relever `migrated` quand les deux tournent à destination, puis `rebooted` après
la fin de leurs vrais arrêts/démarrages. Sonde 1–180 secondes, SSH borné ;
aucune panne du contrôleur n’est nécessaire pour une migration.
Ne contourner ni verrous ni votes attendus. Préserver l’accès de secours.

Rédiger `challenge/work/report.md` pour les quatre critères de `contract.json` :
dépendances, UPID/erreur, placement/processus, empreintes VM/CT et sessions,
interruption mesurée, dépendances au redémarrage, limites et retour/nettoyage.
Les tests lisent état réel des tâches, placement, QEMU, tâches de démarrage et
réponses durables externes. La revue couvre empreintes/sessions CT et choix
de méthode supportée. Archiver `challenge/work/evidence` avant nettoyage.
Celui-ci retire les preuves du contrôleur, jamais invités/disques. Annuler
seulement la dépendance négative et les placements attribués selon le runbook.

## Indices

1. Une migration acceptée par l’API peut échouer en tant que tâche.
2. Vérifier séparément stockages, snippets, ISO et identités des bridges à destination.
3. Une migration réussie peut cacher une dépendance source jusqu’au prochain
   démarrage à froid ; les horodatages client, pas l’icône verte, mesurent la coupure.
