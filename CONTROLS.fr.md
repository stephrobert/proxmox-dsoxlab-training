# Contrôles du catalogue

Portage depuis `containers-dsoxlab-training`, mesuré le 5 novembre 2026.
Le dépôt source comporte **20 modules de tests**, dont 16 contrôles communs
repris ici. Quatre modules éprouvent des composants Docker absents du catalogue
Proxmox ; leurs cas sans objet sont explicités ci-dessous.

## Correspondance des tests

Les noms de modules désignent des fichiers sous `tests/` dans chaque dépôt.

| Module de Containers | Traitement dans Proxmox |
| --- | --- |
| `test_assertions_bilingues.py` | Déjà porté, conservé : deux arguments de langue requis et témoins de refus. |
| `test_assertions_non_nues.py` | Déjà porté, conservé. |
| `test_liens_internes.py` | Déjà porté, conservé. |
| `test_langue_officielle.py` | Déjà porté, conservé. |
| `test_verdicts_et_commun_separes.py` | Déjà présent, conservé avec son outil associé. |
| `test_meta_declare_les_labs.py` | Porté : appariement dans les deux sens, doublons et fichiers manquants. Les prérequis Docker et le libellé `_runtime_label` du générateur source ne sont pas applicables ici. |
| `test_hints_ecrits.py` | Porté : quatre indices bilingues, rédigés et encodés en base64 strict. Coûts Proxmox conservés : 5, 10, 15, 20. |
| `test_style_apprenant.py` | Porté : textes des labs, hors tolérance explicite des emoji des briefs. Le hook français existant reste en place. |
| `test_solutions_chiffrees.py` | Porté : en-tête Vault, fichiers présents et clé hors de Git. |
| `test_aucun_jeton_versionne.py` | Porté : motifs et témoins de secrets, périmètre Git vérifié par des fichiers témoins. Le seuil de 400 fichiers source ne décrit pas les 132 fichiers suivis ici. |
| `test_exigence_critique_declaree.py` | Porté : promesse non compensable et noms des contrôles déclarés. |
| `test_briefs_pointent_juste.py` | Porté : hôtes de `meta.yml`, chemins existants, répertoire de travail déclaré ou effectivement consommé par le contrôleur N3. |
| `test_images_epinglees.py` | Porté avec ses témoins : analyse des images de registre des setups et nettoyages, sans modifier les fixtures. Ce contrôle ne prétend pas épingler les images qcow2 ni les paquets PVE. |
| `test_outillage_coherent.py` | Adapté : chaque cible de chaque hook existe, les appels à `pytest tests/` couvrent leurs modules, contrat et catalogue restent contrôlés. |
| `test_maturite_des_labs.py` | Classification portée. Les tests du validateur Docker sont remplacés par `test_validateur_catalogue.py`, qui éprouve les refus du cycle et l'isolation impossible sans machine. Ils ne constituent pas une photographie des ressources PVE. |
| `test_ancres_trois_issues.py` | Porté avec `scripts/verifier-ancres.py` : ancre juste, fausse, page inaccessible, attentes périmées ou sans objet. Aucun fichier d'attentes Containers n'est copié. |
| `test_paquets_epingles.py` | Sans objet : vérifie les cinq paquets Docker de `infra/bootstrap.yaml`, absent ici. Aucun épinglage PVE n'est revendiqué par ce portage. |
| `test_capstone_recovery.py` | Sans objet : teste `_wait_ready` du lab Docker `capstone-chaine-complete`, absent ici. |
| `test_sonde_du_contexte_de_build.py` | Sans objet : teste la sonde du lab `buildkit-secret-de-build`, absent ici. |
| `test_index_multiarch_sans_attestations.py` | Sans objet : teste les index OCI du lab `images-multi-architecture`, absent ici. |

`test_garde_fous_portes.py` ajoute des témoins conformes et dégradés pour les
contrôles portés. Les contrôles Proxmox du contrat, du provisionnement et des
messages des contrôleurs restent également câblés.

## Correspondance des hooks

Les hooks communs de Containers sont présents : hygiène des fichiers,
YAML, JSON, TOML, conflits de casse et de fusion, gros fichiers, clés privées,
Ruff, parcours, indices, style, assertions, images, exigences critiques,
solutions, liens, langue, maturité, secrets, briefs, cohérence de l'outillage,
ancres, structure, catalogue, verrou et séparation des verdicts.

Les hooks des trois labs Docker absents et de leur bootstrap ne sont pas
ajoutés comme commandes mortes. Leurs quatre modules sont recensés dans la
table ci-dessus. Le contrôle de maturité inclut le validateur Proxmox.

Hadolint est adapté à la disposition réelle du catalogue : Dockerfile du dépôt
et de `solution/`, hors fixtures, travail apprenant et solutions en clair
ignorées. Un fichier Vault est déchiffré dans un temporaire avant analyse.
L'absence de Dockerfile est affichée comme `N/A`, et une clé absente comme
contrôle non joué. TruffleHog complète le contrôle des formes de secrets.
La CI installe les versions de Hadolint et TruffleHog reprises de Containers,
en vérifiant les empreintes publiées, avant de rejouer les hooks.

Le contrôle des ancres est au stade `pre-push`, car il utilise le réseau.
Les tests de ses trois issues utilisent des sondes simulées. La CI existante
rejoue les deux stades de la configuration pre-commit.

## Dette constatée le 5 novembre 2026

Les nouveaux contrôles sont **actifs et bloquants**, sans liste d'exemption
ajoutée pour obtenir du vert. La mesure locale donne :

| Dette | Mesure | Correction nécessaire |
| --- | --- | --- |
| Indices incomplets | 71 refus : 41 labs sans les quatre coûts attendus, 15 sans liste d'indices reconnue et 15 sans textes bilingues utilisables | Rédiger et encoder les quatre paliers des labs concernés. Les 15 derniers cas appartiennent aux mêmes 15 labs que les listes non reconnues. |
| Solutions manquantes | 41 refus | Livrer les solutions chiffrées des 41 labs en cours. Les six solutions présentes passent le contrôle de chiffrement. |
| Typographie | 54 fichiers refusés | Remplacer chaque tiret cadratin selon le sens de sa phrase. |

La suite locale comprend 1 880 cas : **1 616 réussites, 166 échecs, 98 sauts**.
Les sauts proviennent principalement de la tolérance explicite des emoji dans
les briefs, et des contrôles sans squelette ou sans liste d'ancres en attente.
Les nouveaux témoins de refus passent. Les détails par lab et fichier se
rejouent avec `pytest tests/ -q`.

La parité des hooks refuse également les défauts déjà présents avant ce
portage : métadonnées de `pve-reprendre-hors-site`, README générés périmés et
typographie française. Le chargement des playbooks et la résolution des noms
des tests passent. Ruff passe sur le code des contrôles portés ; le lint global
du catalogue conserve les défauts des labs en cours, que le hook ne parcourt
pas encore tant que leurs fichiers ne sont pas suivis par Git.

Les 46 `doc_url` renseignés n'ont actuellement aucun fragment : le hook des
ancres n'a donc aucune ancre réelle à juger. Ses témoins vérifient néanmoins
les refus. Le scan TruffleHog lancé sans changement à l'index a examiné zéro
octet : ce passage ne prouve pas l'absence de secrets dans les fichiers encore
non suivis. Le contrôle des formes a examiné le périmètre Git courant.

Aucune campagne Proxmox n'a été lancée et aucun verdict de lab n'a été modifié.
