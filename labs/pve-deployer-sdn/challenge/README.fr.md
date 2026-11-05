# Défi : Construire un réseau SDN adapté à la charge

Sur un cluster multi-nœuds existant et pris en charge, créez et appliquez le VNet dédié, raccordez les deux invités préparés, prouvez leur communication, migrez un invité vers le second nœud et répétez le test. Corrigez un MTU volontairement erroné ou un état SDN non appliqué avant validation.

## Ce que les tests observent

- Le VNet réel existe, est appliqué sur les deux nœuds configurés et utilise le MTU prévu.
- Les deux invités ont leur carte sur ce VNet et communiquent réellement.
- Après migration, l’invité se trouve sur l’autre nœud et communique toujours avec le même pair.

Les tests inspectent l’état réel de Proxmox/de l’invité. Ils ne notent ni l’historique des commandes ni une déclaration non vérifiée. Un prérequis absent est signalé comme bloquant, jamais comme une réussite.
