# Défi : Router, traduire et modifier le réseau sans se couper

Utilisez le pont isolé et le réseau privé attribués. Configurez la translation sortante et ne publiez que le port de service indiqué dans une chaîne nftables dédiée. Conservez la route par défaut et le réseau d’administration. Préparez le changement volontairement erroné et prouvez que le retour par console indépendante restaure l’état PVE/réseau initial. Vérifiez la persistance des règles et l’absence de doublons après rechargement ; ne modifiez ni l’uplink, ni le lien cluster, ni la route par défaut.

La ressource attribuée est `VMID 206; isolated bridge vmbr206; nftables chain N2LAB206; no physical uplink or default route is assigned.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
