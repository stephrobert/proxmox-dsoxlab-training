# Mission

État initial : deux stockages ZFS qualifiés du cluster, VM 9341 nommée
`n3-pve-mesurer-replication-9341` avec journal séquentiel durable, contrôleur
extérieur et console. Seuls stockage `n3-replica` et job 9341-0 sont attribués.

1. Vérifier identités des volumes source/cible, configurer le job et attendre
   sa vraie fin. Conserver noms/GUID snapshots, état de tâche et séquence métier.
2. Ajouter des écritures acquittées. Rendre réellement la source indisponible/
   clôturée depuis le contrôleur, reprendre à cible et comparer journal retrouvé,
   dernière réplication terminée et queue acquittée.
3. Lors d’une expérience séparée après retour, couper seulement le SSH de
   réplication source-vers-cible ; observer l’erreur du job sans couper le SSH secours.
4. Suivre le retour autorisé ; prouver un seul propriétaire/processus avant
   reprise des écritures. Ne jamais démarrer la réplique si la source peut écrire.

Conserver observations avant correction ; seuls hôtes, volumes et réseaux
attribués, TLS/SSH vérifiés, secrets masqués et contrôles indépendants. Ni votes
forcés, ni verrous contournés, ni durabilité réduite. Rapporter domaines
virtuels/physiques, pertes transactionnelles mesurées et distinctions réplication,
migration, sauvegarde.
