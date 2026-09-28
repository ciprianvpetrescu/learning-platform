"""Instance spawner.

Each user's box is a container on their own isolated docker bridge network
(10.66.<uid>.0/24), with no route to the host or to other users. The Kali
terminal container joins the same bridge, which is how users attack their box
without ever installing anything.

State lives in data/instances.json. A reaper thread destroys expired instances.
"""
import json, os, threading, time, ipaddress, secrets

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA, exist_ok=True)
STATE = os.path.join(DATA, "instances.json")
_lock = threading.Lock()
TTL = 60 * 60  # one hour per instance

# Image per box. Built by boxes/build.sh; falls back to a generic debian if absent.
IMAGE_MAP = {
  "box-web-easy":      "learn/box-web-easy:latest",
  "box-xss":           "learn/box-xss:latest",
  "box-idor":          "learn/box-idor:latest",
  "box-lfi":           "learn/box-lfi:latest",
  "box-ssrf":          "learn/box-ssrf:latest",
  "box-sqli":          "learn/box-sqli:latest",
  "box-linux-privesc": "learn/box-linux:latest",
  "box-forensics":     "learn/box-forensics:latest",
  "box-memory":        "learn/box-forensics:latest",
  "box-malware-static":"learn/box-forensics:latest",
  "box-docker-escape": "learn/box-docker:latest",
  "box-kerberoast":    "learn/box-ad:latest",
  "box-metasploitable":"learn/box-legacy:latest",   # native ARM build; the amd64 image cannot run here
  "box-network-lab":   "learn/box-network:latest",
}
KALI_IMAGE = "learn/kali:latest"

def _load():
    try:
        with open(STATE) as f:
            return json.load(f)
    except Exception:
        return {}

def _save(d):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, indent=1)
    os.replace(tmp, STATE)

def _uid(username):
    """Stable per-user octet for the network, 2..254."""
    h = 0
    for c in username:
        h = (h * 131 + ord(c)) & 0xFFFFFFFF
    return 2 + (h % 250)


# ---- browser terminal (ttyd inside the kali sidecar) ----
TERM_BASE = 8100  # host port for user 0; each user gets a stable slice
TERM_SPAN = 50    # 50 ports per user, ttyd listens on +0

def term_port(username):
    """Stable host port for this user's ttyd."""
    return TERM_BASE + (_uid(username) % 900) + TERM_SPAN

def net_for(username):
    o = _uid(username)
    return f"learn_{o}", f"10.66.{o}.0/24", f"10.66.{o}"

def _docker():
    import docker
    return docker.from_env()

_available = None
def docker_ok():
    global _available
    if _available is None:
        try:
            c = _docker(); c.ping(); _available = True
        except Exception:
            _available = False
    return _available

def _ensure_network(netname, subnet):
    """Create the per-user isolated bridge if it does not exist.

    internal=False so the Kali sidecar can install extra tooling if the user
    wants it; the two containers only see each other and the gateway.
    """
    c = _docker()
    try:
        c.networks.get(netname)
    except Exception:
        c.networks.create(netname, driver="bridge",
                          ipam={"Config": [{"Subnet": subnet}]},
                          internal=False,
                          options={"com.docker.network.bridge.enable_icc": "true"})
    return netname

