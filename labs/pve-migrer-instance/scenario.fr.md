# Mission

État initial : cluster sain, deux destinations qualifiées, VM 9321 et CT 9322
avec services durables, générateur extérieur. Noms du formateur :
`n3-pve-migrer-instance-9321` et `n3-pve-migrer-instance-9322`.

1. Inventorier stockage, CPU, bridges, ISO/snippets/montages. Sur le seul invité
   attribué, introduire une dépendance dédiée présente uniquement à la source ;
   tenter la migration et conserver UPID, erreur finale et propriétaire inchangé.
   Ne pas retirer le disque d’un autre invité ni modifier globalement le stockage.
2. Retirer proprement la fixture négative. Déplacer VM et CT sur le nœud demandé
   avec leurs méthodes live/offline/restart respectives réellement supportées.
3. Exercer des transactions externes pendant la migration ; comparer marqueurs,
   empreintes, séquences durables et sessions. Publier les trous de réponse réels.
4. Effectuer un vrai arrêt/démarrage des deux invités à destination ; détecter
   les dépendances source restantes, confirmer un propriétaire unique.

Limiter les actions aux ressources attribuées ; conserver les diagnostics avant
correction, masquer secrets mais pas identités, préserver SSH/TLS et console.
Les variantes respectant tous les critères sont admises. Ne pas forcer
quorum/verrous ni appeler migration une panne/fencing. Distinguer continuité
mesurée et supposée, fournir un plan de retour précis.
