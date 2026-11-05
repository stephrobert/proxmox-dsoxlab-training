# Défi : Livrer une plateforme reproductible par API et IaC

Validez l’épreuve pratique N4 de bout en bout avec l’API Proxmox, Terraform, un inventaire Ansible rafraîchi, des opérations Ansible idempotentes et une recette de livraison bornée.

## Ce que les tests observent

- L’UPID API correspond à la vraie tâche réussie de la VM attribuée.
- L’état Terraform gère cette VM et le plan final ne propose aucun changement.
- L’inventaire rafraîchi contient exactement l’invité balisé et son nœud/adresse réels.
- Proxmox enregistre un seul démarrage réel ; la répétition ne crée pas une deuxième tâche.
- La même VM sert le nonce avant et après restauration de sa vraie sauvegarde.
- Le template autorisé et la sentinelle non concernée restent inchangés.

Les tests inspectent l’état réel de Proxmox/de l’invité. Ils ne notent ni l’historique des commandes ni une déclaration non vérifiée. Un prérequis absent est signalé comme bloquant, jamais comme une réussite.
