# Mission : Automatiser les opérations avec Ansible

Avec l’identité de lecture, démontrez qu’une opération d’alimentation est refusée, puis utilisez une identité opérateur limitée à la VM cible pour l’arrêter. Rejouez une seconde fois le playbook d’état voulu. Les tests inspectent l’état réel des VM et l’historique des tâches Proxmox, pas le texte du playbook ni un récapitulatif déclaré.

## Critères d’acceptation

1. La VM cible est arrêtée, tandis que la sentinelle reste en marche.
2. Proxmox enregistre un seul arrêt réussi de la cible, pas une nouvelle tâche lors de la répétition idempotente.
3. L’identité en lecture seule reste incapable d’effectuer l’opération d’alimentation.

## Prérequis

Crée deux VM de 512 Mio ; démarre la cible 1741 et la sentinelle 1742. Créez des jetons lecture et opérateur distincts, limités à ces chemins VM ; le setup n’affiche ni n’installe d’identifiants.

Ce scénario n’installe pas PVE, ne provisionne aucun hôte et n’installe aucune fonctionnalité.
