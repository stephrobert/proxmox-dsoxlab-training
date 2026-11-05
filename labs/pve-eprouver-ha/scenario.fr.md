# Mission

État initial : cluster trois nœuds, stockage et réserve N-1 qualifiés, profil
watchdog documenté, client/contrôleur extérieurs. VM 9351 nommée
`n3-pve-eprouver-ha-9351`, stockage dédié `n3-ha`, données durables exposées.

1. Inventorier quorum, propriétaire HA, watchdog, disques et domaines de panne.
   Vérifier secours/arrêt extérieur avant tout armement.
2. Imposer une partition du porteur ou une perte virtuelle d’alimentation qualifiée.
   Ne pas remplacer la panne par arrêt ordonné d’invité ou migration.
3. Corréler chronologie fencing/watchdog, QEMU multi-observateurs, HA et
   transactions externes. Rejeter propriété disque ambiguë ou double écrivain.
4. Rétablir puis, séparément, retirer la majorité : mesurer refus réel d’écriture,
   votes attendus inchangés et données durables conservées. Retrouver un cluster sain.

Seuls hôtes, réseaux et VM attribués peuvent changer. Conserver preuves avant
correction, masquer secrets, maintenir SSH/TLS et secours. Une variante doit
respecter les mêmes garanties et preuves. Une panne de nœud virtuel nested ne
certifie pas la HA après perte de serveur physique/site.
