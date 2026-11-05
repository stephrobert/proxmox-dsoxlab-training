# Défi : Maintenir un nœud et préparer une montée de version

Utilisez uniquement le nœud jetable et qualifié par version nommé dans le manifeste. Exécutez le précontrôle adapté à la version et consignez son résultat réel avant maintenance ; levez les blocages ou arrêtez-vous. Appliquez uniquement le changement de paquets préapprouvé, puis vérifiez la version du nœud, la santé cluster/API, les charges représentatives et l’accès aux sauvegardes. Le test ne fait que lire l’état PVE et ne met jamais à niveau le nœud. Si le nœud jetable et les sauvegardes vérifiées ne sont pas fournis, ne tentez pas de mise à niveau sur un nœud partagé.

La ressource attribuée est `Disposable version-qualified PVE node, verified backups, and console; setup changes no VMID or package state.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
