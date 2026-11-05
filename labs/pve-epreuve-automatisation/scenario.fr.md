# Mission : Livrer une plateforme reproductible par API et IaC

Validez l’épreuve pratique N4 de bout en bout. Utilisez l’API Proxmox pour une opération réelle ; importez/gérez la VM attribuée avec Terraform et conservez un vrai plan/état final ; construisez un inventaire rafraîchi depuis les données du cluster ; exploitez l’invité avec Ansible ; livrez le service et une sauvegarde restaurable. Rejouez la recette sans recréer ni redémarrer l’invité.

## Critères d’acceptation

1. L’UPID API correspond à la vraie tâche réussie de la VM attribuée.
2. L’état Terraform gère exactement cette VM et le dernier plan sauvegardé ne propose aucun changement.
3. L’inventaire rafraîchi contient exactement l’invité du lab balisé et son nœud/adresse réels.
4. Ansible laisse l’état voulu dans Proxmox ; la seconde exécution ne crée pas une deuxième tâche de démarrage/arrêt.
5. Le même VMID sert le nonce du défi avant et après restauration de sa véritable sauvegarde Proxmox.
6. Le template autorisé et la configuration de la sentinelle non concernée restent inchangés.

## Prérequis

Bloqué tant qu’aucun template Debian cloud-init autorisé avec agent QEMU n’est disponible. Ce lab ne crée ni installation PVE, ni template, ni cluster.

Ce scénario n’installe pas PVE, ne provisionne aucun hôte et n’installe aucune fonctionnalité.
