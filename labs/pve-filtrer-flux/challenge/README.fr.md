# Défi : Filtrer le management et les invités

Activez le pare-feu PVE sur la VM attribuée et définissez une liste explicite des flux d’administration et invités autorisés. Gardez la politique entrante par défaut sur DROP et préservez la console indépendante. Laissez un service de test à l’écoute pendant la vérification des origines autorisées et refusées. Contrôlez l’état effectif du pare-feu, pas seulement un brouillon local.

La ressource attribuée est `VMID 203 and its per-VM firewall file /etc/pve/firewall/203.fw; no physical NIC or external network is assigned.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
