# Défi : Sécuriser les identités, jetons et connexions

Configurez l’identité d’automatisation nommée, une voie humaine de secours et un jeton API à séparation de privilèges. Accordez uniquement le périmètre lecture/gestion d’énergie de la VM attribuée. Faites tourner le jeton : conservez son identifiant, remplacez son secret par la procédure PVE prévue et prouvez que l’ancien secret est refusé sans afficher les secrets. Gardez la vérification TLS active ; ne désactivez pas les contrôles de certificat et ne déposez aucun secret dans le dossier de preuves.

La ressource attribuée est `PVE identity automation-n2@pve and privilege-separated token lab-n2; VMID 202 is the only assigned VM ACL scope.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
