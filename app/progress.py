"""Per-user progress: module completion, quiz scores, game bests, points, flags."""
import json, os, time, threading, hashlib

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA, exist_ok=True)
DB = os.path.join(DATA, "progress.json")
_lock = threading.Lock()

def _load():
    try:
        with open(DB) as f:
            return json.load(f)
    except Exception:
        return {}

def _save(d):
    tmp = DB + ".tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, indent=1)
    os.replace(tmp, DB)

def _user(db, u):
    return db.setdefault(u, {
        "modules": {},      # module_id -> {done:bool, quiz:score, theory_read:bool, ts}
        "games": {},        # game_id -> {best:int, attempts:int, last_ts}
        "flags": [],        # captured flags
        "boxes": {},        # box_id -> {state, spawned_at}
        "activity": [],     # recent events
        "created": time.time(),
    })

def get(u):
    with _lock:
        db = _load()
        return _user(db, u)

def all_users():
    with _lock:
        return _load()

def record_module(u, module_id, patch):
    with _lock:
        db = _load()
        usr = _user(db, u)
        cur = usr["modules"].setdefault(module_id, {})
        cur.update(patch)
        cur["ts"] = time.time()
        usr["activity"].insert(0, {"t": time.time(), "what": f"module {module_id}", "patch": patch})
        usr["activity"] = usr["activity"][:50]
        _save(db)
        return cur

def record_game(u, game_id, score, points_awarded):
    with _lock:
        db = _load()
        usr = _user(db, u)
        cur = usr["games"].setdefault(game_id, {"best": 0, "attempts": 0})
        cur["attempts"] += 1
        improved = score > cur["best"]
        if improved:
            cur["best"] = score
        cur["last_ts"] = time.time()
        usr["activity"].insert(0, {"t": time.time(), "what": f"game {game_id}", "patch": {"score": score}})
        usr["activity"] = usr["activity"][:50]
        _save(db)
        return cur, improved

def award_flag(u, flag):
    with _lock:
        db = _load()
        usr = _user(db, u)
        if flag in usr["flags"]:
            return False
        usr["flags"].append(flag)
        usr["activity"].insert(0, {"t": time.time(), "what": "flag", "patch": {"flag": flag}})
        usr["activity"] = usr["activity"][:50]
        _save(db)
        return True

def set_box(u, box_id, patch):
    with _lock:
        db = _load()
        usr = _user(db, u)
        b = usr["boxes"].setdefault(box_id, {})
        b.update(patch)
        _save(db)
        return b

def points(u, catalog, games):
    """Account points: modules completed + quiz scores + game bests + flags."""
    me = get(u)
    total = 0
    for m in catalog:
        st = me["modules"].get(m["id"], {})
        if st.get("theory_read"):
            total += max(1, m["points"] // 4)
        if st.get("quiz") is not None:
            qn = len(m.get("quiz", [])) or 1
            total += int(m["points"] * (st["quiz"] / qn))
        if st.get("done"):
            total += m["points"] // 2
    for g in games:
        gs = me["games"].get(g["id"])
        if gs and gs.get("best"):
            total += int(g["points"] * min(1.0, gs["best"]))
    total += 50 * len(me["flags"])
    return total
