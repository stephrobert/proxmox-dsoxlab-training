# pve-epreuve-automatisation

Validez l’épreuve pratique N4 de bout en bout. Utilisez l’API Proxmox pour une opération réelle ; importez/gérez la VM attribuée avec Terraform et conservez un vrai plan/état final ; construisez un inventaire rafraîchi depuis les données du cluster ; exploitez l’invité avec Ansible ; livrez le service et une sauvegarde restaurable. Rejouez la recette sans recréer ni redémarrer l’invité.

**Prérequis / conditions de blocage :** Bloqué tant qu’aucun template Debian cloud-init autorisé avec agent QEMU n’est disponible. Ce lab ne crée ni installation PVE, ni template, ni cluster.

```bash
dsoxlab run pve-epreuve-automatisation
dsoxlab check pve-epreuve-automatisation
dsoxlab clean pve-epreuve-automatisation
```

Le nettoyage est limité aux VMID, à la balise et aux objets dédiés déclarés pour ce lab. Il ne supprime ni template, ni charge source, ni stockage partagé, ni nœud du cluster.