def spawn(username, box):
    """Start the box and a Kali sidecar for this user. Returns instance info."""
    if not docker_ok():
        return {"error": "docker unavailable"}
    bid = box["id"]
    image = IMAGE_MAP.get(bid)
    if not image:
        return {"error": "no image mapped for this box"}
    netname, subnet, prefix = net_for(username)
    c = _docker()
    _ensure_network(netname, subnet)

    with _lock:
        st = _load()
        key = f"{username}::{bid}"
        cur = st.get(key)
        # tear down any existing instance for this box first
        if cur:
            _destroy_unlocked(c, cur)

    flag = "LEARN{" + secrets.token_hex(8) + "}"
    host_ip = prefix + ".10"
    kali_ip = prefix + ".20"

    name = f"learn-{_uid(username)}-{bid.replace('box-','')}"
    try:
        for nm in (name,):
            try: c.containers.get(nm).remove(force=True)
            except Exception: pass
        box_c = c.containers.run(
            image, name=name, detach=True,
            hostname=bid.replace("box-", ""),
            environment={"FLAG": flag},
            labels={"learn.user": username, "learn.box": bid},
        )
        # attach to the user's isolated bridge at a fixed, predictable address
        c.networks.get(netname).connect(box_c, ipv4_address=host_ip)
    except Exception as e:
        try: c.containers.get(name).remove(force=True)
        except Exception: pass
        return {"error": f"container start failed: {e}"}

    # Kali sidecar, same bridge, so the user can attack the box
    kali_name = f"learn-{_uid(username)}-kali"
    try:
        c.containers.get(kali_name).remove(force=True)
    except Exception:
        pass
    kali_info = None
    tport = term_port(username)
    try:
        k = c.containers.run(
            KALI_IMAGE, name=kali_name, detach=True,
            hostname="kali",
            # ttyd gives the user a real browser shell with no install
            command=["bash", "-lc",
                     # theme is baked into /usr/local/bin/learn-ttyd inside the
                     # image; passing -t on the command line made bash echo the
                     # quoted JSON into the terminal on startup.
                     "exec ttyd -p 7681 -W learn-ttyd"],
            ports={"7681/tcp": tport},
            # nmap needs raw sockets; NET_RAW + NET_ADMIN is enough and far
            # narrower than privileged. No docker socket, no host mounts.
            cap_add=["NET_RAW", "NET_ADMIN"],
            labels={"learn.user": username, "learn.role": "kali"},
        )
        c.networks.get(netname).connect(k, ipv4_address=kali_ip)
        # keep the sidecar off the shared default bridge
        try:
            c.networks.get("bridge").disconnect(k)
        except Exception:
            pass
        kali_info = {"id": k.id[:12], "ip": kali_ip, "term_port": tport}
    except Exception as e:
        kali_info = {"error": str(e)}

    rec = {
        "user": username, "box": bid, "title": box["title"],
        "network": netname, "subnet": subnet,
        "host_ip": host_ip, "kali_ip": kali_ip,
        "container": name, "kali": kali_name,
        "term_port": (kali_info or {}).get("term_port"),
        "flag": flag,
        "ports": box.get("ports", []),
        "started": time.time(), "expires": time.time() + TTL,
        "state": "running",
    }
    with _lock:
        st = _load(); st[f"{username}::{bid}"] = rec; _save(st)
    return rec

def _destroy_unlocked(c, rec):
    for key in ("container", "kali"):
        nm = rec.get(key)
        if nm:
            try:
                c.containers.get(nm).remove(force=True)
            except Exception:
                pass

def destroy(username, box_id):
    if not docker_ok():
        return {"error": "docker unavailable"}
    c = _docker()
    with _lock:
        st = _load()
        key = f"{username}::{box_id}"
        rec = st.get(key)
        if not rec:
            return {"error": "no such instance"}
        _destroy_unlocked(c, rec)
        rec["state"] = "destroyed"
        st.pop(key, None)
        _save(st)
    return {"ok": True}

def list_for(username):
    st = _load()
    out = []
    now = time.time()
    for k, v in st.items():
        if v.get("user") == username:
            v = dict(v); v["ttl_left"] = max(0, int(v.get("expires", 0) - now))
            v.pop("flag", None)  # never leak the flag to the client
            out.append(v)
    return out

def reap():
    """Destroy expired instances. Runs in a background thread."""
    while True:
        try:
            time.sleep(60)
            if not docker_ok():
                continue
            c = _docker()
            now = time.time()
            with _lock:
                st = _load(); changed = False
                for k in list(st.keys()):
                    rec = st[k]
                    if rec.get("expires", 0) < now:
                        _destroy_unlocked(c, rec)
                        st.pop(k, None)
                        changed = True
                if changed:
                    _save(st)
        except Exception:
            pass

def start_reaper():
    t = threading.Thread(target=reap, daemon=True)
    t.start()
    return t
