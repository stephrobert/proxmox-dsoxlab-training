# Défi : Automatiser les opérations avec Ansible

Avec l’identité de lecture, démontrez qu’une opération d’alimentation est refusée, puis utilisez une identité opérateur limitée à la VM cible pour l’arrêter. Rejouez une seconde fois le playbook d’état voulu. Les tests inspectent l’état réel des VM et l’historique des tâches Proxmox, pas le texte du playbook ni un récapitulatif déclaré.

## Ce que les tests observent

- La VM cible est arrêtée, tandis que la sentinelle reste en marche.
- Proxmox enregistre un seul arrêt réussi de la cible, pas une nouvelle tâche lors de la répétition idempotente.
- L’identité en lecture seule reste incapable d’effectuer l’opération d’alimentation.

Les tests inspectent l’état réel de Proxmox/de l’invité. Ils ne notent ni l’historique des commandes ni une déclaration non vérifiée. Un prérequis absent est signalé comme bloquant, jamais comme une réussite.
