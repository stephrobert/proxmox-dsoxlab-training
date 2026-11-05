# Défi : Gérer les volumes et identités des LXC

Sur le CT non privilégié 384 fourni, corrigez le mapping d’identifiants afin que seule l’identité applicative accède aux données. Préservez les restrictions du conteneur. Rendez explicites le volume géré et le bind mount, y compris leur périmètre de sauvegarde. Reconstruisez le CT depuis la sauvegarde fournie et vérifiez les deux marqueurs de données distincts dans le CT restauré. Si le CT ou son modèle attribué est absent, arrêtez-vous et signalez ce prérequis ; ne créez pas de remplacement sur un hôte partagé.

La ressource attribuée est `Pre-provisioned disposable CTID 384 named lab-n2-volumes; managed volume lab-n2-volumes; bind mount /srv/lab-n2-share.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
