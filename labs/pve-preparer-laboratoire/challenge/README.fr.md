# Ce qui est attendu

Préparer un environnement jetable, produire son inventaire et démontrer qu’il peut exécuter une VM accélérée.

# Ce qui est prouvé

- **Le plan correspond aux ressources réellement allouées.** — Comparer l’inventaire fourni, les capacités du niveau externe et les valeurs lues dans le nœud ; refuser un disque non autorisé.
- **Une VM de contrôle utilise effectivement KVM.** — Démarrer l’invité témoin puis examiner l’accélérateur ; une émulation TCG ne valide pas ce profil.
- **Une console indépendante reste utilisable.** — Interrompre seulement le chemin de management du lab et vérifier l’accès par la console extérieure.
- **Un environnement incompatible est identifié avant installation.** — Rejouer le prévol avec /dev/kvm indisponible ; attendre un blocage expliqué et aucune opération destructive.

Les critères nécessitant une observation humaine doivent être revus séparément avant attestation.
