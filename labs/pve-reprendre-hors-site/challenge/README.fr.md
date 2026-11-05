# Allocation et recette de reprise

`challenge/work/config.json` sur contrôleur : trois `hosts` exacts,
`guest_ids=[9371]`, `sources` avec des **hôtes indépendants distincts déclarés**
pour `pbs_secondary`, `recovery`, `vault`, `console_verified=true`,
`nested_only=true`, `allow_failure="pve-reprendre-hors-site"`,
`backup_snapshot="vm/9371/<horodatage UTC>"`, `rto_seconds`, `rpo_transactions`,
`guest_network` dans `10.10.113.0/24`, `marker` durable,
`service_url="https://<invité-primaire>/api/lab/pve-reprendre-hors-site"`,
`recovery_url="https://<invité-restauré>/api/lab/pve-reprendre-hors-site"`.
**Aucun de ces hôtes indépendants n’existe au catalogue actuel.** Les placeholders
ne peuvent pas être des nœuds cluster ; setup arrêté avant toute action.

GET des deux API renvoie `{"sequence":123,"marker":"..."}` durable et POST append
écrit durablement. TLS de confiance. SSH : inventaire dsoxlab ou `N3_SSH_CONFIG`,
clés connues, sudo non interactif, contrôleur extérieur. Identifiants/empreinte
secondaire déjà protégés sur reprise ; le client PBS cible seulement le dépôt
secondaire. Clé coffre :
`/var/lib/lab-proxmox/pve-reprendre-hors-site/recovery-key.json`, jamais affichée
ni enregistrée avec des identifiants. Le formateur qualifie la livraison sûre
sur cible vierge et consigne l’identité de clé sans son contenu.

```bash
python3 tools/controller.py probe --duration 30
python3 tools/controller.py fail --action primary-site --hosts <hôte-reprise-attribué> --duration 120
python3 tools/controller.py restore
```

Restaurer dans un autre terminal **pendant** la fenêtre imposée. Retour armé
avant table nft dédiée sur reprise, bloquant uniquement les adresses cluster
primaires exactes (et PBS primaire déclaré si présent). Ne jamais vider le
firewall global ni bloquer secours/contrôleur/coffre/secondaire. Capturer données
restaurées tant que le primaire est bloqué. Une action, 10–120 secondes, sonde
1–180 secondes ; si la reprise qualifiée dépasse la borne, arrêter et repenser
la fixture, pas supprimer les protections. `restore` est l’urgence.
Échec SSH conserve verrou/preuves ; retirer seulement la table `n3_recovery`
depuis la console indépendante.

Rédiger `challenge/work/report.md` pour les critères : UPID sync secondaire,
manifeste, identité clé, compteurs/refus/connexions primaire, cible vierge et
identité restaurée, empreintes/séquences, panne/disponibilité horodatées,
objectifs/résultats RPO/RTO, limites physiques et retour contrôlé.
Tests sur tâches/manifeste secondaire, ressources/processus reprise, firewall/
connexions et métier externe réel. Revue sur clés de secours seules et toutes
les dépendances primaires pendant l’intervalle. Archiver avant nettoyage :
isolation/preuves seulement, jamais backups, invité restauré ou secrets.
Garder réseaux primaire/reprise séparés jusqu’au retour à écrivain unique approuvé.

## Indices

1. Lire le manifeste secondaire, pas la tâche backup primaire réussie.
2. DNS, authentification, clés et disques peuvent garder des dépendances primaires.
3. Un fichier restauré n’est pas un service repris ; RPO/RTO nécessitent séquences
   acquittées et disponibilité externe horodatée, pas des calendriers configurés.
