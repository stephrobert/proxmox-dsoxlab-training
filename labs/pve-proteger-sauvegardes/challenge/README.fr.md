# Défi : Chiffrer, conserver et vérifier les sauvegardes

Utilisez uniquement PBS et le coffre de clés hors ligne fournis. Configurez le job de sauvegarde attribué avec chiffrement, rétention finie et vérification périodique. Restaurez une sauvegarde de test avec la clé récupérée, puis contrôlez le marqueur de données attendu. Lancez la vérification sur la fixture corrompue jetable fournie et confirmez qu’une tâche ou un enregistrement PBS/PVE rapporte l’échec. Ne déposez jamais la clé ni son contenu sur le nœud PVE.

La ressource attribuée est `PBS storage lab-pbs-n2-208; supplied VM/backups, limited identity, and offline key vault.`. Réalisez l’état Proxmox natif décrit dans `scenario.fr.md` ; ne soumettez ni historique de commandes ni preuve déclarative. Exécutez les tests fonctionnels uniquement sur la cible PVE attribuée et lorsque tous les prérequis externes sont présents. Les tests ne modifient rien.

## Retour

- Un test réussi signifie uniquement que l’état Proxmox interrogé correspond à son assertion.
- Une fixture PBS/CT/ZFS/thin-pool absente est un prérequis manquant, jamais une réussite.
- Gardez les secrets hors des preuves et des sorties de test.
