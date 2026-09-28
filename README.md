# learning.simplu.ie

A hands-on cybersecurity academy that runs in a browser. Twelve subject areas,
four hundred quiz and game exercises, and fourteen deliberately vulnerable
machines you can spawn, attack and destroy without installing anything — the
attack workstation is a Kali container in the browser tab next to the target.

Everything is self-hosted. The whole platform is one FastAPI process, a Docker
daemon and a handful of images built from this repository.

## What it is

- **Modules** — twelve categories (Networking, Linux, Web Application Security,
  Cryptography, Digital Forensics, OSINT, Malware Analysis, Network Security,
  Cloud & Containers, Blue Team & SOC, Active Directory, Secure Coding), each
  with reading material, quizzes and practice exercises.
- **Games** — forty-one scored exercises across four interchangeable front-end
  kinds: timed multiple choice, free-text answer, sequence/composition builder,
  and full interactive simulators (a network simulator and a live terminal).
- **Boxes** — fourteen vulnerable targets defined as code. Web exploitation
  (SQL injection, XSS, IDOR, LFI, SSRF), Linux privilege escalation, Docker
  escape, Kerberoasting, memory and disk forensics, a purpose-built network lab,
  and a native rebuild of the classic Metasploitable target.
- **Browser terminal** — each box spawns beside its own Kali container on an
  isolated bridge network. The terminal is served over a WebSocket bridge, so
  the user gets nmap, sqlmap, hydra, gobuster and rockyou from a browser tab.
- **Grading** — flags are randomised per spawn but always derivable from the
  exploit path, so the answer cannot be copied between students.

## Architecture

```
 browser ──► Caddy :18472 ──► FastAPI :8796 ──┬── content/  modules, quizzes, categories
              │  (portal auth)                 ├── games/    exercise definitions + answer banks
              │                                ├── app/spawner.py  docker lifecycle, bridges, reaper
              │                                └── boxes/     target definitions and Dockerfiles
              │
              └── /__term/<port>/ ──► per-user Kali container (ttyd, WebSocket)
```

Each user gets their own Docker bridge, `10.66.<uid>.0/24`. Boxes and the Kali
workstation join it; nothing else can. Instances expire after one hour and a
reaper thread removes them. State lives in `data/instances.json`.

## Running it

The application process:

```bash
python -m venv .venv && . .venv/bin/activate
pip install fastapi uvicorn websockets
uvicorn main:app --host 127.0.0.1 --port 8796
```

Two settings matter before it will serve anything. `main.py` reads the portal
signing key from `AUTHPORTAL` (default `/home/ccc/authportal`) and validates the
signed `fred_auth` cookie on every request; point that at your own auth service,
or replace `portal_user()` with your own session check. The spawner needs write
access to the Docker socket.

The target images are built from `boxes/`:

```bash
docker build -t learn/kali:latest        boxes/kali
docker build -t learn/box-web-easy:latest boxes/web-easy
# ... one per directory; boxes/defs.py maps each box id to its image
```

`app/spawner.py` holds the id-to-image map. A box with no image falls back to
plain Debian rather than failing, and `box-metasploitable` is mapped to a native
build (`boxes/legacy/`) because the upstream amd64 image cannot run on ARM.

## Layout

```
main.py                 FastAPI app: UI, content API, game engine, term bridge
content/                categories and twelve module sets
  categories.py         category metadata (name, icon, colour, blurb)
  modules/*.py          one file per subject, auto-discovered; _-prefixed skipped
games/
  registry.py           41 exercise definitions (kind, points, cat)
  banks/*.json          answer banks per category
  banks/*.py            generated banks (networking, linux)
boxes/
  defs.py               box catalogue: id, category, tier, ports, entry, hints, flag path
  <name>/Dockerfile     one image per target
  kali/                 attack workstation (ttyd + tooling)
app/
  spawner.py            instance lifecycle, per-user bridges, image map, reaper
  grader.py             flag and answer checking
  progress.py           per-user progress and scores
static/                 front end (index.html, app.js, style.css)
data/                   runtime state (gitignored)
```

## Security posture

The vulnerable machines here are deliberately insecure and are meant to be
attacked — that is the product. They are also the only thing on the box that is
insecure. Containers run on isolated per-user bridges with no route to the host
or to each other, instances are time-limited, and the whole platform sits behind
a signed-cookie portal. The application itself does not shell out on user input;
the terminal bridge is a WebSocket proxy to a container that is already running
inside the user's own network namespace.

Credentials and passwords appearing in `boxes/` are intentional teaching
aids inside throwaway containers — they guard nothing outside them.

## Licence

MIT. See LICENSE.
