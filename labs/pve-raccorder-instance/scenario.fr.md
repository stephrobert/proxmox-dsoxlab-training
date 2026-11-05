# Une VM qui tourne, et que personne ne joint

La VM témoin 160 a été livrée hier. Proxmox la montre en marche, son service
écoute sur le port 8080, et pourtant l'équipe qui doit s'en servir ne la joint
pas : `http://10.10.113.160:8080/` ne répond pas, ni depuis son poste, ni
depuis le nœud.

Le manifeste du lab, dans `/opt/lab-proxmox/pve-raccorder-instance/manifeste.md`,
donne l'adresse réservée et le réseau du lab. Le disque de la VM porte la page
témoin de cette session : recréer la VM ne la rendrait pas.

## Mission

1. Depuis le nœud, trouvez pourquoi la VM est injoignable. Regardez le trajet
   dans l'ordre : la carte de la VM, le pont auquel elle est branchée, puis ce
   que ce pont relie.
2. Corrigez au bon étage : c'est la carte de **cette** VM qui doit rejoindre
   `vmbr0`. Ne recréez pas la VM, et ne donnez pas de carte physique au pont
   isolé.
3. Vérifiez depuis le nœud que la page témoin répond.

## Exigences notées

1. Rattachez net0 de la VM 160 au pont exact vmbr0.
2. Faites de l’interface exacte tap160i0 un port effectif de vmbr0.
3. Servez la ligne témoin exacte de la session à l’adresse et au port du manifeste, accessible depuis le nœud.
4. Gardez les interfaces physiques hors du pont isolé vmbr9.
5. Préservez l’identité SMBIOS de la VM 160 sans déclencher de nouvelle tâche de création de cette VM.
6. Préservez la joignabilité après un arrêt propre et un démarrage de la VM 160.
7. Préservez la joignabilité après le rechargement réussi du réseau du nœud par l’évaluateur.

Les contrôles de persistance effectuent un arrêt propre puis un démarrage et constatent les deux états. Les lectures impossibles refusent la mesure. Les contrôles de préservation ne sont comptés qu’une fois le rapport présent, le réseau rétabli ou l’agent joignable, selon le lab.

## Recommencer

`dsoxlab clean pve-raccorder-instance` détruit la VM 160 et retire le pont
isolé. Le nœud reste en place.

Pour vérifier l’origine de la page, l’évaluateur désactive temporairement l’interface virtuelle de l’invité, constate que le service devient inaccessible, puis restaure l’interface. Il ne modifie pas l’interface de gestion du nœud.
