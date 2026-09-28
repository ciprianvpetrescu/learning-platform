"""learning.simplu.ie - hands-on cybersecurity academy.

FastAPI app: UI, content API, game engine, vulnerable-instance spawner.
Runs behind Caddy on 18472, portal-gated by the shared authportal cookie.
"""
import os, sys, json, time, random, secrets, hashlib, base64, hmac

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse, Response
import websockets
import asyncio
from fastapi import WebSocket
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import content
from content.categories import CATEGORIES
from games.registry import GAMES
from games.banks import BANKS
from boxes.defs import BOXES, BY_ID as BOX_BY_ID
import app.progress as progress
import app.spawner as spawner
import app.grader as grader
from games.registry import by_id as game_by_id

app = FastAPI(title="learning.simplu.ie")
AUTHPORTAL = "/home/ccc/authportal"

def _portal_secret():
    try:
        with open(os.path.join(AUTHPORTAL, "secret.key")) as f:
            return f.read().strip()
    except Exception:
        return ""

def portal_user(request: Request):
    raw = request.cookies.get("fred_auth")
    if not raw:
        return None
    try:
        payload, sig = raw.rsplit(".", 1)
        good = hmac.new(_portal_secret().encode(), payload.encode(), hashlib.sha256).hexdigest()[:32]
        if not hmac.compare_digest(good, sig):
            return None
        pad = "=" * (-len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload + pad))
        if data.get("exp", 0) < time.time():
            return None
        return data.get("u")
    except Exception:
        return None

def who(request: Request):
    u = portal_user(request)
    if not u:
        raise HTTPException(status_code=401, detail="not authenticated")
    return u

app.mount("/static", StaticFiles(directory=os.path.join(HERE, "static")), name="static")

@app.get("/")
def index():
    return FileResponse(os.path.join(HERE, "static", "index.html"))

@app.get("/api/me")
def api_me(request: Request):
    u = who(request)
    st = progress.get(u)
    return {"user": u, "points": progress.points(u, content.MODULES, GAMES),
            "flags": len(st.get("flags", [])),
            "modules_done": sum(1 for m in st.get("modules", {}).values() if m.get("done")),
            "games_played": len(st.get("games", {}))}

@app.get("/api/catalog")
def api_catalog(request: Request):
    u = portal_user(request)
    st = progress.get(u) if u else {"modules": {}, "games": {}}
    cats = []
    for cid, c in CATEGORIES.items():
        mods = content.by_cat(cid)
        gms = [g for g in GAMES if g["cat"] == cid]
        cats.append({**c, "id": cid,
            "module_count": len(mods), "game_count": len(gms),
            "points": sum(m["points"] for m in mods),
            "modules": [{
                "id": m["id"], "title": m["title"], "tier": m["tier"],
                "points": m["points"], "summary": m["summary"],
                "theory_count": len(m.get("theory", [])),
                "quiz_count": len(m.get("quiz", [])),
                "lab_count": len(m.get("labs", [])),
                "progress": st.get("modules", {}).get(m["id"], {}),
            } for m in mods],
            "games": [{"id": g["id"], "title": g["title"], "blurb": g["blurb"],
                       "kind": g["kind"], "points": g["points"],
                       "best": st.get("games", {}).get(g["id"], {}).get("best", 0)} for g in gms]})
    return {"categories": cats,
            "boxes": [{"id": b["id"], "title": b["title"], "cat": b["cat"],
                       "tier": b["tier"], "points": b["points"], "summary": b["summary"],
                       "skills": b.get("skills", []), "entry": b.get("entry", ""),
                       "ports": b.get("ports", []), "teaches": b.get("teaches", "")} for b in BOXES],
            "docker": spawner.docker_ok(), "stats": content.stats()}

@app.get("/api/module/{mid}")
def api_module(mid: str, request: Request):
    m = content.BY_ID.get(mid)
    if not m:
        raise HTTPException(404, "no such module")
    u = portal_user(request)
    st = progress.get(u).get("modules", {}).get(mid, {}) if u else {}
    return {"module": {k: v for k, v in m.items() if k != "quiz"},
            "quiz": [{"q": q["q"], "a": q["a"]} for q in m.get("quiz", [])],
            "progress": st}

class QuizIn(BaseModel):
    answers: list

@app.post("/api/module/{mid}/quiz")
def api_quiz(mid: str, body: QuizIn, request: Request):
    u = who(request)
    m = content.BY_ID.get(mid)
    if not m:
        raise HTTPException(404, "no such module")
    qs = m.get("quiz", [])
    correct = 0
    detail = []
    for i, q in enumerate(qs):
        given = body.answers[i] if i < len(body.answers) else None
        ok = grader.check_quiz(q, given)
        if ok: correct += 1
        detail.append({"ok": ok, "correct": q["c"], "why": q["why"]})
    progress.record_module(u, mid, {"quiz": correct, "done": True})
    return {"score": correct, "total": len(qs), "detail": detail,
            "points": progress.points(u, content.MODULES, GAMES)}

