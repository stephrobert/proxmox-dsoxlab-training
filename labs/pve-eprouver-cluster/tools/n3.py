"""Controller-side, bounded evidence collection for the nine N3 cluster labs.

Nothing provisions a host or silently weakens SSH/TLS. Saved observations are
raw command results, not learner-supplied success flags. Review still covers
physical failure domains, fencing interpretation and operational decisions.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import re
import shlex
import socket
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

HOSTS = ("pve01.lab", "pve02.lab", "pve03.lab")
PHASES = {
    "baseline", "qualified", "preflight-rejected", "migrated", "rebooted",
    "load", "candidate-rejected", "replicated", "replication-failed",
    "source-unavailable", "recovered", "majority", "no-quorum",
    "storage-unavailable", "maintenance", "reintegrated", "restored", "failover",
}
ALLOWED_ACTIONS = {
    "pve-eprouver-cluster": {"one-node", "no-majority"},
    "pve-qualifier-stockage-partage": {"storage"},
    "pve-migrer-instance": set(),
    "pve-reserver-capacite": set(),
    "pve-mesurer-replication": {"one-node", "replication-link"},
    "pve-eprouver-ha": {"one-node", "no-majority"},
    "pve-maintenir-cluster": {"one-node"},
    "pve-reprendre-hors-site": {"primary-site"},
    "pve-epreuve-disponibilite": {"one-node", "no-majority", "replication-link", "primary-site"},
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "Redirect refused", headers, fp)

PROCESS_SCRIPT = """
import glob,json,os,re
out=[]
for p in glob.glob('/proc/[0-9]*/cmdline'):
 try:
  a=open(p,'rb').read().decode().split('\\0')
  if '-id' in a and any('qemu' in x or 'kvm' in x for x in a[:1]):
   disks=[]
   for argument in a:
    for filename in re.findall(r'(?:file=|\"filename\":\")(/[^,\" ]+)',argument):
     disks.append(os.path.realpath(filename))
   out.append({'vmid':int(a[a.index('-id')+1]),'pid':int(p.split('/')[2]),'disks':disks})
 except (OSError,ValueError,IndexError): pass
