# Security posture

This platform teaches offensive security by doing it. The targets are meant to be
broken; the platform around them is not.

## What is deliberately vulnerable

The boxes under `boxes/` contain real vulnerabilities on purpose: SQL injection,
stored XSS, IDOR, LFI, SSRF, SUID and cron misconfiguration, a misconfigured
container, weak service-account passwords, injected processes in memory dumps and
password-protected forensic artefacts. Credentials in those directories (for
example the helpdesk account in the Active Directory box or the backup password
baked into the Linux box's config) are teaching aids inside throwaway containers,
not secrets. They guard nothing outside their own container.

## What protects the host

| control | implementation |
|---|---|
| network isolation | one Docker bridge per user, `10.66.<uid>.0/24`; no host route, no cross-user route |
| instance lifetime | one hour TTL, enforced by a reaper thread |
| authentication | signed `fred_auth` cookie verified independently by the app |
| terminal access | port validated against the caller's own instance list before proxying |
| flag integrity | flags generated per spawn and never sent to the browser |

The application does not pass user input to a shell. The riskiest surface is the
WebSocket terminal proxy, which is why it is scoped to ports the caller already
owns rather than to arbitrary ports.

## Not covered

- **No per-user rate limiting.** A student can spawn as fast as they can click.
- **No resource quotas on containers.** A box that consumes memory affects the
  host. Set `--memory` and `--cpus` in the spawner if the students are not
  trusted.
- **No auditing of terminal sessions.** Commands run inside the container are
  not recorded.
- **Single shared identity.** Any user who can reach the portal can reach every
  box the platform will build for them.

If this is run for anyone other than a trusted group, add container resource
limits and a spawn rate limit first. Both are small, localised changes in
`app/spawner.py`.

## Reporting

The vulnerable targets are the point. A finding in `main.py`, the spawner, the
terminal proxy or the authentication path is a real bug — report it rather than
using it.
