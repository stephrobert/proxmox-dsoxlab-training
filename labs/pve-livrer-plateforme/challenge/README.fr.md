# Défi : Livrer une recette reproductible et transférable

À partir d’un template Debian cloud-init préexistant et autorisé, créez la VM du lab, configurez un service HTTP avec nonce, puis rejouez le provisioning. Créez et restaurez une sauvegarde Proxmox vers une seconde VM du lab, vérifiez le même service et ne nettoyez que les ressources balisées pour ce lab.

## Ce que les tests observent

- Le service réel répond avec le nonce du setup depuis la VM provisionnée.
- La sauvegarde Proxmox réelle correspond à la VM et la VM restaurée sert le même nonce.
- La sentinelle non concernée reste strictement inchangée.

Les tests inspectent l’état réel de Proxmox/de l’invité. Ils ne notent ni l’historique des commandes ni une déclaration non vérifiée. Un prérequis absent est signalé comme bloquant, jamais comme une réussite.
