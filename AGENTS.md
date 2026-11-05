# Travailler sur ce catalogue de labs

Ce dépôt est un **catalogue de labs** piloté par le framework `dsoxlab`. Il
fournit des labs Proxmox : un `meta.yml` racine, un `lab.yaml` par lab, des
playbooks de préparation et de nettoyage, des tests qui prouvent l'état du
système, et une solution de formateur chiffrée.

Ce document porte la **méthode**, pas le contrat. Le contrat déclaratif
(`meta.yml`, `lab.yaml`, runtimes, codes de sortie) est documenté dans
`dsoxlab` et vérifié par `dsoxlab validate-structure`. Ce que vous lisez ici,
aucun schéma ne l'impose : ce sont les règles qui ont été payées par des
défauts réels, chacune avec le cas qui l'a produite.

> **Toute règle de ce document est accompagnée de sa mesure.** Si une affirmation
> vous paraît fausse, remesurez-la et corrigez le document : il décrit le code
> et les faits, pas l'intention. Un document de méthode qui mente est pire
> qu'absent, parce qu'il fait écrire du faux avec assurance.

---

## 1. Les règles non négociables

### On tire `main`, on crée la branche, puis on code

```bash
git -C . switch main && git -C . pull     # partir d'un main à jour
git -C . switch -c <type>/<sujet-court>   # ex. fix/rootless-huit-controles
```

Coder d'abord et brancher ensuite marche tant que rien ne diverge, mais c'est
un coup de chance : la moindre avance de `origin/main` transforme le rattrapage
en rebase manuel sur un arbre sale.

- **Commit et `git push` uniquement quand l'utilisateur le demande.** Sans
  demande, s'arrêter à « prêt à committer » et lister ce qui a changé.
- Aucune ouverture de PR autonome. Sur demande explicite, la créer en
  remplissant réellement le gabarit : chaque case cochée correspond à un
  contrôle joué, et un bloc sans objet porte un `N/A` motivé.
- Après ouverture, **ne pas conclure tant que la CI tourne**. Rapporter le
  résultat réel, pas l'espéré.
- Jamais de commit direct sur `main`.
- **Jamais `git add -A`.** Le durcissement de l'environnement pose des nœuds
  `/dev/null` que `git status` affiche en untracked. Ajouter les fichiers un
  par un.
- **Nommer le dépôt dans chaque commande.** Une session touche souvent deux
  dépôts, et le répertoire courant revient à son point de départ entre deux
  appels sans rien signaler. Donc `git -C /chemin/absolu`, jamais un `cd` posé
  trois commandes plus tôt. Un `git status` qui affiche les fichiers d'un autre
  dépôt est un signal d'arrêt, pas une curiosité.
- Un message de commit va dans un **fichier**, jamais dans `git commit -m`.
  Les backticks d'un message inline sont des substitutions de commande : elles
  remplacent silencieusement des fragments du texte par la sortie d'une
  commande. Vécu, et le commit a été poussé avant qu'on le voie.

### Écrire en français, avec tous ses accents, et jamais d'em-dash

Les énoncés et la documentation sont bilingues EN + FR. Côté français :
accentuation complète (`sécurité`, `contrôle`, `nécessaire`), et **jamais** le
tiret cadratin `—` comme séparateur. À sa place : deux-points pour introduire,
virgules ou parenthèses pour une incise, point ou point-virgule pour une
rupture.

Contrôle avant livraison : `grep -c '—' <fichier>` doit rendre **0** sur tout
fichier écrit ou modifié.

Une exception, et une seule : ce document **cite** le caractère qu'il interdit,
parce qu'on ne peut pas l'interdire sans l'écrire. Ses trois occurrences sont
entre accents graves. Un garde-fou qui compterait les occurrences brutes
refuserait donc le document même, et serait rouge en permanence : s'il est
écrit un jour, il exempte ce qui est cité, et il nomme son exemption au lieu de
la laisser implicite.

Le journal technique, lui, s'écrit en **anglais** : il se cherche mot pour mot
dans un moteur de recherche et se compare entre machines aux locales
différentes.

---

## 2. La loi de ce dépôt : un contrôle doit pouvoir refuser

C'est la règle qui gouverne toutes les autres, et c'est celle qu'on oublie.

### Le cycle de validation ne prouve pas qu'un contrôle sait refuser

`scripts/valider-labs.py` joue, pour chaque lab :

