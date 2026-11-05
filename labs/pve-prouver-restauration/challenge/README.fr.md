# Défi : Restaurer un service et mesurer RPO et RTO

Restaurez la charge attribuée sur le réseau de reprise isolé alors que les volumes source sont indisponibles. Validez l’application à l’aide du journal d’écritures détenu par l’évaluateur et relevez le dernier enregistrement confirmé comme preuve du RPO. Mesurez le RTO à partir des horodatages observés des tâches jusqu’à la disponibilité applicative, pas d’une estimation saisie. Vérifiez que la VM de production et les ressources voisines restent inchangées. Si les fixtures PBS/de reprise manquent, arrêtez-vous et signalez le prérequis manquant.

La ressource attribuée est `Empty recovery VMID 209 reserved for a restored VM named n2-restored-209; PBS storage lab-pbs-n2-209, evaluator-owned backup/journal, and isolated recovery network.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
