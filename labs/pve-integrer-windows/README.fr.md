# pve-integrer-windows

Utilisez uniquement une ISO Windows pour laquelle vous disposez d’une licence et d’une autorisation, ainsi que l’ISO officielle des pilotes VirtIO. Installez une version choisie et prise en charge, chargez les pilotes disque/réseau, vérifiez l’agent et le réseau après redémarrage, retirez les médias et restaurez une sauvegarde incluant EFI et TPM.

**Prérequis / conditions de blocage :** BLOQUÉ tant que les deux chemins ISO et une autorisation de licence explicite ne figurent pas dans /etc/lab-proxmox/pve-integrer-windows.yml. Le setup ne télécharge aucun média Windows et ne contourne ni activation ni OOBE.

```bash
dsoxlab run pve-integrer-windows
dsoxlab check pve-integrer-windows
dsoxlab clean pve-integrer-windows
```

Le nettoyage est limité aux VMID, à la balise et aux objets dédiés déclarés pour ce lab. Il ne supprime ni template, ni charge source, ni stockage partagé, ni nœud du cluster.