```
0. photographie de l'état (machines, ressources)
1. dsoxlab run       l'état initial est posé
2. dsoxlab check     DOIT rendre 0   : le travail n'est pas fait
3. la solution du formateur est posée
4. dsoxlab check     DOIT rendre 100 : le travail est fait
5. clean, run, check DOIT rendre 0   : le point de départ se rejoue
6. photographie à nouveau : aucun écart admis
```

Ce cycle est nécessaire et **il ne suffit pas**. Il soumet deux états : rien de
fait, et tout bien fait. Il ne soumet **jamais** de travail faux. Un contrôle
qui ne regarde rien passe donc les deux étapes : il échoue sur un répertoire
vide parce que la commande n'existe pas, et il réussit sur la solution parce
que tout est là.

**Neuf contrôles incapables de refuser ont été trouvés de cette manière dans un
catalogue voisin, tous au vert dans le cycle.**

### La triche : le seul contrôle qui vaille

Pour chaque contrôle ajouté ou corrigé, **dégrader un seul facteur** et
vérifier qu'il refuse. La règle de méthode :

> **Vérifier que la dégradation a bien eu lieu AVANT de lire le verdict.**

Sans cette vérification, un refus peut venir de la dégradation ou d'une panne
du banc, et les deux sont indiscernables. Exemple vécu, sur un lab qui
enseigne le démon sans privilèges : le démon a été remplacé par un relais vers
le démon privilégié, puis on a relevé, avant tout verdict :

| fait relevé | valeur |
|---|---|
| service | `active` |
| UID du processus | 999, le compte dédié |
| racine de données | `/var/lib/docker`, celle du privilégié |
| options de sécurité | sans « rootless » |

Tout ce qui est facile à satisfaire l'était, et ce que le lab enseigne
manquait. **Deux contrôles ont refusé, exactement les deux prédits.** Les six
autres ont passé, ce qui est juste : ils étaient vrais face à ce moteur.

Une triche bien choisie satisfait ce qui est facile et manque ce qui est
enseigné. Une triche qui casse tout ne mesure rien.

### Un contrôle doit être rejouable

Lancer `dsoxlab check` **deux fois de suite**. Les deux doivent rendre le même
verdict.

Vécu : un contrôle chargeait une image pour sa mesure et ne la retirait pas.
Premier `check` rc=0, second rc=1, **sans que rien ne change entre les deux**.
Le lab passait au rouge pour la seule raison qu'on l'avait relancé. Un contrôle
qui ne se rejoue pas ne mesure que son premier passage.

Corollaire : ce qu'un contrôle fabrique pour mesurer, il le retire. Et il le
retire **sans `assert`** (voir plus bas).

---

## 3. Reconnaître un harnais de mesure en panne

Huit bancs de mesure ont été cassés en une semaine de travail sur un catalogue
voisin. **Aucun n'a été trouvé par relecture.** Tous l'ont été par un garde-fou,
une contradiction interne, ou un résultat trop uniforme. D'où ces signes, à
traiter comme des arrêts :

| signe | ce que c'est presque toujours |
|---|---|
| une série de contrôles indépendants échoue d'un coup | le banc, pas le sujet |
| un résultat accuse tout le catalogue | la lecture du relevé, pas le catalogue |
| un refus survient sans qu'on ait rien dégradé | le banc |
| un verdict est identique dans tous les cas, y compris celui censé réussir | le banc ne mesure plus que sa propre panne |

Deux cas concrets, pour que vous les reconnaissiez :

- un comptage comparait un verdict à `"valide"` quand le champ portait
  `"VALIDE"` : il a annoncé les 91 labs comme non valides. Depuis, le comptage
  porte son propre garde-fou : **il échoue s'il ne trouve aucun VALIDE**, parce
  qu'un catalogue entièrement rouge est bien plus probablement une lecture en
  panne ;
- un `sed 's/ *#.*//'` posé pour nettoyer des commentaires supprimait aussi les
  ancres d'URL qu'il servait justement à comparer. Les deux côtés paraissaient
  identiques, et ils ne l'étaient pas.

**Règle qui en découle : un script de mesure porte un garde-fou sur son propre
fonctionnement.** Un total attendu, une valeur témoin, une assertion qui
échoue si la mesure n'a pas pu avoir lieu. Une mesure qui n'a pas eu lieu ne
conclut jamais au vert.

