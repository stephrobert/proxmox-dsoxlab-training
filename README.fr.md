# Formation Proxmox VE : installer, exploiter, sécuriser et automatiser un hyperviseur de type 1

**Langue :** [English](./README.md) · [Français](./README.fr.md)

[![CI](https://github.com/stephrobert/proxmox-dsoxlab-training/actions/workflows/ci.yml/badge.svg)](https://github.com/stephrobert/proxmox-dsoxlab-training/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://img.shields.io/ossf-scorecard/github.com/stephrobert/proxmox-dsoxlab-training?label=OpenSSF%20Scorecard)](https://securityscorecards.dev/viewer/?uri=github.com/stephrobert/proxmox-dsoxlab-training)
[![Plumber compliance](https://score.getplumber.io/github.com/stephrobert/proxmox-dsoxlab-training.svg)](https://score.getplumber.io/github.com/stephrobert/proxmox-dsoxlab-training)
[![SLSA 3](https://slsa.dev/images/gh-badge-level3.svg)](https://slsa.dev)
[![Licence : CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](./LICENSE)

Des labs vérifiables pour la formation
[« Proxmox VE »](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/)
du blog, joués avec [dsoxlab](https://github.com/stephrobert/dsoxlab).

## Ce que c'est

À la fin, l'apprenant sait installer Proxmox VE sur une machine qu'il ne
connaît pas, y créer des machines virtuelles et des conteneurs, les sauvegarder
et **prouver qu'il sait les restaurer**, puis exploiter un cluster et
automatiser la plateforme par son API. Pas une liste de sujets : chaque lab se
termine sur un état que les tests interrogent, comme un nœud conforme, une
instance qui répond ou une restauration qui rend le service.

L'ordre compte. Le catalogue ne livre **pas** un Proxmox prêt à l'emploi :
l'apprenant l'installe lui-même, selon un cahier des charges publié dans la
leçon, et le premier lab vérifie cette installation poste par poste. On
n'apprend pas à installer un hyperviseur en le recevant installé.

**Un lab est noté sur l'état du système, jamais sur les commandes tapées.**
L'apprenant atteint le résultat par le chemin qu'il choisit.

## Prérequis

- **Python 3.11+ et [`uv`](https://docs.astral.sh/uv/)**
- **`git`**
- **`dsoxlab`**, le moteur, installé en outil autonome (voir plus bas).
- **Un hyperviseur**, parce que tous les labs sont en `runtime: vm` :
  **libvirt/KVM** (avec `terraform` et le provider `dmacvicar/libvirt`) est le
  provider par défaut, déclaré dans [`meta.yml`](./meta.yml).
- **La virtualisation imbriquée active** sur l'hôte : Proxmox VE crée lui-même
  des machines, donc la VM qui le porte doit exposer les extensions de
  virtualisation du processeur. Sous Linux,
  `cat /sys/module/kvm_intel/parameters/nested` (ou `kvm_amd`) doit rendre `Y`.
- **6 Go de RAM libre et 60 Go de disque** pour l'unique machine, `pve.lab`.
- **Pour les labs cluster :** un hôte distinct de 48 Go, dont 24 Go réservés
  aux trois nœuds, et au moins 280 Go libres dans le pool libvirt.
- **Un accès réseau sortant**, pour l'image de base et les dépôts Proxmox.

Une machine virtuelle, `pve.lab` (Debian 13, 4 vCPU, 6 Go, 40 Go de disque
système et un second disque brut de 20 Go), déclarée dans `meta.yml` et créée
par `dsoxlab provision --host pve.lab`. Proxmox VE remplace le noyau de la
machine et prend la main sur son réseau : rien ne tourne sur votre poste.

Les labs cluster utilisent une cible distincte `proxmox-cluster` :
`pve01.lab`, `pve02.lab` et `pve03.lab`, chacune avec 4 vCPU, 8 Go de RAM, un
disque système de 40 Go et un disque supplémentaire de 40 Go. Le démarrage d'un
lab cluster provisionne ces trois machines Debian 13 à la demande via le
backend KVM. Cela ne crée **pas** le cluster Proxmox : l'apprenant doit le
construire avec `pvecm`. Pour conserver les 24 Go réservés à l'hôte, utilisez
les environnements mono-nœud et cluster l'un après l'autre.

Pour démarrer explicitement un lab cluster :

```bash
dsoxlab start pve-eprouver-cluster --target proxmox-cluster
```

Ne lancez pas `dsoxlab provision` sans filtre : cette commande applique tout le
catalogue. Lancez ce prévol de capacité en lecture seule, puis sélectionnez
explicitement la cible cluster :

```bash
uv run python scripts/provision_cluster.py
dsoxlab start pve-eprouver-cluster --target proxmox-cluster
```

Le prévol exige au minimum 26 Gio de RAM disponible, 280 Gio libres dans le
pool libvirt, 12 CPU logiques et une charge CPU modérée. Les machines cluster
peuvent ensuite lancer des invités supplémentaires. Le démarrage du lab
provisionne les trois nœuds via le backend KVM ; il ne forme jamais le cluster.
`--apply` du script est une autre méthode pour provisionner manuellement ces
hôtes avant de démarrer un lab. `dsoxlab destroy` sans filtre détruit toute
l'infrastructure du catalogue, pas seulement le cluster.

`dsoxlab doctor` dit ce dont ce dépôt a besoin et ce dont il n'a pas besoin, et
distingue un contrôle qui a échoué d'un contrôle qu'il n'a pas pu mesurer.

## Installation

`dsoxlab` est publié sur [PyPI](https://pypi.org/project/dsoxlab/).
Installe-le en outil autonome, pour qu'il reste hors de ce dépôt :

```bash
# 1. La CLI dsoxlab (outil externe, hors de ce dépôt)
uv tool install dsoxlab

# 2. Ce catalogue de labs
git clone https://github.com/stephrobert/proxmox-dsoxlab-training.git
cd proxmox-dsoxlab-training

# 3. Vérifier le contrat et la machine
dsoxlab validate-structure
dsoxlab doctor
```

### Votre premier lab

```bash
export LAB_HOME=$PWD
dsoxlab provision --host pve.lab            # crée uniquement le nœud de base
dsoxlab list-labs                          # le catalogue, dans l'ordre pédagogique
dsoxlab run       verifier-son-installation
dsoxlab challenge verifier-son-installation   # le cahier des charges à tenir
dsoxlab check     verifier-son-installation   # le verdict, poste par poste
```

Entre `challenge` et `check`, c'est vous qui installez Proxmox VE sur `pve.lab`,
en suivant la leçon
[« Installer Proxmox VE sur Debian 13 »](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/installation-debian/).
Comptez une trentaine de minutes.

C'est `run` qui prépare le lab. Un `check` joué sur un lab jamais démarré ne
mesure rien, et le dit au lieu d'enregistrer un 0.

### Garder à jour

```bash
uv tool upgrade dsoxlab        # le moteur, publié sur PyPI
git -C <ce dépôt> pull         # le catalogue
```

Le moteur et le catalogue avancent indépendamment : un nouveau `dsoxlab` ne
demande jamais de recloner les labs, et de nouveaux labs ne demandent jamais de
mettre l'outil à jour, tant que la version du contrat correspond.

## Comment ça marche

### Le contrat déclaratif, à deux niveaux

Le catalogue est décrit par des données, pas par du code, et c'est ce qui garde
le moteur `dsoxlab` indépendant du domaine :

- **`meta.yml`** à la racine déclare l'identité du dépôt et l'**ordre** des
  sections affichées par `list-labs` ;
- **`lab.yaml`** par lab déclare ses `skills`, son `level`, son `runtime`
  (type, fixtures, services), ses `distros`, son `doc_url` et un bloc
  `validation`. Un `lab.fr.yaml` surcharge `title` et `description` en
  français, et rien d'autre.

`dsoxlab validate-structure` contrôle tout le contrat : `meta.yml` bien formé,
chaque lab référencé présent avec un `lab.yaml` valide, chaque fichier de test
et de fixture déclaré réellement là, et chaque lien relatif d'un README qui
mène quelque part.

### Le cycle de vie d'un lab

```bash
dsoxlab list-labs              # parcourir le catalogue
dsoxlab show      <id>         # métadonnées et état d'un lab
dsoxlab run       <id>         # poser l'état de départ
dsoxlab challenge <id>         # lire la mission, sans pas-à-pas
dsoxlab hint      <id>         # révéler un indice (déduit du score)
dsoxlab check     <id>         # lancer les tests, calculer et enregistrer le score
dsoxlab clean     <id>         # défaire ce que le lab a posé
dsoxlab progress               # avancement par section, score moyen
```

### Les runtimes

Tous les labs sont en `vm` : Proxmox VE ne s'installe pas sur un poste de
travail, et ses invités vivent dans la machine, pas sur l'hôte de l'apprenant.

| Runtime | Ce que le lab demande |
|---|---|
| `vm` | la machine `pve.lab` pour les labs ordinaires, créée de façon ciblée, sous Debian 13, avec la virtualisation imbriquée. Les labs cluster sélectionnent la cible séparée `proxmox-cluster`, dont les trois nœuds sont provisionnés à la demande ; l'apprenant construit le cluster. |

### Le modèle de validation

La validation **prouve l'état, elle ne fait pas confiance à l'apprenant**.
Chaque lab porte des tests `pytest` sous `challenge/tests/` qui lisent ce que
le système contient, jamais ce qu'un fichier contient ni quelles commandes ont
été tapées.

Et un lab est prouvé **dans les deux sens** : les tests doivent échouer avant
le travail et passer après. Un test vert avant le travail n'est pas un test,
c'est une hypothèse sur le setup.

Les solutions de référence vivent sous `solution/<lab>/`, chiffrées avec
`ansible-vault` ; le mot de passe (`.vault-pass` à la racine) n'est jamais
versionné. Une solution en clair gâcherait le lab, et git la garde pour
toujours.

La CI GitHub vérifie le contrat, les workflows et la qualité du dépôt, mais ne
provisionne aucune VM et ne rejoue pas les labs. Son badge ne vaut donc pas
attestation pédagogique : le cycle runtime 0 → 100 est vérifié séparément avec
`python3 scripts/valider-labs.py --lab <id>` sur une infrastructure provisionnée.

### Score, indices, avancement

`check` enregistre un score (tests réussis sur total, moins le coût des indices
révélés). Les indices sont **en base64** dans `challenge/hints.yaml`, pour qu'on
n'y accède pas en ouvrant le fichier, et leur coût croît avec leur précision.
L'historique vit dans une base SQLite **locale à ce dépôt**.

Une exécution qui n'a rien mesuré n'est ni une réussite ni un échec : si tous
les tests collectés skippent, `check` n'enregistre aucune note et dit pourquoi.
Un 0 accuserait le lab de ce qui manque au poste.

## Catalogue

À jouer dans l'ordre. La présence au catalogue signifie que le lab est écrit,
pas qu'il est attesté. Il n'est prouvé qu'après échec des tests avant le geste
et réussite après celui-ci sur l'environnement cible.

<!-- LABS:START -->
### Concevoir et qualifier le premier nœud

Préparer un laboratoire isolé et raccorder un invité au réseau attribué.

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `pve-preparer-laboratoire` | Préparer un laboratoire et son plan de ressources | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-raccorder-instance` | Raccorder une VM au réseau et corriger la panne au bon étage | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/reseau/) |

### Déployer un nœud et ses premières instances

Installer Proxmox VE, depuis l'ISO ou sur Debian 13, puis vérifier sa conformité ; créer une VM KVM et un conteneur LXC non privilégié, construire un modèle et restaurer un premier service.

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `pve-installer-noeud` | Installer Proxmox et établir un accès fiable | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/installation/) |
| `verifier-son-installation` | Vérifier votre installation de Proxmox face au cahier des charges | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/installation-debian/) |
| `pve-suivre-tache` | Lire les tâches de Proxmox : rattacher chaque résultat à sa tâche | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/interface-ui/) |
| `pve-creer-vm` | Créer une VM KVM et vérifier que son service répond | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/creer-vm-kvm/) |
| `pve-creer-lxc` | Créer un conteneur LXC non privilégié aux ressources bornées | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/conteneurs-lxc/) |
| `pve-reparer-agent` | Rétablir l'agent invité QEMU sans forcer l'arrêt de la VM | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/qemu-guest-agent/) |
| `pve-gerer-cycle-vie` | Redimensionner une VM et prouver un retour local | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-construire-template` | Construire un template cloud-init et des clones indépendants | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-restaurer-premiere-instance` | Sauvegarder et restaurer une première VM sur un réseau isolé | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-epreuve-deploiement` | Livrer et restaurer un premier service virtualisé | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |

### Sécuriser les identités et les frontières

Déléguer les droits, sécuriser les identités et filtrer les flux de gestion et des invités.

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `pve-deleguer-acces` | Déléguer les droits sans élargir le périmètre | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-securiser-identites` | Sécuriser les identités, jetons et connexions | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-filtrer-flux` | Filtrer le management et les invités | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-maitriser-volumes-lxc` | Gérer les volumes et identités des LXC | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |

### Exploiter les réseaux des invités

Segmenter les VLAN, router les flux et modifier le réseau de façon réversible.

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `pve-segmenter-vlan` | Segmenter et diagnostiquer les VLAN | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-changer-reseau` | Router, traduire et modifier le réseau sans se couper | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |

### Sauvegarder et restaurer avec PBS

Intégrer PBS, protéger les clés de sauvegarde et prouver la reprise du service.

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `pve-integrer-pbs` | Déployer PBS et réaliser une sauvegarde vérifiable | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-proteger-sauvegardes` | Chiffrer, conserver et vérifier les sauvegardes | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-prouver-restauration` | Restaurer un service et mesurer RPO et RTO | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |

### Observer, diagnostiquer et maintenir

Observer la capacité, diagnostiquer un invité indisponible et maintenir un nœud.

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `pve-observer-alerter` | Observer la capacité et recevoir les alertes | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-diagnostiquer-instance` | Diagnostiquer une VM indisponible | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-maintenir-noeud` | Maintenir un nœud et préparer une montée de version | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-exploiter-thin-pool` | Exploiter Directory et LVM-thin sans saturation | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-restaurer-redondance-zfs` | Exploiter un miroir ZFS et récupérer un disque | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |
| `pve-epreuve-exploitation` | Sécuriser, diagnostiquer et restaurer une plateforme | l2 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/) |

### Exploiter un cluster et sa disponibilité

Construire un cluster de trois nœuds, migrer et répliquer les invités, éprouver la haute disponibilité face à une panne imposée de l'extérieur, et reprendre après la perte du site primaire.

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `pve-eprouver-cluster` | Construire et éprouver le cluster | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/chapter-pvecm.html) |
| `pve-qualifier-stockage-partage` | Qualifier le stockage partagé et ses limites | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/chapter-pvesm.html) |
| `pve-migrer-instance` | Migrer une VM et un CT en mesurant l’impact client | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/chapter-qm.html) |
| `pve-reserver-capacite` | Réserver la capacité N-1 et imposer le placement | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/) |
| `pve-mesurer-replication` | Mesurer la réplication ZFS et la frontière récupérable | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/chapter-pvesr.html) |
| `pve-eprouver-ha` | Éprouver la reprise du service sans double écrivain | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/chapter-ha-manager.html) |
| `pve-maintenir-cluster` | Maintenir un nœud en préservant le contrat de service | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/) |
| `pve-reprendre-hors-site` | Reprendre depuis un PBS secondaire sans dépendance primaire | l3 | vm | - |
| `pve-epreuve-disponibilite` | Épreuve de disponibilité et reprise indépendante | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/chapter-ha-manager.html) |

### Automatiser une plateforme reproductible

Piloter l'API et attendre les résultats réels, provisionner avec Terraform sous des droits mesurés, construire un inventaire Ansible fiable, et livrer une plateforme qu'un contrôleur vierge sait reconstruire.

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `pve-piloter-api` | Piloter l’API et attendre les résultats réels | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/api-viewer/) |
| `pve-provisionner-terraform` | Provisionner avec Terraform et des droits mesurés | l3 | vm | [guide](https://registry.terraform.io/providers/bpg/proxmox/latest/docs) |
| `pve-reconcilier-etat` | Maîtriser état, dérive et changements destructeurs | l3 | vm | [guide](https://registry.terraform.io/providers/bpg/proxmox/latest/docs) |
| `pve-fiabiliser-inventaire` | Construire un inventaire Ansible fiable | l3 | vm | [guide](https://docs.ansible.com/ansible/latest/inventory_guide/intro_dynamic_inventory.html) |
| `pve-operer-ansible` | Automatiser les opérations avec Ansible | l3 | vm | [guide](https://docs.ansible.com/ansible/latest/collections/community/proxmox/proxmox_module.html) |
| `pve-livrer-plateforme` | Livrer une recette reproductible et transférable | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/) |
| `pve-epreuve-automatisation` | Livrer une plateforme reproductible par API et IaC | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/) |

### Options

Windows avec VirtIO, migration VMware, Ceph et SDN. Chaque option est indépendante, et aucune ne bloque un niveau.

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `pve-integrer-windows` | Exploiter une VM Windows avec VirtIO | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/) |
| `pve-migrer-vmware` | Migrer une charge VMware avec une recette de bascule | l3 | vm | [guide](https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE) |
| `pve-eprouver-ceph` | Déployer et dépanner un stockage Ceph | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/chapter-pveceph.html) |
| `pve-deployer-sdn` | Construire un réseau SDN adapté à la charge | l3 | vm | [guide](https://pve.proxmox.com/pve-docs/chapter-pvesdn.html) |

_47 labs, table générée par `scripts/gen_catalog.py`._
<!-- LABS:END -->

## Contribuer

Lis [`CONTRIBUTING.fr.md`](./CONTRIBUTING.fr.md). En bref : un lab est prouvé
**dans les deux sens** avant d'être fusionné, `dsoxlab validate-structure` est
vert, et l'énoncé existe en anglais et en français.

Tout ce qui s'affiche est bilingue. Un document traduit d'un seul côté est
signalé par le validateur, et non laissé à la bonne volonté.

## Licence

Voir [`LICENSE`](./LICENSE).
