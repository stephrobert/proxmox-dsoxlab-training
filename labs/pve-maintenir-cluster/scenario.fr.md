# Mission

État initial : cluster stable, backups contrôlés, version de changement autorisée,
contrôleur/sonde indépendants. VM 9361 nommée `n3-pve-maintenir-cluster-9361`,
stockage dédié `n3-maintenance` ; inventorier toutes les charges avant intervention.

1. Qualifier backups et retour. Évacuer seulement les charges migrables
   attribuées, conserver placements avant/après, traiter les exceptions.
   Refuser si une charge étrangère doit être déplacée ou reste sur le nœud arrêté.
2. Une maintenance à la fois ; prouver le refus d’une demande concurrente.
   Observer quorum des deux survivants et réserve N-1 pendant chaque étape.
3. Appliquer seulement le changement autorisé et borné, rétablir le nœud,
   vérifier identité, versions, réseaux, stockage et tâches HA.
4. Après maintenance, exercer transaction métier, nouveau backup et lecture
   d’un marqueur restauré. Un journal de backup réussi ne prouve pas la restauration.

Conserver diagnostics et masquer secrets ; seuls hôtes/réseaux/disques attribués,
SSH/TLS et secours préservés. Variantes admises dans le même contrat. Ni votes
forcés ni verrous/durabilité contournés ; documenter service mesuré et limites
virtuelles/physiques.
