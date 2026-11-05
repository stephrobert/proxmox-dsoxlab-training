# Défi : Segmenter et diagnostiquer les VLAN

Créez les segments VLAN isolés 285 et 286 sur le pont de lab nommé, affectez les cartes de test à leurs tags attendus et n’implémentez que la route inter-VLAN demandée. Gardez l’administration sur son chemin initial. Corrigez le tag invité erroné, puis vérifiez la configuration effective des cartes/ponts PVE et la matrice de connectivité. Ne modifiez pas l’uplink physique et ne redémarrez pas le réseau de l’hôte.

La ressource attribuée est `VMID 205; isolated bridge vmbr205 and VLAN IDs 285/286; no physical uplink is assigned.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