@app.post("/api/module/{mid}/read")
def api_read(mid: str, request: Request):
    u = who(request)
    progress.record_module(u, mid, {"theory_read": True})
    return {"ok": True, "points": progress.points(u, content.MODULES, GAMES)}

# ---------- games ----------
@app.get("/api/game/{gid}")
def api_game(gid: str):
    g = game_by_id(gid)
    b = BANKS.get(gid)
    if not g or not b:
        raise HTTPException(404, "no such game")
    ch = b["challenges"]
    order = list(range(len(ch)))
    random.shuffle(order)
    lim = g.get("rounds") or len(ch)
    out = []
    for i in order[:lim]:
        c = ch[i]
        item = {"idx": i, "q": c["q"], "hint": c.get("hint", "")}
        if "a" in c:
            opts = list(enumerate(c["a"]))
            random.shuffle(opts)
            item["kind"] = "quiz"
            item["a"] = [o[1] for o in opts]
            item["map"] = [o[0] for o in opts]
        elif "answers" in c:
            item["kind"] = "input"
        elif "order" in c:
            item["kind"] = "order"
            items = list(enumerate(c["items"]))
            random.shuffle(items)
            item["items"] = [x[1] for x in items]
            item["map"] = [x[0] for x in items]
            item["count"] = len(items)
        elif "correct" in c:
            item["kind"] = "pick"
            items = list(enumerate(c["items"]))
            random.shuffle(items)
            item["items"] = [x[1] for x in items]
            item["map"] = [x[0] for x in items]
        out.append(item)
    return {"game": dict(g), "intro": b.get("intro", ""),
            "seconds": b.get("seconds"), "rounds": out}

class GameSubmit(BaseModel):
    results: list

@app.post("/api/game/{gid}/submit")
def api_game_submit(gid: str, body: GameSubmit, request: Request):
    u = who(request)
    g = game_by_id(gid)
    b = BANKS.get(gid)
    if not g or not b:
        raise HTTPException(404, "no such game")
    ch = b["challenges"]
    results = []
    ok_count = 0
    for r in body.results:
        idx = r.get("idx")
        ans = r.get("answer")
        if not isinstance(idx, int) or idx < 0 or idx >= len(ch):
            continue
        c = ch[idx]
        if "a" in c:
            ok = (ans == c["c"])
        elif "answers" in c:
            ok = grader.check_input(g, c, ans if isinstance(ans, str) else str(ans))
        elif "order" in c:
            ok = (isinstance(ans, list) and ans == c["order"])
        elif "correct" in c:
            ok = (ans == c["correct"])
        else:
            ok = False
        if ok: ok_count += 1
        results.append({"idx": idx, "ok": ok, "why": c.get("why", ""),
                        "correct": c.get("c") if "a" in c else None})
    total = len(results) or 1
    score = ok_count / total
    rec, improved = progress.record_game(u, gid, score, int(g["points"] * score))
    return {"correct": ok_count, "total": total, "score": round(score, 3),
            "improved": improved, "best": rec["best"],
            "awarded": int(g["points"] * score), "results": results,
            "points": progress.points(u, content.MODULES, GAMES)}

# ---------- boxes and instances ----------
@app.get("/api/boxes")
def api_boxes(request: Request):
    u = portal_user(request)
    live = {b["box"]: b for b in spawner.list_for(u)} if u else {}
    out = []
    for b in BOXES:
        d = dict(b)
        d["instance"] = live.get(b["id"])
        out.append(d)
    return {"boxes": out, "docker": spawner.docker_ok()}

class SpawnIn(BaseModel):
    box: str

@app.post("/api/spawn")
def api_spawn(body: SpawnIn, request: Request):
    u = who(request)
    b = BOX_BY_ID.get(body.box)
    if not b:
        raise HTTPException(404, "no such box")
    rec = spawner.spawn(u, b)
    if "error" in rec:
        return JSONResponse({"error": rec["error"]}, status_code=503)
    safe = dict(rec); safe.pop("flag", None)
    return {"instance": safe}

class StopIn(BaseModel):
    box: str

@app.post("/api/stop")
def api_stop(body: StopIn, request: Request):
    u = who(request)
    return spawner.destroy(u, body.box)

@app.get("/api/instances")
def api_instances(request: Request):
    u = who(request)
    return {"instances": spawner.list_for(u), "docker": spawner.docker_ok()}

