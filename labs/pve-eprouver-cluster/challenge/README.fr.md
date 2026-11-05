# Consigne et allocation du formateur

Sur le **poste indépendant**, depuis le répertoire du lab, créer
`challenge/work/config.json` (ne jamais committer de secrets) :

```json
{
  "hosts": ["pve01.lab", "pve02.lab", "pve03.lab"],
  "guest_ids": [],
  "sources": {},
  "console_verified": true,
  "nested_only": true,
  "allow_failure": "pve-eprouver-cluster"
}
```

Le formateur vérifie réellement ces garanties avant de renseigner les indicateurs.
Le profil indépendant à la demande `proxmox-cluster` attribue 8 Gio/4 vCPU par
nœud, disques système et supplémentaire de 40 Gio chacun. Ne provisionner que
sur demande explicite ; former le cluster manuellement, jamais en effet
automatique du setup ou corrigé. Toute panne refuse la présence d’un invité
hors allocation, même arrêté : un redémarrage de nœud pourrait le démarrer.
L’inventaire SSH provisionné de dsoxlab est utilisé. Sinon `N3_SSH_CONFIG` désigne
un inventaire OpenSSH existant avec ces alias exacts. Clés d’hôtes connues et
sudo non interactif sont requis. Le contrôleur vérifie qu’aucune cible ne se
résout sur une de ses adresses locales. Ne pas provisionner de nœuds pendant le
lab et ne pas désactiver les vérifications d’identité SSH/TLS.

Lancer le setup avant de former le cluster. Une fois sain :

```bash
python3 tools/controller.py snapshot --phase qualified
python3 tools/controller.py fail --action one-node --hosts pve03.lab --duration 120
python3 tools/controller.py fail --action no-majority --hosts pve02.lab pve03.lab --duration 120
python3 tools/controller.py check --criterion coherence
python3 tools/controller.py restore
```

Le contrôleur arrête **Corosync seulement** sur les nœuds exacts attribués,
arme un retour borné avant chaque arrêt, relève votes et refus pmxcfs réels,
puis restaure dans `finally`. C’est une partition d’appartenance, pas une
preuve de perte physique d’alimentation. Le watchdog HA peut redémarrer un nœud
nested jetable : interdire tout hôte de production. Fenêtre de 10 à 120 secondes.
`restore` est l’arrêt d’urgence. Si SSH ne revient pas, démarrer Corosync depuis
la console indépendante sur les seuls hôtes concernés. Preuves et verrou sont
conservés lors d’un retour incomplet ; ne jamais les effacer pour cacher l’échec.
Une seule action/maintenance du contrôleur peut être active à la fois.

Contrôle indépendant facultatif d’alimentation virtuelle :
`failure_mode="power"`,
`domains={"pve01.lab":"<UUID>","pve02.lab":"<UUID>","pve03.lab":"<UUID>"}`.
Chaque UUID exact est vérifié via les adresses guest-agent du `qemu:///system`
local contre l’IP SSH attribuée au setup. Aucun nom deviné ni URI extérieur.
Le contrôleur arme son retour **local** avant `virsh destroy`, observe le vrai
état éteint et ne démarre que cet UUID au retour. Libvirt/identité guest-agent
absents : erreur de précondition. Mesure virtuelle, jamais panne serveur physique.

Rédiger `challenge/work/report.md` : allocation, topologie, observations
avant/pendant/après, chaque critère de `contract.json`, diagnostics de refus et
tâches, domaines de panne, limites et procédure précise de retour/nettoyage.
La revue humaine vérifie isolation réseau et absence de contournement votes/verrous.
Les tests comparent membres, votes, versions, empreintes de configuration et
reçus de panne réels, pas des affirmations. Preuves : `challenge/work/evidence`.
Les archiver avant nettoyage. Celui-ci préserve toutes les ressources du
formateur et le fichier d’allocation ; il restaure et retire uniquement ses preuves.

## Indices progressifs

1. Observer chaque survivant, pas seulement une interface qui répond.
2. Comparer votes attendus, membres présents et écriture pmxcfs.
3. Un nœud accessible sans majorité ne peut pas autoriser des écritures cluster.
   Le retour doit converger vers une configuration unique, pas trois pings.
