# Redimensionner une VM et prouver un retour local

La VM applicative fonctionne avec 1 vCPU, 1024 Mio de mémoire et un disque système de 4 Gio. Préservez un point de retour local avant de lui allouer 2 vCPU, 2048 Mio et un disque de 8 Gio. Étendez aussi la partition et le système de fichiers dans Debian. Le témoin initial, l’agent invité et le réseau fixe sont fournis.

Lisez [scenario.fr.md](./scenario.fr.md) avant de commencer.

```bash
dsoxlab run pve-gerer-cycle-vie
dsoxlab challenge pve-gerer-cycle-vie
dsoxlab check pve-gerer-cycle-vie
```
