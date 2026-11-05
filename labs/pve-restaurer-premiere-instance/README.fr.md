# pve-restaurer-premiere-instance

Sauvegarder une instance puis retrouver ses données et son service dans une restauration isolée.

Lisez [`scenario.fr.md`](./scenario.fr.md) avant de commencer.

```bash
dsoxlab run pve-restaurer-premiere-instance
dsoxlab challenge pve-restaurer-premiere-instance
dsoxlab check pve-restaurer-premiere-instance
```

N'utilisez que les ressources nommées dans le manifeste. Les nœuds cluster ne sont jamais provisionnés implicitement. La réussite automatisée n'atteste pas les critères qui nécessitent une observation humaine.

Le setup réserve les VMID 198 et 199, prépare la VM témoin source et vérifie l'image Debian. Il exige un bridge de restauration isolé fourni par l'instructeur via `pve_restore_bridge` ; aucun réseau externe n'est créé implicitement.