def _live_kali(u):
    """Return the running kali sidecar record for this user, if any."""
    for rec in spawner.list_for(u):
        if rec.get("term_port"):
            return rec
    return None

@app.get("/api/terminal")
def api_terminal(request: Request):
    """Where to point the browser terminal, and whether it is up."""
    u = who(request)
    rec = _live_kali(u)
    if not rec:
        return {"up": False, "reason": "no live instance"}
    import socket
    port = rec["term_port"]
    up = False
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            up = True
    except Exception:
        pass
    return {"up": up, "path": "/__term/%d/" % port, "box": rec.get("box"),
            "host_ip": rec.get("host_ip"), "ttl_left": rec.get("ttl_left")}

@app.websocket("/__term/{port}/{path:path}")
async def term_ws(websocket: WebSocket, port: int, path: str):
    """Relay the ttyd websocket for a port we actually spawned for this user.

    Frames are passed through verbatim (ttyd's own framing is preserved), and
    pings are forwarded so neither side times the other out.
    """
    u = portal_user(websocket)
    rec = _live_kali(u) if u else None
    if not rec or rec.get("term_port") != port:
        await websocket.close(code=4403)
        return
    await websocket.accept(subprotocol="tty")
    try:
        async with websockets.connect(
            "ws://127.0.0.1:%d/%s" % (port, path),
            subprotocols=["tty"],
            max_size=None,
            ping_interval=None,   # ttyd handles liveness itself
            close_timeout=3,
        ) as upstream:
            stop = asyncio.Event()

            async def client_to_upstream():
                try:
                    while not stop.is_set():
                        msg = await websocket.receive()
                        if msg.get("type") == "websocket.disconnect":
                            break
                        if msg.get("text") is not None:
                            await upstream.send(msg["text"])
                        elif msg.get("bytes") is not None:
                            await upstream.send(msg["bytes"])
                except Exception:
                    pass
                finally:
                    stop.set()

            async def upstream_to_client():
                try:
                    async for m in upstream:
                        if isinstance(m, bytes):
                            await websocket.send_bytes(m)
                        else:
                            await websocket.send_text(m)
                except Exception:
                    pass
                finally:
                    stop.set()

            t1 = asyncio.create_task(client_to_upstream())
            t2 = asyncio.create_task(upstream_to_client())
            await stop.wait()
            for t in (t1, t2):
                t.cancel()
            await asyncio.gather(t1, t2, return_exceptions=True)
    except Exception:
        pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass

@app.get("/__term/{port}/")
@app.get("/__term/{port}/{path:path}")
def term_http(request: Request, port: int, path: str = ""):
    """Serve the ttyd index/assets through our own origin so the cookie applies."""
    u = who(request)
    rec = _live_kali(u)
    if not rec or rec.get("term_port") != port:
        raise HTTPException(403, "not your terminal")
    import httpx
    try:
        r = httpx.get("http://127.0.0.1:%d/%s" % (port, path), timeout=5)
    except Exception as e:
        raise HTTPException(502, "terminal unreachable: %s" % e)
    ct = r.headers.get("content-type", "application/octet-stream")
    body = r.content
    if "text/html" in ct:
        body = body.replace(b'href="/"', ('href="/__term/%d/"' % port).encode())
        body = body.replace(b'src="/', ('src="/__term/%d/' % port).encode())
    return Response(content=body, media_type=ct)

# ---------- flags ----------
class FlagIn(BaseModel):
    flag: str

@app.post("/api/flag")
def api_flag(body: FlagIn, request: Request):
    u = who(request)
    given = (body.flag or "").strip()
    if not given:
        return {"ok": False, "reason": "empty"}
    found = None
    try:
        with open(os.path.join(HERE, "data", "instances.json")) as f:
            raw = json.load(f)
        for k, v in raw.items():
            if v.get("user") == u and hmac.compare_digest(given, v.get("flag") or ""):
                found = v.get("box")
                break
    except Exception:
        pass
    if not found:
        return {"ok": False, "reason": "no match"}
    fresh = progress.award_flag(u, given)
    return {"ok": True, "new": fresh, "box": found,
            "points": progress.points(u, content.MODULES, GAMES)}

@app.get("/api/leaderboard")
def api_leaderboard():
    users = progress.all_users()
    rows = [{"user": un, "points": progress.points(un, content.MODULES, GAMES)} for un in users]
    rows.sort(key=lambda r: -r["points"])
    return {"leaderboard": rows[:50]}

@app.get("/api/progress")
def api_progress(request: Request):
    u = who(request)
    return {"progress": progress.get(u), "points": progress.points(u, content.MODULES, GAMES)}

@app.on_event("startup")
def _startup():
    spawner.start_reaper()