### Hygiène shell, qui est une cause de panne de banc à elle seule

Le shell de connexion est `zsh`, et il ne se comporte pas comme bash.

- **Quoter tout motif destiné à la commande** : `--include='*.py'`, jamais
  `--include=*.py`. Sans correspondance dans le répertoire courant, zsh fait
  une **erreur fatale** là où bash transmet le motif.
- **zsh ne découpe pas** une variable non quotée en mots : `commande $args`
  passe toute la chaîne comme **un seul argument**. Un script qui dépend du
  découpage porte un shebang `#!/usr/bin/env bash`.
- **Un script de plus d'une ligne va dans un fichier.** Déclencheur mécanique :
  compter `<<`, `'`, `"`, `$(` dans la commande. **Dès que deux cohabitent,
  écrire un fichier.** Ne pas juger au cas par cas si « ça devrait passer » :
  c'est exactement le raisonnement qui produit l'échec.
- Dans une boucle `while read`, **toute commande reçoit `< /dev/null`**, sinon
  elle consomme l'entrée de la boucle et la boucle saute des éléments en
  silence.
- Ne pas comparer une sortie tronquée : `git rev-parse --short HEAD`, jamais un
  `cut` sur `git log --oneline`, qui compare « 5e67b79 f » à « 5e67b79 ».

### Vérifier n'est pas parser

Contrôler la syntaxe d'un fichier généré ne prouve pas qu'il s'exécute.
`ast.parse` accepte un module Python dont une variable a été supprimée par une
substitution malheureuse : le fichier est valide, et lève au premier appel.

**Le contrôle porte sur le comportement, jamais sur la forme.** Un fichier
généré se vérifie en l'exécutant ; un test se vérifie en le faisant échouer
quand il doit échouer.

---

## 4. Écrire un lab : l'énoncé et les contrôles disent la même chose

Deux défauts **symétriques**, et il faut chasser les deux. Ils ont occupé
l'essentiel du travail de reprise d'un catalogue voisin.

### Défaut A : une exigence mesurée sans être annoncée

Un contrôle exige quelque chose que l'énoncé ne demande pas. L'apprenant perd
des points sur un geste qu'on ne lui a pas demandé : **le lab mesure sa
débrouille, pas son apprentissage.**

Cas vécus : un contrôle exigeait un mot accentué quand l'énoncé l'écrivait en
ASCII ; un autre exigeait un mode `enforce` dont rien n'était observable ; un
troisième promettait « sans TLS » alors que tout le trafic était refusé.

### Défaut B : une exigence annoncée sans être demandée

L'inverse, et il est plus difficile à voir parce que les contrôles passent.

Cas vécu, sur un lab de démon sans privilèges : la préparation posait tout et
s'arrêtait volontairement avant le dernier geste, que sa dernière tâche nommait
en clair. La solution du formateur faisait **un** geste. Mais l'énoncé
promettait : « son moteur doit exécuter un vrai service HTTP, autoriser le pair
de son réseau et refuser un pair sans réseau ». Les contrôles **fabriquaient
eux-mêmes** ce décor pour prouver que le moteur fonctionnait.

Un apprenant montait donc un serveur, un réseau et un volume **pour rien**,
puis voyait passer un `check` auquel il n'avait pas touché.

**La parade est la même dans les deux sens.** Avant de livrer un lab, lister
les exigences de l'énoncé et les contrôles, et les apparier. Chaque exigence a
son contrôle ; chaque contrôle a son exigence ; et ce que le lab fabrique
lui-même est annoncé comme tel, pas comme un livrable.

### Un contrôle par exigence

Un contrôle qui porte neuf exigences a trois défauts, mesurés sur un cas réel :

- **le barème ment** : neuf exigences valaient un point sur deux, donc l'échec
  d'une seule coûtait la moitié du lab ;
- **l'arrêt au premier échec masque les huit autres** : l'apprenant ne sait pas
  laquelle des neuf a échoué ;
- et le diagnostic ne désigne rien.

Un contrôle par propriété prouvée. Chaque assertion porte son message, et le
message **nomme le geste attendu**, pas seulement le fait manquant.

### Jamais d'`assert` dans un bloc `finally`

Mesuré, pas déduit :

