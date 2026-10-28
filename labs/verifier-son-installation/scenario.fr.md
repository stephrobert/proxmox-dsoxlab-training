# Installez Proxmox, et faites noter votre installation

Vous recevez une machine **Debian 13 nue**. Aucun Proxmox dessus, et c'est
voulu : on n'apprend pas à installer un hyperviseur en le recevant installé.

Votre travail consiste à y installer **Proxmox VE 9**, puis à faire noter le
résultat. Le lab ne regarde pas les commandes que vous avez tapées, il mesure
l'**état de la machine**. Si vous arrivez au bon état par un autre chemin que
celui du guide, vous avez réussi.

## Ce qui est noté

**Six postes**, et ce sont ceux que vous accomplissez. Le cahier des charges
complet est sur la machine, dans `/opt/lab-proxmox/cahier-des-charges.md`.

| # | Poste | Comment il est vérifié |
|---|-------|------------------------|
| 1 | Proxmox VE est installé | `pveversion` répond |
| 2 | C'est bien une version 9 | le numéro majeur est 9 ou plus |
| 3 | Les services tournent | `pve-cluster`, `pvedaemon` et `pveproxy` sont actifs |
| 4 | L'interface web écoute | le port 8006 est tenu par `pveproxy` |
| 5 | Le pont existe | `vmbr0` est présent et porte l'adresse du serveur |
| 6 | Les mises à jour sont possibles | le dépôt `pve-no-subscription` est configuré, `apt-get update` passe |

## Ce qui est garanti, et n'est donc pas noté

Quatre autres postes du cahier des charges sont assurés par la machine qu'on
vous remet : la base **Debian 13**, la **virtualisation imbriquée** avec son
`/dev/kvm`, le **dimensionnement** à 4 vCPU et 6 Go, et la présence d'un
**second disque brut** de 20 Go.

Ce sont des prérequis, pas des acquis : les noter reviendrait à vous créditer
d'un travail que vous n'avez pas fait. Le lab les vérifie quand même, mais au
démarrage, et il refuse de s'ouvrir si l'un manque, avec le message qui dit
lequel.

Ces quatre postes comptent en revanche pleinement quand vous installez Proxmox
sur **votre propre machine**, hors de ce lab : c'est là que le cahier des
charges complet prend son sens.

## Deux pièges qui coûtent cher

**Le second disque doit rester brut.** Il est tentant de l'intégrer tout de
suite à un volume ou à un pool. Ne le faites pas : les labs de stockage qui
suivent y construiront leur propre pool ZFS ou LVM-thin, et ils ont besoin
d'un disque vierge. Rien ne vous en empêchera ici, et c'est justement pour cela
qu'il faut le savoir : la conséquence se paiera deux leçons plus loin.

**L'adresse doit vivre sur le pont, pas sur la carte réseau.** Un Proxmox
installé par-dessus Debian garde, tant qu'on ne fait rien, son adresse sur la
carte physique. Il faut créer le pont `vmbr0`, lui donner l'adresse, et mettre
la carte physique en `manual` comme port du pont. C'est par ce pont que vos
futures machines virtuelles rejoindront le réseau.

## Un troisième piège, plus sournois

La **résolution du nom d'hôte** doit rendre une adresse routable. Si
`hostname --ip-address` répond `127.0.1.1`, le service `pve-cluster` ne
démarrera pas, et l'installation échouera sur un message qui ne dit pas sa
cause :

```text
ipcc_send_rec[1] failed: Connection refused
```

Vérifiez donc votre `/etc/hosts` **avant** d'installer les paquets.

## Comment procéder

Le guide décrit la marche à suivre, section « Quelle méthode d'installation
choisir dans une VM » :
<https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/installation/>

La procédure officielle de Proxmox, pour la voie Debian, est sur leur wiki :
<https://pve.proxmox.com/wiki/Install_Proxmox_VE_on_Debian_13_Trixie>

Un point d'ordre que l'on saute souvent : installez d'abord le **noyau**
Proxmox, **redémarrez dessus**, et installez seulement ensuite les paquets
Proxmox. Les installer d'affilée laisse la machine sur le noyau Debian.

## Faire noter votre travail

```bash
dsoxlab check verifier-son-installation
```

Chaque poste en défaut est nommé, avec ce qu'il faut corriger. Un échec n'est
pas une fin : corrigez, puis relancez la notation autant de fois que
nécessaire.

## Recommencer de zéro

`dsoxlab clean` retire la consigne, mais **ne désinstalle pas Proxmox** :
arracher Proxmox d'un Debian ne rend pas une Debian nue, cela rend une Debian
abîmée. Pour repartir vraiment du début, détruisez la machine et
reprovisionnez-la.
