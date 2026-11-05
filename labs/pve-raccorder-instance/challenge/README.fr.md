# pve-raccorder-instance

Réparez le raccordement réseau de la VM 160 fournie. Conservez son identité de VM et son disque ; la page de session seule ne prouve pas cette identité.

## Exigences notées

1. Rattachez net0 de la VM 160 au pont exact vmbr0.
2. Faites de l’interface exacte tap160i0 un port effectif de vmbr0.
3. Servez la ligne témoin exacte de la session à l’adresse et au port du manifeste, accessible depuis le nœud.
4. Gardez les interfaces physiques hors du pont isolé vmbr9.
5. Préservez l’identité SMBIOS de la VM 160 sans déclencher de nouvelle tâche de création de cette VM.
6. Préservez la joignabilité après un arrêt propre et un démarrage de la VM 160.
7. Préservez la joignabilité après le rechargement réussi du réseau du nœud par l’évaluateur.

Les contrôles de persistance effectuent un arrêt propre puis un démarrage et constatent les deux états. Les lectures impossibles refusent la mesure. Les contrôles de préservation ne sont comptés qu’une fois le rapport présent, le réseau rétabli ou l’agent joignable, selon le lab.

Pour vérifier l’origine de la page, l’évaluateur désactive temporairement l’interface virtuelle de l’invité, constate que le service devient inaccessible, puis restaure l’interface. Il ne modifie pas l’interface de gestion du nœud.
