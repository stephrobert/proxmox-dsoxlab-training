# Défi : Déléguer les droits sans élargir le périmètre

Créez les deux pools et leurs VM sentinelles, puis attribuez un rôle de moindre privilège à `equipe-n2@pve` uniquement sur le pool attribué. Gardez le pool voisin et l’administration du nœud hors de cette ACL. Prouvez les autorisations et refus en interrogeant les permissions PVE effectives avec l’identité déléguée ; une ACL lue par root ne constitue pas une preuve d’accès effectif.

La ressource attribuée est `VMIDs 201/n2-delegueracc and 216/n2-voisin; pools lab-n2-deleguer and lab-n2-voisin; test accounts equipe-n2@pve, auditeur-n2@pve, and secours-n2@pve.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
