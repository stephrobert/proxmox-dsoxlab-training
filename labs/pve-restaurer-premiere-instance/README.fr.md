# Sauvegarder et restaurer une première VM sur un réseau isolé

La VM source 198 sert déjà un témoin propre à la session sur 10.10.113.198:8080. La préparation fournit le pont isolé vmbr9 et le client dsox-restore (10.10.113.240/24). Sauvegardez dans /var/lib/vz/dump/pve-restaurer-premiere-instance puis restaurez vers la VM 199. Gardez l’adresse IP de l’invité restauré : source et restauration utilisent des segments Ethernet distincts. Ne raccordez pas le pont isolé au réseau de l’hôte.

Lisez [scenario.fr.md](./scenario.fr.md) avant de commencer.

```bash
dsoxlab run pve-restaurer-premiere-instance
dsoxlab challenge pve-restaurer-premiere-instance
dsoxlab check pve-restaurer-premiere-instance
```
