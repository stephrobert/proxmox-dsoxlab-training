# Défi : Déployer PBS et réaliser une sauvegarde vérifiable

Intégrez uniquement le point de terminaison et le datastore PBS attribués dans le manifeste. Utilisez son empreinte TLS enregistrée et une identité de sauvegarde dédiée au moindre privilège. Sauvegardez la VM et le CT nommés, avec leurs volumes déclarés, puis consultez l’inventaire réel des snapshots PBS. Confirmez la réutilisation/déduplication par les statistiques PBS, pas par une affirmation saisie. Si aucun endpoint/datastore PBS n’est fourni, arrêtez-vous : ce lab n’installe pas PBS et n’invente pas d’autre hôte.

La ressource attribuée est `PBS storage lab-pbs-n2-207; externally supplied PBS endpoint/datastore and VM/CT workloads; no PBS host is provisioned by this lab.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
