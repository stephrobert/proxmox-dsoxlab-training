# Défi : Déployer et dépanner un stockage Ceph

Sur un lab Ceph dédié et isolé uniquement, relevez la santé initiale et le contrat de réplication, observez la perte contrôlée de l’OSD explicitement désigné pour le lab, vérifiez que le volume RBD reste disponible selon la politique dégradée annoncée, puis rétablissez cet OSD et prouvez que les PG redeviennent sains et la réplication est restaurée. Ne prétendez pas mesurer le matériel.

## Ce que les tests observent

- L’image RBD du lab reste lisible quand l’OSD désigné est dégradé et le pool respecte son min_size.
- L’OSD désigné revient up/in et les PG du pool deviennent clean avec le nombre de répliques configuré.
- La santé Ceph actuelle est interrogée en direct ; aucune performance n’est évaluée.

Les tests inspectent l’état réel de Proxmox/de l’invité. Ils ne notent ni l’historique des commandes ni une déclaration non vérifiée. Un prérequis absent est signalé comme bloquant, jamais comme une réussite.
