#!/bin/bash
set +e
mkdir -p /opt/lab
pkill -f systemd-resolved 2>/dev/null
printf 'nameserver 127.0.0.1\n' > /etc/resolv.conf
python3 /opt/lab/dnsserver.py 2>/tmp/dns.err &
sleep 2
python3 /opt/lab/adminsvc.py 2>/tmp/adm.err &
sleep 1
cat > /opt/lab/README <<'EOF'
NETWORK LAB

A DNS server runs on this host. An internal admin service answers on 8080.

Objectives:
 1. Discover the DNS service and query for lab.internal.
 2. Request a zone transfer. It is not restricted.
 3. Read every internal hostname, and the TXT records on flag.lab.internal.
 4. Use the API token from the TXT record to fetch the flag.

Hints:
  dig router.lab.internal @127.0.0.1
  dig AXFR lab.internal @127.0.0.1     (note: AXFR is TCP)
  curl 'http://127.0.0.1:8080/flag?token=...'
EOF
sleep infinity
