# Challenge : rétablir l'agent invité, sans arrêt forcé

Vous travaillez sur `pve.lab`. Le manifeste est dans
`/opt/lab-proxmox/pve-reparer-agent/manifeste.md`.

## Ce qui est attendu

1. Le périphérique de l'agent est activé, `qm agent 180 ping` répond, et le
   canal `/dev/virtio-ports/org.qemu.guest_agent.0` existe dans l'invité.
2. `qm agent 180 network-get-interfaces` remonte `10.10.113.180`.
3. La VM n'a jamais été arrêtée de force depuis le début du lab, et la page
   témoin répond toujours avec les données de la session.

## Ce qui est prouvé

Les tests interrogent l'agent depuis le nœud, lisent le journal des tâches de
Proxmox à la recherche d'un `qmstop`, et lisent la page témoin depuis le nœud.