print(json.dumps(out))
"""


class PreconditionError(RuntimeError):
    pass


def require(condition, text):
    if not condition:
        raise PreconditionError(text)


def command(argv, timeout=30):
    result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
    return {"rc": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def parsed(result):
    require(result["rc"] == 0, f"Command failed: {result['stderr'] or result['stdout']}")
    return json.loads(result["stdout"])


def redact(value):
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, dict):
        sensitive = {"password", "cipassword", "token", "secret", "ticket",
                     "encryption-key", "private-key", "keyfile"}
        return {key: "<redacted>" if key.lower() in sensitive else redact(item)
                for key, item in value.items()}
    return value


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def quorum(node):
    text = node["votes"]["stdout"]
    return bool(re.search(r"Quorate:\s+Yes\b", text))


def votes_unmodified(node):
    return bool(re.search(r"Expected votes:\s+3\b", node["votes"]["stdout"]))


def members(node):
    return {
        x["name"] for x in parsed(node["members"])
        if x.get("type") == "node" and x.get("online") == 1
    }


def resources(snapshot):
    return parsed(next(iter(snapshot["nodes"].values()))["resources"])


def guests(snapshot, ids):
    return {int(x["vmid"]): x for x in resources(snapshot) if x.get("vmid") in ids}


def owners(snapshot, vmid):
    for host in HOSTS:
        if host not in snapshot["nodes"]:
            state = snapshot.get("power", {}).get(host, {})
            require(state.get("rc") == 0 and state.get("stdout", "").strip() == "shut off",
                    f"{host}: missing process observer and no independent power-off proof.")
    for node in snapshot["nodes"].values():
        for process in parsed(node["processes"]):
            require(process["vmid"] == vmid or not any(
                f"vm-{vmid}-disk-" in path for path in process.get("disks", [])
            ), "Another QEMU identity is using the allocated guest's disk.")
    return [
        name for name, node in snapshot["nodes"].items()
        if any(x["vmid"] == vmid for x in parsed(node["processes"]))
    ]


def healthy(snapshot):
    nodes = snapshot["nodes"]
    require(set(nodes) == set(HOSTS), "All three nodes must be observable.")
    configs = {digest(n["corosync"]["stdout"]) for n in nodes.values()}
    versions = {n["version"]["stdout"].split("/")[1].split(".")[0] for n in nodes.values()}
    require(len(configs) == len(versions) == 1, "Distributed configuration/version mismatch.")
    node_names = {n["name"]["stdout"].strip() for n in nodes.values()}
    for node in nodes.values():
        require(quorum(node) and votes_unmodified(node), "Quorum/votes not nominal (3 expected).")
        require(members(node) == node_names, "Membership differs between observers.")


def successful_samples(snapshot):
    return [p for p in snapshot["samples"] if p.get("status") == 200]


def business(snapshot):
    samples = successful_samples(snapshot)
    require(samples, "No successful external business observation.")
    for sample in samples:
        body = sample["body"]
        require(isinstance(body.get("sequence"), int) and body["sequence"] >= 0,
                "Witness must expose the durable sequence number.")
        require(isinstance(body.get("marker"), str) and bool(body["marker"]),
                "Witness must expose the durable marker, not just HTTP health.")
    return samples[-1]["body"]


def same_data(before, after):
    a, b = business(before), business(after)
    require(a["marker"] == b["marker"], "Durable marker changed.")
    require(b["sequence"] >= a["sequence"], "Acknowledged data was lost.")


class Controller:
    def __init__(self, lab):
        self.lab = Path(lab).resolve()
        self.repo = self.lab.parents[1]
        self.contract = json.loads((self.lab / "contract.json").read_text())
        self.id = self.contract["id"]
        self.work = self.lab / "challenge/work"
        self.evidence = self.work / "evidence"
        config = self.work / "config.json"
        require(config.is_file(), f"Missing instructor allocation: {config}; see challenge README.")
        self.cfg = json.loads(config.read_text())
        require(self.cfg.get("hosts") == list(HOSTS), "Only the three catalog cluster hosts are allowed.")
        require(os.environ.get("DSOXLAB_TARGET", "proxmox-cluster") == "proxmox-cluster",
                "This lab requires runtime target proxmox-cluster; no single-node override.")
        self.ids = self.contract["guest_ids"]
        require(self.cfg.get("guest_ids") == self.ids, "Guest IDs differ from this lab's allocation.")
        metadata = yaml.safe_load((self.repo / "meta.yml").read_text())
        profile = metadata.get("environments", {}).get("proxmox-cluster", {})
        if not profile:
            profile = metadata["infra"].get("environments", {}).get("proxmox-cluster", {})
        infra = profile.get("infra", profile) if profile else metadata["infra"]
        self.catalog = {h["name"] for h in infra.get("hosts", [])}
        self.network = infra.get("cidr", metadata["infra"].get("cidr"))
        require(set(HOSTS) <= self.catalog, "The catalog does not declare all three cluster nodes.")
        self.sources = self.cfg.get("sources", {})
        for role in self.contract["required_sources"]:
            host = self.sources.get(role)
            require(host in self.catalog and host not in HOSTS,
                    f"Missing independent catalog host for {role}; do not reuse a cluster node "
                    "or invent a source role. This catalog cannot run this scenario yet.")
        require(set(self.sources) == set(self.contract["required_sources"]),
                "Unexpected source role; actions must stay within the mission allocation.")
        require(len(set(self.sources.values())) == len(self.sources),
                "Independent source/recovery roles must not share a host.")
        self.allowed = set(HOSTS) | set(self.sources.values())
        require(self.cfg.get("failure_mode", "partition") in {"partition", "power"},
                "Unsupported failure mode.")
        self.domains = self.cfg.get("domains", {})
        require(set(self.domains) <= set(HOSTS)
                and all(re.fullmatch(r"[0-9a-f-]{36}", value) for value in self.domains.values()),
                "Power control accepts only UUIDs explicitly mapped to allocated cluster hosts.")
        ssh_config = os.environ.get("N3_SSH_CONFIG")
        if not ssh_config:
            from dsoxlab.discovery.repo import read_repo_metadata
            from dsoxlab.infra.inventory import (
                build_inventory,
                read_terraform_outputs,
                write_ssh_config,
            )
            meta = read_repo_metadata(self.repo)
            inventory = build_inventory(meta, terraform_outputs=read_terraform_outputs(meta))
            ssh_config = str(write_ssh_config(inventory, meta))
        self.ssh_config = str(Path(ssh_config).resolve())
        require(Path(self.ssh_config).is_file(), "No provisioned SSH inventory/configuration.")
        self.guard_controller()
        self.evidence.mkdir(parents=True, exist_ok=True, mode=0o700)

    def guard_controller(self):
        require(socket.gethostname().split(".")[0] not in {"pve01", "pve02", "pve03"},
                "Controller must execute outside the cluster.")
        local = parsed(command(["ip", "-j", "address", "show"]))
        local_ips = {a["local"] for i in local for a in i.get("addr_info", [])}
        self.addresses = {}
        for host in sorted(self.allowed):
            conf = command(["ssh", "-F", self.ssh_config, "-G", host])
            require(conf["rc"] == 0, "Cannot resolve SSH target.")
            hostname = next(
                line.split(maxsplit=1)[1] for line in conf["stdout"].splitlines()
                if line.startswith("hostname ")
            )
            addresses = {a[4][0] for a in socket.getaddrinfo(hostname, None)}
            require(not addresses & local_ips, f"Controller is hosted on target {host}.")
            require(len(addresses) == 1, f"Ambiguous address for {host}.")
            self.addresses[host] = addresses.pop()

    def ssh(self, host, script, timeout=30):
        require(host in self.allowed, "Host outside the exact catalog allocation.")
        return command([
            "ssh", "-F", self.ssh_config, "-o", "StrictHostKeyChecking=yes",
            "-o", "BatchMode=yes", "-o", "ConnectTimeout=5",
            "-o", "ConnectionAttempts=1", host,
            "sudo -n timeout 25 bash -c " + shlex.quote(script),
        ], timeout)

    def read(self, host, path):
        require(re.fullmatch(r"/[a-zA-Z0-9/:_.@-]+", path), "Invalid API path.")
        result = self.ssh(host, f"pvesh get {shlex.quote(path)} --output-format json")
        if result["rc"] == 0:
            result["stdout"] = json.dumps(redact(json.loads(result["stdout"])))
        return result

    def sample(self, transaction=False, recovery=False, ct=False):
        key = "ct_service_url" if ct else ("recovery_url" if recovery else "service_url")
        url = self.cfg.get(key)
        if not url:
            return {"at": time.time(), "error": f"Missing {key}"}
        u = urllib.parse.urlsplit(url)
        require(u.scheme == "https" and not u.username and not u.password,
                "Witness requires normal verified HTTPS; credentials must not be in URLs.")
        require(u.path == f"/api/lab/{self.id}" and not u.query and not u.fragment,
                "Witness URL must be the dedicated lab API path.")
        network = ipaddress.ip_network(self.cfg["guest_network"], strict=True)
        require(self.network and network.subnet_of(ipaddress.ip_network(self.network)),
                "Guest service must remain in the catalog lab network.")
        ips = {ipaddress.ip_address(a[4][0]) for a in socket.getaddrinfo(u.hostname, u.port or 443)}
        require(ips and all(ip in network for ip in ips), "Witness resolved outside allocated network.")
        require(not {str(ip) for ip in ips} & set(self.addresses.values()),
                "Use the guest business service, not a PVE/PBS management API.")
        payload = json.dumps({"operation": "append", "marker": self.cfg["marker"]}).encode()
        req = urllib.request.Request(
            url, data=payload if transaction else None,
            headers={"Content-Type": "application/json"},
        )
        sample = {"at": time.time(), "transaction": transaction, "url": url}
        try:
            with urllib.request.build_opener(NoRedirect()).open(req, timeout=3) as response:
                require(response.geturl() == url, "Witness redirects are outside the allocation.")
                sample.update(status=response.status, body=json.loads(response.read(65536)))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            sample["error"] = str(exc)
        return sample

    def snapshot(self, phase, samples=None, persist=True):
        require(phase in PHASES, "Unknown observation phase.")
        state = {
            "lab": self.id, "at": time.time(), "controller": socket.gethostname(),
            "phase": phase, "nodes": {}, "sources": {},
            "samples": samples if samples is not None else [self.sample()],
        }
        def collect(host):
            name = self.ssh(host, "hostname -s")
            if name["rc"]:
                return host, None, name
            node = name["stdout"].strip()
            require(re.fullmatch(r"[A-Za-z0-9-]+", node), "Invalid Proxmox node identity.")
            item = {
                "name": name, "version": self.ssh(host, "pveversion"),
                "votes": self.ssh(host, "pvecm status"),
                "corosync": self.ssh(host, "cat /etc/pve/corosync.conf"),
                "members": self.read(host, "/cluster/status"),
                "resources": self.read(host, "/cluster/resources"),
                "storage_config": self.read(host, "/storage"),
                "storage": self.read(host, f"/nodes/{node}/storage"),
                "network": self.ssh(host, "ip -j link show"),
                "ha": self.read(host, "/cluster/ha/status/current"),
                "ha_resources": self.read(host, "/cluster/ha/resources"),
                "ha_rules": self.read(host, "/cluster/ha/rules"),
                "replication": self.read(host, f"/nodes/{node}/replication"),
                "processes": self.ssh(host, "python3 -c " + shlex.quote(PROCESS_SCRIPT)),
                "tasks": self.read(host, f"/nodes/{node}/tasks"),
                "journal": self.ssh(host, "journalctl -b -u pve-ha-lrm -u pve-ha-crm "
                                    "-u watchdog-mux -u corosync --since '-30 minutes' "
                                    "--no-pager -o short-unix"),
                "guests": {},
            }
            for vmid in self.ids:
                kind = "lxc" if vmid == self.contract.get("ct_id") else "qemu"
                item["guests"][str(vmid)] = {
                    "status": self.read(host, f"/nodes/{node}/{kind}/{vmid}/status/current"),
                    "config": self.read(host, f"/nodes/{node}/{kind}/{vmid}/config"),
                }
            sid = self.contract["storage_id"]
            mount = f"/mnt/pve/{sid}"
            item["mount"] = self.ssh(host, "findmnt -J -T " + shlex.quote(mount))
            item["nonce"] = self.ssh(
                host, "sha256sum " + shlex.quote(f"{mount}/.n3-{self.id}-nonce")
            )
            item["zfs"] = self.ssh(host, "zfs list -Hp -t filesystem,volume,snapshot "
                                 "-o name,guid,creation,used,available")
            if self.contract.get("ct_id"):
                item["ct_process"] = self.ssh(
                    host, f"lxc-info -n {self.contract['ct_id']} -sH -pH"
                )
            return host, item, None

        with ThreadPoolExecutor(max_workers=3) as pool:
            for host, item, error in pool.map(collect, HOSTS):
                if error:
                    state.setdefault("unreachable", {})[host] = error
                else:
                    state["nodes"][host] = item
        if self.domains:
            state["power"] = {
                host: command(["virsh", "-c", "qemu:///system", "domstate", uuid])
                for host, uuid in self.domains.items()
            }
        if self.contract.get("ct_id"):
            state["ct_samples"] = [self.sample(ct=True)]
        for role, host in self.sources.items():
            source = {"host": host}
            if role.startswith("pbs"):
                source["sync"] = self.ssh(host, "proxmox-backup-manager sync-job list "
                                         "--output-format json")
                source["tasks"] = self.ssh(host, "proxmox-backup-manager task list "
                                          "--output-format json")
            elif role == "nfs":
                source["exports"] = self.ssh(host, "exportfs -v")
                source["service"] = self.ssh(host, "systemctl is-active nfs-server")
            elif role == "recovery":
                source["resources"] = self.read(host, "/cluster/resources")
                source["processes"] = self.ssh(host, "python3 -c " + shlex.quote(PROCESS_SCRIPT))
                source["tasks"] = self.ssh(host, "pvesh get /nodes/$(hostname -s)/tasks "
                                          "--output-format json")
                source["connections"] = self.ssh(host, "ss -ntp")
                source["firewall"] = self.ssh(host, "nft list table inet n3_recovery")
                source["files"] = self.ssh(host, "proxmox-backup-client snapshot files "
                                         + shlex.quote(self.cfg["backup_snapshot"])
                                         + " --output-format json")
                source["snapshots"] = self.ssh(host, "proxmox-backup-client snapshot list "
                                              "--output-format json")
                source["guest_config"] = self.ssh(host, f"qm config {self.ids[0]}")
                source["storage_config"] = self.read(host, "/storage")
            elif role == "vault":
                source["key"] = self.ssh(host, "test -s /var/lib/lab-proxmox/"
                                        + self.id + "/recovery-key.json")
            state["sources"][role] = source
        if "recovery" in self.sources:
            state["recovery_samples"] = [self.sample(recovery=True)]
        if persist:
            self.save(f"{phase}.json", state)
        return state

    def save(self, name, data):
        require(re.fullmatch(r"[a-z-]+\.json", name), "Invalid evidence name.")
        file = self.evidence / name
        file.write_text(json.dumps(data, indent=2) + "\n")
        file.chmod(0o600)

    def load(self, phase):
        path = self.evidence / f"{phase}.json"
        require(path.is_file(), f"Missing measured phase {phase}; run the controller observation.")
        data = json.loads(path.read_text())
        require(data["lab"] == self.id, "Evidence belongs to another lab.")
        return data

    def prepare(self):
        require(not (self.evidence / "baseline.json").exists(),
                "Evidence already exists; clean/reset explicitly, never overwrite a baseline.")
        require(self.cfg.get("console_verified") is True and self.cfg.get("nested_only") is True,
                "Instructor must confirm independent rescue console and disposable nested scope.")
        state = self.snapshot("baseline", persist=False)
        require(set(state["nodes"]) == set(HOSTS), "Three reachable preinstalled PVE nodes required.")
        for node in state["nodes"].values():
            parsed(node["processes"])
            require(node["version"]["rc"] == 0, "PVE not installed; setup never installs/provisions it.")
        if self.id != "pve-eprouver-cluster":
            healthy(state)
            actual = guests(state, self.ids)
            require(set(actual) == set(self.ids), "Assigned instructor guests/services are missing.")
            for vmid, guest in actual.items():
                require(guest["name"] == f"n3-{self.id}-{vmid}",
                        "An allocated ID belongs to another exercise; do not reuse or destroy it.")
                if vmid != self.contract.get("ct_id"):
                    require(len(owners(state, vmid)) == (1 if guest["status"] == "running" else 0),
                            "Baseline guest process ownership differs from actual guest status.")
            for host, node in state["nodes"].items():
                require(node["name"]["stdout"].strip() == host.split(".")[0],
                        "PVE node identity differs from its allocated host alias.")
                stores = parsed(node["storage"])
                store = next((s for s in stores if s["storage"] == self.contract["storage_id"]), None)
                require(store and store.get("active") == 1, "Dedicated prepared storage is missing/inactive.")
            if self.id == "pve-mesurer-replication":
                for node in state["nodes"].values():
                    config = parsed(node["storage_config"])
                    require(any(s["storage"] == self.contract["storage_id"] and s["type"] == "zfspool"
                                for s in config) and node["zfs"]["rc"] == 0,
                            "Qualified real ZFS storage is required before replication.")
            business(state)
            require(business(state)["marker"] == self.cfg["marker"], "Instructor marker mismatch.")
            if self.contract.get("ct_id"):
                business({**state, "samples": state["ct_samples"]})
        if self.sources:
            for role, source in state["sources"].items():
                require(role != "recovery" or not any(
                    x.get("vmid") for x in parsed(source["resources"])
                ),
                        "Recovery host must initially be empty.")
        if self.cfg.get("failure_mode") == "power":
            require(set(self.domains) == set(HOSTS), "Power experiments require all three exact UUID mappings.")
            for host, uuid in self.domains.items():
                identity = command(["virsh", "-c", "qemu:///system", "domifaddr",
                                    uuid, "--source", "agent"])
                require(identity["rc"] == 0 and re.search(
                    rf"\b{re.escape(self.addresses[host])}/\d+\b", identity["stdout"]),
                    f"{host}: hypervisor UUID does not prove this allocated node address.")
        self.save("baseline.json", state)
        self.save("allocation.json", {
            "lab": self.id, "at": time.time(), "hosts": self.cfg["hosts"],
            "guest_ids": self.ids, "storage_id": self.contract["storage_id"],
            "sources": self.sources, "baseline_sha256": digest(json.dumps(state, sort_keys=True)),
            "domains": self.domains,
        })

    def fail(self, action, duration, hosts, experiment=None):
        require(10 <= duration <= 120, "Failure window must be 10..120 seconds.")
        require(self.cfg.get("allow_failure") == self.id,
                "Set allow_failure to this exact lab ID only after reviewing the rescue plan.")
        require(self.cfg.get("console_verified") is True and self.cfg.get("nested_only") is True,
                "No failure without independent console and disposable nested scope.")
        require(action in ALLOWED_ACTIONS[self.id], "Failure action is outside this mission.")
        if action in {"one-node", "no-majority"}:
            require(len(hosts) == (1 if action == "one-node" else 2)
                    and len(set(hosts)) == len(hosts) and set(hosts) <= set(HOSTS),
                    "Partition exactly one/two allocated nodes, never an arbitrary host.")
        elif action == "replication-link":
            require(len(hosts) == 1 and hosts[0] in HOSTS and self.cfg["destination"] in HOSTS
                    and hosts[0] != self.cfg["destination"], "Invalid replication endpoints.")
        elif action == "storage":
            require(hosts == [self.sources.get("nfs")], "Only the independent allocated NFS server.")
        else:
            require(hosts == [self.sources.get("recovery")], "Only the empty allocated recovery host.")
        require(not (self.evidence / "active.json").exists(),
                "Another experiment/maintenance is active; restore it first.")
        qualified = self.snapshot("qualified")
        healthy(qualified)
        require(not any(x.get("vmid") not in self.ids
                        for x in resources(qualified) if x.get("vmid")),
                "An unrelated guest exists; cluster failure would affect unallocated resources.")
        event = {"lab": self.id, "action": action, "hosts": hosts,
                 "at": time.time(), "duration": duration, "restored": False, "commands": []}
        with (self.evidence / "active.json").open("x") as lock:
            json.dump(event, lock)
        (self.evidence / "active.json").chmod(0o600)
        deadline = time.monotonic() + duration - 5
        try:
            for host in hosts:
                if action in {"one-node", "no-majority"} and self.cfg.get("failure_mode") == "power":
                    uuid = self.domains.get(host)
                    require(uuid and self.load("allocation").get("domains", {}).get(host) == uuid,
                            "Power mapping differs from the verified baseline allocation.")
                    unit = f"n3-{self.id}-{action}-{host.split('.')[0]}-{int(event['at'])}"
                    arm = command(["sudo", "-n", "systemd-run", f"--unit={unit}",
                                   f"--on-active={duration}s", "virsh", "-c",
                                   "qemu:///system", "start", uuid])
                    require(arm["rc"] == 0, "Independent hypervisor recovery timer could not be armed.")
                    entry = {"host": host, "unit": unit, "power": uuid, "arm": arm}
                    event["commands"].append(entry)
                    self.save("active.json", event)
                    entry["change"] = command(["virsh", "-c", "qemu:///system", "destroy", uuid])
                    require(entry["change"]["rc"] == 0, "Exact allocated domain power removal failed.")
                    self.save("active.json", event)
                    continue
                if action in {"one-node", "no-majority"}:
                    undo, change = "systemctl start corosync", "systemctl stop corosync"
                elif action == "storage":
                    undo, change = "systemctl start nfs-server", "systemctl stop nfs-server"
                else:
                    table = "n3_recovery" if action == "primary-site" else "n3_replication"
                    require(self.ssh(host, f"nft list table inet {table}")["rc"] != 0,
                            "Existing firewall table is not owned by this experiment.")
                    undo = f"nft delete table inet {table}"
                    peers = list(HOSTS) if action == "primary-site" else [self.cfg["destination"]]
                    if action == "primary-site" and "pbs_primary" in self.sources:
                        peers.append(self.sources["pbs_primary"])
                    addresses = [self.addresses[p] for p in peers]
                    require(all(ipaddress.ip_address(ip).version == 4 for ip in addresses),
                            "This bounded firewall scenario requires catalog IPv4 endpoints.")
                    rules = "; ".join(
                        f"add rule inet {table} output ip daddr {ip} "
                        + ("counter reject" if action == "primary-site" else "tcp dport 22 counter reject")
                        for ip in addresses
                    )
                    change = "nft -f - <<'N3_RULES'\n" + (
                        f"add table inet {table}\n"
                        f"add chain inet {table} output {{ type filter hook output priority 0; policy accept; }}\n"
                        + rules.replace("; ", "\n") + "\nN3_RULES"
                    )
                unit = f"n3-{self.id}-{action}-{int(event['at'])}"
                arm = self.ssh(host, f"systemd-run --unit={unit} --on-active={duration}s "
                               "/bin/sh -c " + shlex.quote(undo))
                require(arm["rc"] == 0, "Recovery timer could not be armed; refusing failure.")
                entry = {"host": host, "unit": unit, "undo": undo, "arm": arm}
                event["commands"].append(entry)
                self.save("active.json", event)
                entry["change"] = self.ssh(host, change)
                self.save("active.json", event)
                require(entry["change"]["rc"] == 0, "Failure action failed.")
            if action == "no-majority":
                survivor = next(h for h in HOSTS if h not in hosts)
                path = f"/etc/pve/n3-{self.id}-quorum-probe"
                event["write_probe"] = self.ssh(
                    survivor, "printf 'bounded quorum probe\\n' > " + shlex.quote(path)
                )
                require(event["write_probe"]["rc"] not in {0, 255} and re.search(
                    r"Permission denied|Read-only file system|Operation not permitted",
                    event["write_probe"]["stderr"], re.I),
                    "Missing actual pmxcfs write refusal; connection failure is not a quorum result.")
            samples = [self.sample()]
            if experiment is not None:
                experiment(event)
            require(time.monotonic() < deadline, "Experiment exceeded the armed failure window.")
            phase = {
                "one-node": "majority", "no-majority": "no-quorum",
                "replication-link": "replication-failed", "storage": "storage-unavailable",
                "primary-site": "restored",
            }[action]
            # Capture votes during the fault, not after the automatic recovery timer.
            state = self.snapshot(phase, [])
            while time.monotonic() < deadline:
                samples.append(self.sample())
                time.sleep(1)
            newer = self.load(phase)
            if state["at"] < newer["at"] < event["at"] + duration:
                state = newer
            state["samples"] = samples
            self.save(f"{phase}.json", state)
            event["observed_at"] = state["at"]
        finally:
            self.restore(event)
        self.save(f"{action}.json", event)

    def restore(self, event=None):
        path = self.evidence / "active.json"
        if event is None:
            if not path.exists():
                return
            event = json.loads(path.read_text())
        failures = []
        require(event["action"] in ALLOWED_ACTIONS[self.id] and event["lab"] == self.id,
                "Recovery receipt is not an allocated action for this lab.")
        require(all(re.fullmatch(rf"n3-{re.escape(self.id)}-[a-z0-9-]+-\d+", e["unit"])
                    for e in event["commands"]), "Invalid owned recovery timer identity.")
        for entry in event["commands"]:
            require(entry["host"] in event["hosts"], "Recovery receipt contains an unallocated host.")
            if "power" in entry:
                require(entry["host"] in HOSTS and self.domains.get(entry["host"]) == entry["power"],
                        "Recovery domain differs from exact allocated host.")
                current = command(["virsh", "-c", "qemu:///system", "domstate", entry["power"]])
                result = current if current["stdout"].strip() == "running" else command(
                    ["virsh", "-c", "qemu:///system", "start", entry["power"]]
                )
                command(["sudo", "-n", "systemctl", "stop", f"{entry['unit']}.timer"])
            else:
                expected = {
                    "one-node": "systemctl start corosync", "no-majority": "systemctl start corosync",
                    "storage": "systemctl start nfs-server",
                    "replication-link": "nft delete table inet n3_replication",
                    "primary-site": "nft delete table inet n3_recovery",
                }[event["action"]]
                require(entry["undo"] == expected, "Untrusted recovery command in receipt.")
                result = self.ssh(entry["host"], expected)
                self.ssh(entry["host"], f"systemctl stop {shlex.quote(entry['unit'] + '.timer')}")
            if result["rc"] and "No such file" not in result["stderr"]:
                failures.append(entry["host"])
        require(not failures, f"Recovery failed for {failures}; evidence/lock retained; use rescue console.")
        event["restored"] = True
        event["end"] = time.time()
        self.save(f"{event['action']}.json", event)
        for _ in range(12):
            if all(self.ssh(h, "systemctl is-active corosync")["rc"] == 0 for h in HOSTS):
                break
            time.sleep(5)
        recovered = self.snapshot("recovered")
        healthy(recovered)
        path.unlink(missing_ok=True)

    def probe(self, duration):
        require(1 <= duration <= 180, "Probe duration must be 1..180 seconds.")
        samples = []
        deadline = time.monotonic() + duration
        while time.monotonic() < deadline:
            samples.append(self.sample(transaction=True))
            time.sleep(1)
        self.snapshot("load", samples)

    def permissions(self):
        require(self.id == "pve-qualifier-stockage-partage", "Not a shared-storage exercise.")
        denial = self.cfg["denied_export"]
        require(re.fullmatch(r"/n3-denied-[a-z0-9-]+", denial), "Negative export outside lab allocation.")
        host = HOSTS[1]
        mount = f"/var/lib/lab-proxmox/{self.id}/negative"
        server = self.addresses[self.sources["nfs"]]
        create = self.ssh(host, f"test ! -e {mount} && mkdir -p {mount}")
        require(create["rc"] == 0, "Negative mountpoint already exists; never reuse/remove an unknown mount.")
        try:
            result = self.ssh(host, "timeout 10 mount -t nfs "
                              "-o ro,nosuid,nodev,noexec,retry=0,timeo=10,retrans=1 "
                              f"{shlex.quote(server + ':' + denial)} {mount}")
            self.save("permissions-negative.json", {"lab": self.id, "at": time.time(), "result": result})
            require(result["rc"] != 0 and re.search(r"denied|permission|not exported", result["stderr"], re.I),
                    "Negative fixture lacks an actual NFS permission refusal.")
        finally:
            self.ssh(host, f"if mountpoint -q {mount}; then umount {mount}; fi; rmdir {mount}")

    def event(self, action):
        event = self.load(action)
        require(event["action"] == action and event["restored"]
                and event["hosts"] and event.get("observed_at"),
                "Missing controller-imposed, observed and recovered failure.")
        require(0 < event["end"] - event["at"] <= event["duration"] + 360,
                "Failure/recovery exceeded its documented bound.")
        return event

    def verify(self, criterion):
        require(criterion in {p["id"] for p in self.contract["points_a_tester"]},
                "Unknown catalog criterion.")
        allocation = self.load("allocation")
        baseline = self.load("baseline")
        require(allocation["baseline_sha256"] == digest(json.dumps(baseline, sort_keys=True)),
                "Baseline has been altered.")
        live = self.snapshot("reintegrated")
        healthy(live)
        require(not (self.evidence / "active.json").exists(), "Experiment still active.")
        check(self, criterion, baseline, live)

    def cleanup(self):
        self.restore()
        for host in HOSTS:
            result = self.ssh(host, "systemctl is-active corosync")
            require(result["rc"] == 0, f"{host}: corosync is not restored; refusing evidence removal.")
            self.ssh(host, f"rm -f /etc/pve/n3-{self.id}-quorum-probe")
        # Instructor resources, backups, cluster membership and disks are never destroyed.
        for file in self.evidence.glob("*.json"):
            file.unlink()
        self.evidence.rmdir()


def placement(c, phase, baseline, vmid=None):
    vmid = vmid or c.ids[0]
    state = c.load(phase)
    target = c.cfg["destination"]
    require(target in HOSTS, "Destination outside cluster allocation.")
    node = state["nodes"][target]["name"]["stdout"].strip()
    actual = guests(state, c.ids)
    require(actual[vmid]["node"] == node and actual[vmid]["status"] == "running",
            "Guest is not running on the requested destination.")
    require(owners(state, vmid) == [target], "QEMU process ownership is not unique.")
    same_data(baseline, state)
    return state


def rejected(c, phase, task_type):
    state = c.load(phase)
    candidates = []
    for node in state["nodes"].values():
        for task in parsed(node["tasks"]):
            if (task.get("type") == task_type and task.get("id") in {str(v) for v in c.ids}
                    and task.get("starttime", 0) >= c.load("baseline")["at"]):
                candidates.append((node, task))
    require(candidates, "No real guest-specific rejected task since the baseline.")
    for node, task in candidates:
        name = node["name"]["stdout"].strip()
        upid = task["upid"]
        require(re.fullmatch(r"UPID:[A-Za-z0-9:_.@-]+:", upid), "Invalid UPID.")
        status = parsed(c.read(next(h for h, n in state["nodes"].items() if n is node),
                               f"/nodes/{name}/tasks/{upid}/status"))
        if (status.get("status") == "stopped" and status.get("exitstatus")
                and status.get("exitstatus") != "OK"):
            return state, status
    raise PreconditionError("Task did not terminate with a real error; HTTP acceptance is insufficient.")


def capacity(c, state):
    host_data = [x for x in resources(state) if x["type"] == "node"]
    require(len(host_data) == 3, "No real three-node capacity measurements.")
    reserve = max(x["maxmem"] for x in host_data)
    usable = sum(x["maxmem"] - x["mem"] for x in host_data) - reserve
    budget = c.cfg["budget"]
    require(budget["host_overhead_bytes"] > 0 and budget["recovery_bytes"] > 0,
            "Explicit measured host overhead and recovery budget required.")
    reserved_ids = c.ids[:2] if c.id == "pve-reserver-capacite" else c.ids
    configured = sum(x.get("maxmem", 0) for x in resources(state)
                     if x.get("vmid") in reserved_ids)
    require(configured + budget["host_overhead_bytes"] + budget["recovery_bytes"]
            <= sum(x["maxmem"] for x in host_data) - reserve,
            "Configured guests consume the N-1 recovery reserve.")
    require(usable >= budget["recovery_bytes"], "Measured free memory does not retain the reserve.")
    storage = parsed(next(iter(state["nodes"].values()))["storage"])
    entry = next((x for x in storage if x["storage"] == c.contract["storage_id"]), None)
    require(entry and entry.get("avail", 0) >= budget["disk_reserve_bytes"] > 0,
            "Dedicated storage lacks the measured disk recovery reserve.")
    return usable


def no_quorum(c):
    c.event("no-majority")
    state = c.load("no-quorum")
    event = c.load("no-majority")
    survivors = set(HOSTS) - set(event["hosts"])
    require(len(survivors) == 1, "Wrong loss-of-majority scenario.")
    node = state["nodes"][survivors.pop()]
    require(not quorum(node) and votes_unmodified(node),
            "Quorum was bypassed or expected votes were forced.")
    require(event["write_probe"]["rc"] not in {0, 255} and re.search(
        r"Permission denied|Read-only file system|Operation not permitted",
        event["write_probe"]["stderr"], re.I), "No real pmxcfs write refusal.")


def replication(c):
    state = c.load("replicated")
    source = c.cfg["source"]
    target = c.cfg["destination"]
    require(source in HOSTS and target in HOSTS and source != target, "Invalid replication placement.")
    jobs = parsed(state["nodes"][source]["replication"])
    job = next((j for j in jobs if j.get("id") == f"{c.ids[0]}-0"), None)
    require(job and job.get("target") == state["nodes"][target]["name"]["stdout"].strip(),
            "Replication job points to the wrong guest/target.")
    require(job.get("last_sync", 0) > c.load("baseline")["at"]
            and not job.get("fail_count", 0) and not job.get("error"),
            "Replication has not completed successfully in this run.")
    for host in (source, target):
        zfs = state["nodes"][host]["zfs"]
        require(zfs["rc"] == 0 and f"vm-{c.ids[0]}-disk-" in zfs["stdout"]
                and "__replicate_" in zfs["stdout"], "Real ZFS volume/snapshot identity missing.")
    snapshot_guids = []
    for host in (source, target):
        snapshot_guids.append({
            line.split("\t")[1] for line in state["nodes"][host]["zfs"]["stdout"].splitlines()
            if f"vm-{c.ids[0]}-disk-" in line and "@__replicate_" in line
            and len(line.split("\t")) >= 2
        })
    require(snapshot_guids[0] & snapshot_guids[1], "No common received snapshot GUID across ZFS peers.")
    return state, job


def offsite(c, baseline):
    c.event("primary-site")
    restored = c.load("restored")
    source = restored["sources"]["recovery"]
    files = parsed(source["files"])
    require(any(x.get("filename") == "qemu-server.conf.blob" for x in files)
            and any(x.get("filename", "").endswith(".img.fidx") for x in files),
            "Secondary snapshot archive manifest lacks the actual VM configuration/data.")
    stores = parsed(source["storage_config"])
    secondary = next((s for s in stores if s["storage"] == "n3-secondary"), None)
    require(secondary and secondary.get("type") == "pbs"
            and secondary.get("server") in {
                c.sources["pbs_secondary"], c.addresses[c.sources["pbs_secondary"]]
            }, "Recovery backup repository is not the independent secondary PBS.")
    target_store = next((s for s in stores if s["storage"] == c.contract["storage_id"]), None)
    require(target_store and target_store.get("type") in {"dir", "zfspool", "lvmthin"},
            "Recovery guest disks must use independent local recovery storage.")
    for role in ("pbs_secondary",):
        tasks = parsed(restored["sources"][role]["tasks"])
        require(any(t.get("worker_type") == "sync" and t.get("status") == "OK"
                    for t in tasks), "No completed secondary synchronization task.")
    require(source["firewall"]["rc"] == 0 and "counter" in source["firewall"]["stdout"],
            "Primary dependencies were not blocked throughout recovery.")
    for host in HOSTS:
        require(c.addresses[host] in source["firewall"]["stdout"], "Primary host not blocked.")
    require(all(c.addresses[h] not in source["connections"]["stdout"] for h in HOSTS),
            "Recovery still contacts a primary dependency.")
    if "pbs_primary" in c.sources:
        primary = c.addresses[c.sources["pbs_primary"]]
        require(primary in source["firewall"]["stdout"] and primary not in source["connections"]["stdout"],
                "Primary PBS dependency was not excluded.")
    loaded = parsed(source["resources"])
    require(any(x.get("vmid") == c.ids[0] and x.get("status") == "running" for x in loaded),
            "Assigned recovery guest is not actually running.")
    require(sum(p["vmid"] == c.ids[0] for p in parsed(source["processes"])) == 1,
            "Recovery QEMU process not unique.")
    tasks = parsed(source["tasks"])
    require(any(t.get("type") == "qmrestore" and t.get("id") == str(c.ids[0])
                and t.get("status") == "OK" and t.get("starttime", 0) >= c.load("primary-site")["at"]
                for t in tasks), "No real successful same-allocation recovery task during primary isolation.")
    current = {**restored, "samples": restored["recovery_samples"]}
    require(business(current)["marker"] == business(baseline)["marker"], "Recovered marker differs.")
    return current


def check(c, criterion, baseline, live):
    lab = c.id
    if lab == "pve-eprouver-cluster":
        if criterion == "coherence":
            healthy(live)
        elif criterion == "majorite":
            event = c.event("one-node")
            state = c.load("majority")
            survivors = set(HOSTS) - set(event["hosts"])
            for host in survivors:
                require(quorum(state["nodes"][host]) and votes_unmodified(state["nodes"][host])
                        and len(members(state["nodes"][host])) == 2, "Two survivors did not retain quorum.")
        elif criterion == "sans-quorum":
            no_quorum(c)
        else:
            healthy(c.load("recovered"))
    elif lab == "pve-qualifier-stockage-partage":
        if criterion == "partage":
            state = c.load("qualified")
            hashes = {parsed_nonce(n["nonce"]) for n in state["nodes"].values()}
            mounts = [parsed(n["mount"])["filesystems"][0] for n in state["nodes"].values()]
            require(len(hashes) == 1 and all(m["fstype"].startswith("nfs") for m in mounts)
                    and len({m["source"] for m in mounts}) == 1, "Not the same NFS dataset/nonce.")
        elif criterion == "permissions":
            require(c.load("qualified")["sources"]["nfs"]["exports"]["rc"] == 0,
                    "NFS export configuration is not readable.")
            result = c.load("permissions-negative")["result"]
            require(result["rc"] != 0 and re.search(r"denied|permission|not exported", result["stderr"], re.I),
                    "No actual denied NFS operation; export listing is insufficient.")
        elif criterion == "panne":
            c.event("storage")
            state = c.load("storage-unavailable")
            require(any(n["nonce"]["rc"] != 0 for n in state["nodes"].values()),
                    "Storage loss did not cause a real I/O failure.")
            require(any("error" in p for p in state["samples"]), "No measured service impact.")
        else:
            before, after = c.load("qualified"), c.load("recovered")
            require({parsed_nonce(n["nonce"]) for n in before["nodes"].values()}
                    == {parsed_nonce(n["nonce"]) for n in after["nodes"].values()}, "Nonce data changed.")
            same_data(baseline, after)
    elif lab == "pve-migrer-instance":
        if criterion == "prevol":
            state, _ = rejected(c, "preflight-rejected", "qmigrate")
            require(owners(state, c.ids[0]) == owners(baseline, c.ids[0]),
                    "Rejected migration left an unexpected active copy.")
        elif criterion in {"placement", "dependances"}:
            phase = "migrated" if criterion == "placement" else "rebooted"
            state = placement(c, phase, baseline)
            ct = guests(state, c.ids)[c.contract["ct_id"]]
            require(ct["node"] == state["nodes"][c.cfg["destination"]]["name"]["stdout"].strip()
                    and ct["status"] == "running", "CT placement/service not restored.")
            running_ct = [
                h for h, n in state["nodes"].items()
                if n["ct_process"]["rc"] == 0 and "RUNNING" in n["ct_process"]["stdout"]
            ]
            require(running_ct == [c.cfg["destination"]], "CT process ownership is not unique on target.")
            same_data({**baseline, "samples": baseline["ct_samples"]},
                      {**state, "samples": state["ct_samples"]})
            if criterion == "dependances":
                tasks = [t for n in state["nodes"].values() for t in parsed(n["tasks"])]
                require(all(any(t.get("id") == str(v) and t.get("type") in {"qmstart", "vzstart"}
                                and t.get("starttime", 0) > c.load("migrated")["at"] for t in tasks)
                            for v in c.ids), "Both guests must really restart on destination.")
        else:
            same_data(baseline, c.load("migrated"))
            require(c.load("load")["samples"], "Missing external migration timeline.")
    elif lab == "pve-reserver-capacite":
        if criterion == "budget":
            capacity(c, live)
        elif criterion == "placement":
            for state in (baseline, c.load("migrated")):
                actual = guests(state, c.ids)
                require(actual[c.ids[0]]["node"] != actual[c.ids[1]]["node"],
                        "Loads that must be separated run on the same node.")
                rules = parsed(next(iter(state["nodes"].values()))["ha_rules"])
                require(any(r.get("type") == "resource-affinity" and r.get("affinity") == "negative"
                            and all(f"vm:{v}" in r.get("resources", "") for v in c.ids[:2])
                            and not r.get("disable", 0) for r in rules),
                        "No effective enabled resource anti-affinity rule for both allocated loads.")
        elif criterion == "surcharge":
            state = c.load("candidate-rejected")
            require(c.cfg["candidate_bytes"] > capacity(c, state), "Candidate does not exceed reserve.")
            require(guests(state, c.ids)[c.ids[2]]["maxmem"] == c.cfg["candidate_bytes"],
                    "Declared candidate demand differs from actual configured maximum memory.")
            require(guests(state, c.ids)[c.ids[2]]["status"] == "stopped"
                    and not owners(state, c.ids[2]), "Candidate consumed reserved capacity.")
        else:
            capacity(c, c.load("load"))
            business(c.load("load"))
    elif lab == "pve-mesurer-replication":
        if criterion == "job":
            replication(c)
        elif criterion == "rpo":
            replicated, job = replication(c)
            c.event("one-node")
            recovered = placement(c, "source-unavailable", replicated)
            a, b = business(c.load("load")), business(recovered)
            require(a["sequence"] >= b["sequence"] >= business(replicated)["sequence"],
                    "Recovered sequence not bounded by completed replication/acknowledged writes.")
            require(job["last_sync"] <= c.load("one-node")["at"], "Replica was updated after source loss.")
        elif criterion == "retard":
            c.event("replication-link")
            jobs = parsed(c.load("replication-failed")["nodes"][c.cfg["source"]]["replication"])
            require(any(j.get("id") == f"{c.ids[0]}-0" and (j.get("error") or j.get("fail_count", 0))
                        for j in jobs), "No actual replication error; VM status is not job status.")
        else:
            require(len(owners(live, c.ids[0])) == 1, "Return plan permits double writing.")
            business(live)
    elif lab == "pve-eprouver-ha":
        if criterion == "negatif":
            no_quorum(c)
            same_data(baseline, live)
        else:
            c.event("one-node")
            state = c.load("failover")
            event = c.load("one-node")
            require(event["at"] <= state["at"] <= event["end"],
                    "Failover observation was not captured during the imposed failure.")
            if criterion == "panne-reelle":
                event = c.load("one-node")
                affected = event["hosts"][0]
                require(affected in owners(baseline, c.ids[0]), "Failure did not remove the original owner.")
                require(affected not in owners(state, c.ids[0]), "Original owner still runs QEMU.")
                text = "\n".join(n["journal"]["stdout"] for n in state["nodes"].values())
                require(re.search(r"fenc|watchdog", text, re.I), "No fencing/watchdog observations.")
            elif criterion == "unicite":
                require(len(owners(state, c.ids[0])) == 1 and len(owners(live, c.ids[0])) == 1,
                        "Multi-node observations do not prove a unique QEMU writer.")
            else:
                same_data(baseline, state)
                require(any("error" in p for p in c.load("majority")["samples"]),
                        "No measured client outage; cannot claim tested failover.")
    elif lab == "pve-maintenir-cluster":
        state = c.load("maintenance")
        if criterion == "evacuation":
            node = state["nodes"][c.cfg["maintenance_node"]]["name"]["stdout"].strip()
            require(not any(x.get("vmid") and x.get("node") == node and x.get("status") == "running"
                            for x in resources(state)), "Running guest forgotten on maintained node.")
        elif criterion == "quorum":
            c.event("one-node")
            for host in set(HOSTS) - set(c.load("one-node")["hosts"]):
                require(quorum(c.load("majority")["nodes"][host]), "Maintenance lost survivor quorum.")
            capacity(c, state)
        elif criterion == "reintegration":
            healthy(live)
            for node in live["nodes"].values():
                require(all(x.get("active") == 1 for x in parsed(node["storage"])),
                        "A returned node cannot access its storage.")
        else:
            same_data(baseline, live)
            tasks = [t for n in live["nodes"].values() for t in parsed(n["tasks"])]
            require(any(t.get("type") == "vzdump" and t.get("status") == "OK"
                        and t.get("starttime", 0) > state["at"] for t in tasks),
                    "No actual successful post-maintenance backup task.")
            same_data(baseline, c.load("restored"))
            require(any(t.get("type") == "qmrestore" and t.get("id") == str(c.ids[0])
                        and t.get("status") == "OK" and t.get("starttime", 0) > state["at"]
                        for t in tasks), "Marker must come from a real post-maintenance restoration.")
    elif lab == "pve-reprendre-hors-site":
        current = offsite(c, baseline)
        if criterion == "mesure":
            objectives(c, baseline, current)
    elif lab == "pve-epreuve-disponibilite":
        if criterion == "architecture":
            capacity(c, live)
            configs = parsed(next(iter(live["nodes"].values()))["storage_config"])
            store = next((s for s in configs if s["storage"] == c.contract["storage_id"]), None)
            require(store and store["type"] in {"nfs", "rbd", "zfspool"},
                    "A shared flag on local storage is not shared storage.")
        elif criterion == "bascule":
            c.event("one-node")
            state = c.load("failover")
            require(len(owners(state, c.ids[0])) == 1, "No unique failover writer.")
            same_data(baseline, state)
            objectives(c, baseline, state)
        elif criterion == "donnees":
            require(business(c.load("load"))["sequence"] >= business(c.load("failover"))["sequence"],
                    "Data timeline cannot be reconciled with acknowledged transactions.")
            business(offsite(c, baseline))
        elif criterion == "maintenance":
            healthy(live)
            rejected(c, "preflight-rejected", "qmigrate")
            same_data(baseline, c.load("maintenance"))
        else:
            objectives(c, baseline, offsite(c, baseline))
    report = c.work / "report.md"
    require(report.is_file() and len(report.read_text().strip()) >= 300,
            "Missing substantive runbook/observations/limits report; human review is mandatory.")


def parsed_nonce(result):
    require(result["rc"] == 0, "Dedicated storage nonce cannot be read.")
    value = result["stdout"].split()[0]
    require(re.fullmatch(r"[0-9a-f]{64}", value), "Invalid nonce fingerprint.")
    return value


def objectives(c, baseline, state):
    before, after = business(baseline), business(state)
    require(before["marker"] == after["marker"], "Recovered business marker differs.")
    event = c.load("primary-site" if state.get("recovery_samples") else "one-node")
    samples = successful_samples(state)
    first = min(p["at"] for p in samples)
    require(0 <= first - event["at"] <= c.cfg["rto_seconds"], "Measured RTO exceeds announced objective.")
    acknowledged = before["sequence"]
    load_file = c.evidence / "load.json"
    if load_file.exists():
        acknowledged = max(
            [acknowledged] + [s["body"]["sequence"] for s in successful_samples(c.load("load"))
                              if s["at"] <= event["at"]]
        )
    require(0 <= acknowledged - after["sequence"] <= c.cfg["rpo_transactions"],
            "Measured RPO exceeds announced transaction objective.")


def main(lab):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "snapshot", "probe", "permissions", "fail", "restore", "check", "cleanup"])
    parser.add_argument("--phase", choices=sorted(PHASES))
    parser.add_argument("--criterion")
    parser.add_argument("--action")
    parser.add_argument("--hosts", nargs="+", default=[])
    parser.add_argument("--duration", type=int, default=30)
    args = parser.parse_args()
    try:
        evidence = Path(lab) / "challenge/work/evidence"
        if args.command == "cleanup" and not evidence.exists():
            return
        c = Controller(lab)
        if args.command == "snapshot":
            c.snapshot(args.phase)
        elif args.command == "probe":
            c.probe(args.duration)
        elif args.command == "fail":
            c.fail(args.action, args.duration, args.hosts)
        elif args.command == "check":
            c.verify(args.criterion)
        else:
            getattr(c, args.command)()
    except (PreconditionError, OSError, ValueError, KeyError, StopIteration,
            subprocess.TimeoutExpired, ImportError) as exc:
        parser.exit(2, f"N3 PRECONDITION / PRÉCONDITION: {exc}\n")


if __name__ == "__main__":
    main(Path(__file__).resolve().parent.parent)
