# Mission

Former un cluster de trois nœuds et démontrer son comportement avec et sans majorité.
État initial : nœuds compatibles préinstallés, réseau Corosync isolé et
contrôleur indépendant avec identités SSH vérifiées et console de secours.

1. Comparer identités, versions, configuration distribuée et votes avant
   l’adhésion. Conserver les observations avant correction. Former le cluster
   sur le réseau Corosync attribué, jamais sur une interface de production.
2. Observer le cluster sain depuis les trois nœuds.
3. Retirer un votant depuis le contrôleur extérieur ; observer les deux survivants.
4. Rétablir, puis retirer deux votants ; mesurer un vrai refus d’écriture pmxcfs
   sur le survivant. Interdire `pvecm expected`, pmxcfs local et contournements.
5. Rétablir les votants, comparer configuration, membres et tâches en cours.
   Toute divergence ou reprise échouée impose un retour par la console de secours.

N’agir que sur les hôtes, réseaux et ressources attribués. Conserver les
observations, masquer les secrets sans masquer les identités. Une autre
configuration respectant le contrat est acceptée. Distinguer domaines virtuels
et physiques : une perte de nœud nested ne prouve pas la tolérance serveur/site.
La consigne donne commandes bornées, retour et indices progressifs.