```python
def sujet():
    try:
        assert False, "LE VRAI ECHEC : le pair sans reseau n a pas ete refuse"
    finally:
        assert False, "le nettoyage a echoue"
# ce que l'apprenant lit : « le nettoyage a echoue »
```

**L'exception du `finally` remplace celle du `try`.** Un lab réel lisait « le
nettoyage a échoué » là où le vrai défaut était ailleurs : **il accusait le
mauvais geste.**

Un démontage qui échoue s'annonce par un avertissement, jamais par une
exception. Et le ménage du banc est contrôlé à sa vraie place : la
**photographie** que le cycle prend avant et après le lab refuse tout objet
laissé derrière. Le barème note l'apprenant, la photographie note le banc.

### Le contrôle doit interroger ce qu'il nomme

Cas vécu : un contrôle annonçait « identifiez l'image chargée dans le moteur
sans privilèges » et lançait son inspection **sans** l'option qui désigne ce
moteur. Il interrogeait donc l'autre, et passait au vert sans jamais regarder
celui qu'il nommait.

Ce défaut ne se voit pas en relisant le message : il se voit en corrigeant la
commande, parce que le contrôle échoue alors immédiatement.

### Une exigence doit avoir un effet observable

Refuser par **omission**, pas par liste noire. Un contrôle qui vérifie
l'absence d'un mot-clé se contourne ; un contrôle qui vérifie qu'une action
**échoue** mesure la politique réelle.

Et un lab n'exige que ce que la leçon enseigne : un geste non enseigné mesure
la débrouille.

---

## 5. Les verdicts ne se commitent jamais avec le code qu'ils mesurent

C'est la règle que `tests/test_verdicts_et_commun_separes.py` tient, et elle
est déjà en place dans ce dépôt. La séquence est **toujours** :

```
1. PR de code            (le lab change)
2. merge sur main
3. campagne sur main     (chaque lab seul)
4. PR de relevé          (le verdict seul, dans un commit séparé)
```

**Pourquoi.** Un verdict committé avec le code qu'il mesure n'est plus
datable : rien ne dit s'il a été relevé avant ou après le changement. Et un
squash des deux détruit ce qui les distinguait.

Le site qui publie ces labs tient pour **périmé** tout verdict dont un commit
ultérieur touche les fichiers du lab. Il a raison de ne pas faire d'exception,
pas même pour un commentaire : **rien dans un diff ne dit de lui-même qu'il est
sans effet**, et c'est précisément la campagne qui l'établit.

Avant de livrer un relevé, vérifier la correspondance **dans les deux sens** :
autant de labs sur le disque que d'entrées au relevé, et les deux ensembles
identiques.

### Un rouge n'est pas toujours une dette

Un lab peut sortir rouge sans aucun défaut, quand un registre amont republie un
tag que la préparation tire. Trois marques doivent être **réunies** pour
conclure :

1. le cycle est **parfait** (0 puis N puis 0) ;
2. l'écart porte **uniquement** sur la photographie, jamais sur un score ;
3. l'écart nomme un tag mobile, avec un digest neuf d'un côté et l'ancien de
   l'autre.

Et la conclusion vient de la **seconde mesure**, jamais du raisonnement que
« ça devrait passer ».

---

## 6. Les garde-fous sont des tests, pas de la bonne volonté

Tout ce qui précède est du jugement, et le jugement dérive. Ce qui tient, c'est
un test qui refuse.

Ce dépôt porte déjà :

| garde-fou | ce qu'il refuse |
|---|---|
| `tests/test_contrat_du_catalogue.py` | les écarts au contrat déclaratif |
| `tests/test_verdicts_et_commun_separes.py` | un verdict committé avec son code |
| `tests/test_provision_cluster.py` | les dérives du provisionnement |
| `scripts/valider-labs.py` | un lab qui ne rend pas 0 puis 100 puis 0 |
| `scripts/verdict_check.py` | un relevé incohérent |
| `scripts/gen_catalog.py --check` | un catalogue périmé dans les README |

Les contrôles communs du catalogue `containers` sont désormais portés et
câblés. Leur correspondance complète, les adaptations au contrat Proxmox et
les quatre modules Docker sans objet ici sont documentés dans
[CONTROLS.fr.md](CONTROLS.fr.md) et [CONTROLS.md](CONTROLS.md).

