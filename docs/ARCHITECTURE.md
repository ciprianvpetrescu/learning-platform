# Architecture

## Process

One FastAPI application (`main.py`) serves the front end, the content and game
APIs, the instance spawner endpoints and the WebSocket terminal bridge. It is
a single uvicorn process behind Caddy; Caddy terminates TLS at the edge tunnel
and forwards. There is no worker pool, no queue and no database — progress and
instances are small JSON documents on disk.

## Request paths

```
GET  /                     front end (static/index.html)
GET  /api/me               current user from the portal cookie
GET  /api/catalog          categories + modules + games + boxes for the user
GET  /api/module/{mid}     one module's reading material
POST /api/module/{mid}/quiz      submit a quiz answer
POST /api/module/{mid}/read      mark reading complete
GET  /api/game/{gid}       fetch an exercise (answers stripped)
POST /api/game/{gid}/submit      submit and score
GET  /api/boxes            box catalogue
POST /api/spawn            create an instance (box + Kali on a new bridge)
POST /api/stop             tear an instance down
GET  /api/instances        the caller's live instances
GET  /api/terminal         terminal URL for a live instance
POST /api/flag             submit a captured flag
GET  /api/leaderboard
GET  /api/progress
GET  /__term/{port}/       proxy into ttyd in the user's Kali container
WS   /__term/{port}/{path} WebSocket bridge to ttyd
```

Every route except the static mount and the terminal proxy calls `who(request)`,
which validates the signed `fred_auth` cookie against the shared authportal's
HMAC key. The cookie payload is base64 JSON carrying the username and an expiry;
the signature is the first 32 hex characters of the HMAC-SHA256 over the payload.
Substitution is a one-function change (`portal_user()` in `main.py`) if you run a
different identity provider.

## Spawning a box

The spawner (`app/spawner.py`) does the following on `POST /api/spawn`:

1. Derives a per-user network from the username (`10.66.<uid>.0/24`), determined
   from a stable hash, so a user's boxes always land on their own bridge.
2. Creates the bridge if it does not exist.
3. Starts the target container from the image in `IMAGE_MAP`, attached only to
   that bridge, with a random flag written to the image's flag path at boot.
4. Starts the Kali workstation container on the same bridge and returns its
   published ttyd port.
5. Records the instance in `data/instances.json` under a lock.

A reaper thread runs in the application process and destroys anything older than
one hour (TTL). Every spawn also prunes expired entries.

The bridge is the isolation boundary: the target has no route to the host, to
other users' networks, or to the public internet. The only path in is the Kali
container, which itself is only reachable through the WebSocket proxy in the
application.

## The terminal bridge

The Kali image runs `ttyd` on port 7681 with a wrapper (`boxes/kali/learn-ttyd`)
that carries the theme and font, so the spawner never has to pass quoted JSON on
a command line. The application exposes `/__term/{port}/` as HTTP and
`/__term/{port}/{path}` as a WebSocket; both proxy to `127.0.0.1:<port>` for the
caller's own instance. The port is validated against the caller's instance list
before the proxy is established.

## Grading and flags

Two independent mechanisms:

- **Modules and games** are scored in `app/grader.py`. Quiz answers compare
exactly; input exercises are normalised (numeric answers compare as floats);
builder exercises compare either an ordered list (sequence games) or a single
index (pick-one games).
- **Boxes** carry a flag at a fixed path inside the image. The flag is generated
per spawn as `LEARN{<16 hex>}` and written at container boot, so it is unique
per user and per instance, but the path to it is always the same exploit chain.

Correct flag submission credits points and records progress via
`app/progress.py`. Progress and scores are keyed by portal username.

## Content model

Content is Python, not a database, deliberately: a module is a file, so the
whole curriculum is reviewable in version control and a typo is a commit.

- `content/categories.py` — the twelve categories with presentation metadata.
- `content/modules/*.py` — one file per subject, auto-discovered at import.
  Files beginning with an underscore are skipped, which is the escape hatch for
  work-in-progress material.
- `games/registry.py` — the forty-one exercise definitions. The `kind` field
  tells the front end how to render the exercise.
- `games/banks/` — answer banks, split between JSON data and generated Python.
- `boxes/defs.py` — the box catalogue. Nothing about a box lives anywhere else:
  its image, ports, entry URL, hints, skills and flag path are all here, and
  `IMAGE_MAP` in the spawner is derived from it.

## Failure behaviour

- A box whose image was never built falls back to plain Debian rather than
  failing the spawn, so the platform is never hard-broken by a missing build.
- `box-metasploitable` maps to a native ARM build because the upstream amd64
  image cannot run on ARM hosts.
- If the portal key is unreadable, `portal_user()` returns `None` and every
gated route answers 401 rather than failing open.
