# Mission : Déployer et dépanner un stockage Ceph

Sur un lab Ceph dédié et isolé uniquement, relevez la santé initiale et le contrat de réplication, observez la perte contrôlée de l’OSD explicitement désigné pour le lab, vérifiez que le volume RBD reste disponible selon la politique dégradée annoncée, puis rétablissez cet OSD et prouvez que les PG redeviennent sains et la réplication est restaurée. Ne prétendez pas mesurer le matériel.

## Critères d’acceptation

1. L’image RBD du lab reste lisible quand l’OSD désigné est dégradé et le pool respecte son min_size.
2. L’OSD désigné revient up/in et les PG du pool deviennent clean avec le nombre de répliques configuré.
3. La santé Ceph actuelle est interrogée en direct ; aucune performance n’est évaluée.

## Prérequis

BLOQUÉ sans /etc/lab-proxmox/ceph-isolated et sans identifiant d’OSD jetable dédié dans /etc/lab-proxmox/pve-eprouver-ceph.yml sur un cluster isolé. Ne mettez jamais out un OSD partagé/de production.

Ce scénario n’installe pas PVE, ne provisionne aucun hôte et n’installe aucune fonctionnalité.
