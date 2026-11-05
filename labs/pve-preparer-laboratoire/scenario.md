# Préparer un laboratoire et son plan de ressources

## Mission

Préparer un environnement jetable, produire son inventaire et démontrer qu’il peut exécuter une VM accélérée.

## Starting state

- Poste contrôleur fourni
- Hôte de lab dédié ou VM externe autorisée
- Disques identifiés et environnement de production explicitement exclu

## Constraints

- N’agir que sur les identifiants, réseaux et disques explicitement attribués au lab ; préserver la console de secours.
- Une configuration différente du corrigé est acceptée si elle respecte les contraintes et produit toutes les preuves.
- Conserver les observations utiles avant correction ; masquer les secrets sans masquer l’identité des ressources contrôlées.

## Acceptance criteria

- **Le plan correspond aux ressources réellement allouées.** — Comparer l’inventaire fourni, les capacités du niveau externe et les valeurs lues dans le nœud ; refuser un disque non autorisé.
- **Une VM de contrôle utilise effectivement KVM.** — Démarrer l’invité témoin puis examiner l’accélérateur ; une émulation TCG ne valide pas ce profil.
- **Une console indépendante reste utilisable.** — Interrompre seulement le chemin de management du lab et vérifier l’accès par la console extérieure.
- **Un environnement incompatible est identifié avant installation.** — Rejouer le prévol avec /dev/kvm indisponible ; attendre un blocage expliqué et aucune opération destructive.

Automated checks prove only observable system state. Human-observed steps (for example ISO provenance, console access, or imposed outages) require their own recorded review before attestation.
