# Défi : Diagnostiquer une VM indisponible

Examinez la VM 211 fournie et l’état des tâches/journaux PVE avant toute modification. La fixture injecte une panne de pont réseau. Identifiez et corrigez cette panne sans remplacer la VM, supprimer son disque ni affaiblir son pare-feu/agent. Vérifiez que la VM fonctionne, que son disque reste attaché, que le pont attribué est rétabli et que l’agent invité répond après le redémarrage pertinent.

La ressource attribuée est `Pre-provisioned disposable VMID 211 named n2-diagnostique with its disk, guest agent, and firewall; the only injected fault is net0 on vmbr999.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien. Le setup exige la vraie fixture invitée et refuse de simuler une VM sans son disque de données.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
