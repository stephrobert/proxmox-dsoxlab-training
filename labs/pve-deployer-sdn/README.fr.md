# pve-deployer-sdn

Sur le cluster existant à trois nœuds `proxmox-cluster`, créez et appliquez le VNet dédié, raccordez les deux invités préparés, prouvez leur communication, migrez un invité vers un autre nœud configuré et répétez le test. Examinez et corrigez un MTU incohérent ou un état SDN non appliqué s'il y en a un.

**Prérequis / conditions de blocage :** BLOQUÉ sans le cluster `proxmox-cluster` existant, sain et à trois nœuds, zone SDN autorisée, fichier de topologie isolée `/etc/lab-proxmox/pve-deployer-sdn.json` (avec les noms réels des nœuds du cluster) et template invité autorisé au VMID 9000. Ce lab ne fournit ni nœuds, ni installation PVE, ni licence, ni média invité.

```bash
dsoxlab start pve-deployer-sdn --target proxmox-cluster
dsoxlab check pve-deployer-sdn
dsoxlab clean pve-deployer-sdn
```

Le nettoyage est limité aux VMID, à la balise et aux objets dédiés déclarés pour ce lab. Il ne supprime ni template, ni charge source, ni stockage partagé, ni nœud du cluster.
