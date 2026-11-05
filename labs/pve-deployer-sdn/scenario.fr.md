# Mission : Construire un réseau SDN adapté à la charge

Sur le cluster existant à trois nœuds `proxmox-cluster`, créez et appliquez le VNet dédié, raccordez les deux invités préparés, prouvez leur communication, migrez un invité vers un autre nœud configuré et répétez le test. Corrigez un MTU volontairement erroné ou un état SDN non appliqué avant validation.

## Critères d’acceptation

1. Le VNet réel existe, est appliqué sur les trois nœuds configurés et utilise le MTU prévu.
2. Les deux invités ont leur carte sur ce VNet et communiquent réellement.
3. Après migration, l’invité se trouve sur l’autre nœud et communique toujours avec le même pair.

## Prérequis

BLOQUÉ sans le cluster `proxmox-cluster` existant, sain et à trois nœuds, zone SDN autorisée, fichier de topologie isolée `/etc/lab-proxmox/pve-deployer-sdn.json` utilisant les vrais noms des nœuds du cluster et template invité autorisé au VMID 9000. Ce lab ne fournit ni nœuds, ni installation PVE, ni licence, ni média invité.

Ce scénario n’installe pas PVE, ne provisionne aucun hôte et n’installe aucune fonctionnalité.
