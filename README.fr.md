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
- **Un accès réseau sortant**, pour l'image de base et les dépôts Proxmox.

Une machine virtuelle, `pve.lab` (Debian 13, 4 vCPU, 6 Go, 40 Go de disque
système et un second disque brut de 20 Go), déclarée dans `meta.yml` et créée
par `dsoxlab provision`. Proxmox VE remplace le noyau de la machine et prend la
main sur son réseau : rien ne tourne sur votre poste.

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
dsoxlab provision                          # crée pve.lab, une Debian 13 nue
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
| `vm` | la machine `pve.lab`, créée par `dsoxlab provision`, sous Debian 13, avec la virtualisation imbriquée. L'apprenant y installe Proxmox VE, puis y crée ses invités. |

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

À jouer dans l'ordre. D'autres labs s'ajoutent à mesure qu'ils sont écrits et
prouvés dans les deux sens.

<!-- LABS:START -->
### Déployer un nœud et ses premières instances

Installer Proxmox VE, depuis l'ISO ou sur une Debian 13, et le vérifier face à un cahier des charges ; créer une VM KVM et un conteneur LXC non privilégié, construire un modèle, restaurer une première instance.

| Lab (id) | Titre | Niveau | Runtime | Guide compagnon |
|---|---|---|---|---|
| `verifier-son-installation` | Vérifier votre installation de Proxmox face au cahier des charges | l1 | vm | [guide](https://www.stephane-robert.info/docs/virtualiser/type1/proxmox/fondamentaux/installation-debian/) |

_1 labs, table générée par `scripts/gen_catalog.py`._
<!-- LABS:END -->

## Contribuer

Lis [`CONTRIBUTING.fr.md`](./CONTRIBUTING.fr.md). En bref : un lab est prouvé
**dans les deux sens** avant d'être fusionné, `dsoxlab validate-structure` est
vert, et l'énoncé existe en anglais et en français.

Tout ce qui s'affiche est bilingue. Un document traduit d'un seul côté est
signalé par le validateur, et non laissé à la bonne volonté.

## Licence

Voir [`LICENSE`](./LICENSE).
