# Défi : Exploiter un miroir ZFS et récupérer un disque

Utilisez uniquement le miroir jetable à deux périphériques nommé. Identifiez le membre défaillant à partir de l’état ZFS réel, confirmez que les données du service restent lisibles en mode dégradé, remplacez uniquement le périphérique virtuel attribué et attendez la fin du resilver. Vérifiez que le pool est ONLINE, que le miroir possède deux membres sains et qu’aucune erreur de données ne subsiste. Précisez qu’un remplacement de périphérique virtuel ne simule pas une panne de disque physique. Si la fixture miroir dédiée manque, arrêtez-vous ; ne créez/n’altérez jamais un pool sur un disque de production.

La ressource attribuée est `Dedicated disposable two-device ZFS pool labmirror-n2-214 and evaluator-owned corpus; setup does not create or degrade a pool.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
