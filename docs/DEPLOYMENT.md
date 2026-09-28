# Deployment

## Components

| piece | detail |
|---|---|
| application | uvicorn, `main:app`, 127.0.0.1:8796 |
| reverse proxy | Caddy listener on 18472, portal-gated |
| portal | shared authportal, 127.0.0.1:9443, signed `fred_auth` cookie |
| edge | Cloudflare tunnel ingress -> localhost:18472 |
| runtime | Docker daemon, images from `boxes/` |

## systemd

```ini
[Unit]
Description=learning.simplu.ie
After=network.target docker.service

[Service]
WorkingDirectory=/opt/apps/learn
ExecStart=/opt/apps/learn/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8796
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

## Caddy

```
http://:18472 {
    forward_auth 127.0.0.1:9443 {
        uri /verify
        copy_headers X-Auth-User
    }
    reverse_proxy 127.0.0.1:8796
}
```

Caddy is the authentication gate and the application independently verifies the
same cookie, so a misrouted request does not become an unauthenticated one.

## Cloudflare

Three things are required for a new hostname on a shared zone, in this order:

1. A proxied DNS record pointing at the tunnel.
2. An ingress rule in the tunnel configuration pointing at `localhost:18472`.
3. An entry in any firewall allowlist rule that whitelists known hostnames.

Miss the third and the edge answers 403 before the request ever reaches the
server.

## Docker

The application process must be able to reach the Docker socket to create
bridges and containers. It is not exposed over TCP and the port is not published
beyond loopback; the terminal reaches containers through the application's
WebSocket proxy.

Images are built once and tagged to match `IMAGE_MAP` in `app/spawner.py`.
A missing image is not fatal — the spawner falls back to plain Debian — but the
box will be unsolvable, so verify the tag after any rebuild.

## Disk hygiene

A long-running instance accumulates dangling images and build cache. Prune
periodically:

```bash
docker image prune -f
docker builder prune -f
```

Instances themselves are reaped automatically after one hour.

## Changing the port

Nothing binds port 18480 on the host; pick a listener that is free. Two services
on the same port will take the whole proxy down, not just the new site.
