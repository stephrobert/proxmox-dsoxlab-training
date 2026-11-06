# Construire un template cloud-init et des clones indépendants

La préparation fournit une image cloud Debian 13 avec son SHA-512 publié, un snippet vendor qui installe le service témoin et deux clés clientes SSH distinctes. Elle ne crée ni template ni clone. Utilisez la VM 197 pour le template et les VM 198 et 199 pour les clones. Gardez un vCPU et 768 Mio par clone, la passerelle et le DNS 10.10.113.1 et le pont vmbr0. Ces bornes réservent la place nécessaire à la sonde de l’évaluateur.

Lisez [scenario.fr.md](./scenario.fr.md) avant de commencer.

```bash
dsoxlab run pve-construire-template
dsoxlab challenge pve-construire-template
dsoxlab check pve-construire-template
```