**Quand vous ajoutez un garde-fou, donnez-lui son propre garde-fou.** Un
contrôle qui parcourt des fichiers doit échouer s'il n'en trouve aucun : sinon
un motif cassé le rend silencieusement vert. Vécu : un motif qui avait perdu un
drapeau a annoncé « 91 labs sans URL de documentation », et un autre, trop
large, a fabriqué sept faux positifs qui portaient l'autorité d'un chiffre.

**Un contrôle rouge en permanence, qu'on fusionne par-dessus, ne contrôle plus
rien.** Si un garde-fou est rouge pour une raison qui n'est pas une dette, la
cause se nomme, se date et se motive, ou le contrôle se corrige. Jamais une
tolérance implicite.

### La dette mesurée le 2026-11-05 après portage

Les 47 labs sont comparés dans les deux sens au parcours déclaré. Les messages
bilingues passent désormais, après correction des neuf labs N3.

Les nouveaux garde-fous restent **bloquants** sur la dette réellement mesurée :
71 refus liés aux indices (41 labs sans les quatre coûts attendus, 15 sans liste
reconnue et les mêmes 15 sans textes bilingues utilisables), 41 solutions de
référence manquantes et 54 fichiers portant un tiret cadratin. Aucune liste
d'exemption n'a été ajoutée pour les faire passer. Les coûts des indices
restent ceux des six labs Proxmox complets : 5, 10, 15, 20.

Le détail des contrôles, les témoins de refus et les limites de la mesure sont
consignés dans [CONTROLS.fr.md](CONTROLS.fr.md). La suite des garde-fous donne
1 616 réussites, 166 échecs et 98 sauts. Ces résultats mesurent le dépôt ;
ils ne remplacent pas une campagne réelle sur Proxmox.

---

## 7. La discipline de session

- **Mesurer l'état réel avant d'agir**, jamais de mémoire. Compter les
  `lab.yaml` sur le disque, puis comparer à ce que l'outil déclare découvrir :
  l'écart, ce sont les fichiers qui lèvent en silence.
- **Lire un fichier avant de l'éditer.** Un bloc qu'on croit connaître a changé.
  Faire porter la substitution par une assertion qui échoue si le bloc visé est
  introuvable, plutôt que d'écrire à l'aveugle.
- **Une seule campagne de mesure à la fois** sur la machine. Deux campagnes
  concurrentes produisent des faux rouges silencieux.
- **Ne pas enchaîner deux dégradations** sans restaurer entre les deux : la
  seconde partirait de l'état sale laissé par la première, et son verdict ne
  mesurerait plus rien.
- **Restaurer ce qu'on a modifié pour mesurer**, y compris hors du dépôt : une
  ACL posée sur un socket, un service démarré à la main, un fichier déposé dans
  `/tmp` d'une machine.
- **Un point à chaque étape terminée** pendant un travail long, sans attendre
  qu'on le demande.
- **Un fait transmis se remesure.** Pour réfuter une affirmation, il faut un
  témoin capable de montrer l'effet. Vécu : une affirmation juste a été réfutée
  avec un témoin aveugle, et le faux est parti dans le corps d'une PR.
- **Ne pas se corriger à l'excès.** Corriger ce qui change une décision, puis
  continuer.

---

## 8. Avant de livrer

- [ ] Branche créée depuis un `main` à jour **avant** la première modification.
- [ ] `dsoxlab validate-structure` vert.
- [ ] `scripts/gen_catalog.py --check` : catalogue à jour (les README racine
      sont **générés**, pas édités à la main).
- [ ] Les garde-fous de `tests/` verts, et **un garde-fou nouveau** par
      comportement ajouté ou corrigé.
- [ ] `ruff` propre.
- [ ] Cycle complet joué sur chaque lab touché : **0 puis N puis 0**, et
      l'environnement rendu intact.
- [ ] **La triche jouée** sur chaque contrôle ajouté ou corrigé, avec la
      dégradation vérifiée avant le verdict.
- [ ] **`check` joué deux fois** : même verdict.
- [ ] `grep -c '—' <fichiers touchés>` rend 0, et les accents sont complets.
- [ ] Énoncés et contrôles appariés dans les deux sens, EN et FR.
- [ ] Le message de commit est dans un **fichier**, et il dit ce qui a été
      **mesuré**, avec ses valeurs.
- [ ] Le relevé d'attestation est livré **séparément**, après merge et campagne
      sur `main`.
- [ ] La PR est ouverte par l'utilisateur, pas par l'agent.
