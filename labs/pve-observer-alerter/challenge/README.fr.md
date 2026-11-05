# Défi : Observer la capacité et recevoir les alertes

Configurez la chaîne de métriques/alertes PVE pour le service attribué et son volume de données jetable borné. Définissez un seuil avant saturation, configurez le récepteur local et faites franchir le seuil par la charge bornée fournie. Vérifiez un échantillon de métrique PVE réel et la réception de la notification. Résolvez la condition et observez le retour à la normale sans désactiver la surveillance. Un compte rendu saisi par l’apprenant ne prouve pas la réception.

La ressource attribuée est `Live PVE node metrics; local receiver and bounded guest load are supplied externally; no guest or receiver is created.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
