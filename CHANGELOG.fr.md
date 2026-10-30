# Journal des modifications

Les changements notables de ce catalogue sont consignés ici. Le format suit
[Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), et ce catalogue suit
le [versionnage sémantique](https://semver.org/lang/fr/).

**Ce qu'une version veut dire ici.** Un catalogue n'est pas une bibliothèque :
un incrément MINEUR ajoute des labs, un CORRECTIF corrige un énoncé ou un test
sans changer ce qu'un lab prouve, et un incrément MAJEUR renomme ou retire des
labs, ce qui casse la progression déjà enregistrée des apprenants.

## [Non publié]

### Ajouté

- Le squelette du catalogue, créé par `dsoxlab new catalog`.
- **Le premier lab, `verifier-son-installation`** : il note, poste par poste,
  une installation de Proxmox VE 9 que l'apprenant a faite lui-même sur une
  Debian 13 nue, avec quatre indices bilingues à coût croissant et un README
  de challenge.
- **Cinq labs du niveau 1**, chacun attesté 0 → 100 sur machine neuve :
  `pve-raccorder-instance` (rebrancher une VM sur le bon pont sans la
  recréer), `pve-suivre-tache` (rattacher chaque résultat à sa tâche par
  l'UPID), `pve-creer-vm` (contrat matériel, démarrage sur disque, service
  qui revient après un redémarrage), `pve-creer-lxc` (conteneur non
  privilégié, limites lues dans les cgroups) et `pve-reparer-agent` (agent
  invité rétabli sans arrêt forcé, panne tirée parmi deux cas).
- `shared/noeud-proxmox.yml`, une garde qui ne rejoue l'installation
  attestée de Proxmox que si le nœud n'est pas prêt, et
  `shared/image-debian-cloud.yml`, l'image cloud Debian 13 vérifiée par sa
  somme.
- **L'outillage des catalogues frères** : `scripts/valider-labs.py` et
  `validation-labs.json`, qui attestent un lab dans les deux sens (0 avant le
  travail, 100 après la solution) ; `gen_catalog.py`, `check-playbooks.py`,
  `check-tests.py`, `chiffrer-solutions.sh`, `rebase-vms.sh` et les garde-fous
  de `tests/`.
- **La chaîne de sécurité du dépôt public** : workflows `plumber` et
  `scorecard`, configuration CodeQL, `dependabot`, `CODEOWNERS`, modèles
  d'issue, `.poutine.yml`, `.plumber.yaml`, `uv.lock`, et le hook `pre-commit`
  repris des frères.

### Modifié

- **Les sections suivent les niveaux de la formation** : déployer, sécuriser
  et exploiter, cluster et disponibilité, automatiser, puis les options. Les
  sections encore vides sont déclarées, pas masquées.
- `README`, `RELEASING`, `pyproject.toml` et `meta.fr.yml` sont remplis sur la
  forme des frères ; ils portaient encore les textes du squelette et le nom
  provisoire `proxmox`.
- Les actions GitHub sont épinglées sur les mêmes versions que les frères.
