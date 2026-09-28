# Target catalogue

Every box is defined in `boxes/defs.py` and built from its own directory under
`boxes/`. Flags are random per spawn and always sit at the path the definition
declares. The Kali workstation is not a target — it is the attacker's machine.

## Easy — web fundamentals

| Box | Category | Teaches |
|---|---|---|
| Recruit | web | Directory discovery, a file parameter nobody validated, and injection on a login form |
| Guestbook | web | Stored XSS against a privileged bot, and what a missing HttpOnly flag costs |
| Ledger | web | Object-level authorisation failure (IDOR) in an invoicing app |

## Medium — escalation

| Box | Category | Teaches |
|---|---|---|
| Pamphlet | web | Local file inclusion escalated to remote code execution via log poisoning |
| Fetcher | web | SSRF past a hand-written blocklist, reaching an internal admin service |
| Terminal | web | SQL injection to a shell |

## Harder material

| Box | Category | Teaches |
|---|---|---|
| Elevator | linux | SUID, cron and PATH abuse to root |
| Dockside | cloud | A container that is not as contained as it looks |
| Woodland | windows | Kerberoasting and weak service-account passwords |
| Memory | forensics | Volatility: process injection and a hidden process |
| Autopsy | forensics | Disk images, file carving and a password-protected archive |
| Sample | malware | Static analysis, obfuscation and writing a detection rule |
| Observatory | netsec | Segment-based network lab with a live DNS and admin service |
| Legacy | netsec | A native rebuild of the classic deliberately-vulnerable target |

The lab boxes (`Observatory`) are built from `boxes/network/`, which contains a
real DNS server and admin service rather than canned responses, so enumeration
exercises behave the way they do on a live network.

## Building

Each directory is self-contained:

```bash
docker build -t learn/box-web-easy:latest boxes/web-easy
docker build -t learn/kali:latest       boxes/kali
```

The tag must match `IMAGE_MAP` in `app/spawner.py`. Unbuilt boxes fall back to
plain Debian, which keeps the platform running but makes the box unsolvable — if
a box looks empty, check the image name.

## Adding a box

1. Create `boxes/<name>/` with a `Dockerfile` and an `entrypoint.sh` that writes
   the flag to the declared `flag_path` (read `$FLAG` from the environment).
2. Add a definition to `boxes/defs.py` with category, tier, ports, entry URL,
   hints, skills and flag path.
3. Add the id-to-image mapping to `IMAGE_MAP` in `app/spawner.py`.
4. Build and tag the image.

The catalogue is the single source of truth: the spawner, the API and the front
end all read the same definitions, so a new box needs no UI change.
