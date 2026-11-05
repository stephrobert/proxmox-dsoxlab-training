# Allocation et preuves

Créer `challenge/work/config.json` sur le contrôleur indépendant avec
`hosts=["pve01.lab","pve02.lab","pve03.lab"]`, `guest_ids=[9331,9332,9333]`,
`sources={}`, `console_verified=true`, `nested_only=true`,
`destination="pve02.lab"`, `candidate_bytes` pour la demande déclarée et :

```json
{
  "budget": {
    "host_overhead_bytes": 536870912,
    "recovery_bytes": 1073741824,
    "disk_reserve_bytes": 1073741824
  },
  "guest_network": "10.10.113.0/24",
  "service_url": "https://<invité>/api/lab/pve-reserver-capacite",
  "marker": "<marqueur durable>"
}
```

Chiffres illustratifs, **pas des mesures** ; remplacer par des budgets justifiés.
GET invité renvoie `{"sequence":123,"marker":"..."}` durable ; POST append
renvoie la séquence durable mise à jour. TLS de confiance, clés SSH connues et
sudo non interactif obligatoires ; inventaire dsoxlab ou `N3_SSH_CONFIG` existant.
Aucun nœud/service manquant n’est provisionné. Vérifier la console indépendante.

```bash
python3 tools/controller.py snapshot --phase migrated
python3 tools/controller.py snapshot --phase candidate-rejected
python3 tools/controller.py probe --duration 30
```

Observer après déplacement autorisé puis décision de report/refus. Garder 9333
arrêtée. Sonde bornée à 1–180 secondes. Aucune panne physique ni manipulation
de quorum n’est nécessaire pour le calcul N-1. Les tests comparent mémoire,
disque, maxima invités, séparation et candidate inactive. La revue vérifie
aussi règle effective propre à la version et décision d’admission/report.
Rédiger `challenge/work/report.md` pour les critères de `contract.json` :
unités, budgets hôtes/invités/stockage, mesures sous charge, perte hypothétique
du plus gros nœud, règles, demande candidate, limites et retour.
Archiver avant nettoyage ; celui-ci retire ses seules preuves et restaure ses
actions, jamais invités/règles. Annuler seulement règles et placements attribués
selon le runbook. Aucune charge non bornée ni contournement de verrou.

## Indices

1. Mesurer le plus gros nœud et le disque réellement disponible.
2. Maxima configurés et surcharge hôtes diffèrent de l’usage instantané des invités.
3. La marge avant panne n’est pas celle après perte du plus gros hôte ;
   une préférence affichée n’est pas nécessairement une séparation imposée.
