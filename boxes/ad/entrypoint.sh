#!/bin/bash
set +e
python3 /ldap_sim.py &
sleep 2
cat > /briefing.txt <<'EOF'
WOODLAND.LOCAL - Active Directory Attack Paths lab

A simulated directory service is running on this host, port 8080.
It exposes the enumeration and roasting workflow as real HTTP endpoints,
so you walk the reasoning without needing a Windows domain controller.

You have one credential: woodland\a.smith  password Helpdesk123

a.smith is a helpdesk user with GenericWrite over svc_iis.

Endpoints:
  GET /enum/users        list directory users
  GET /enum/spns         list accounts with service principal names
  GET /roast/<account>   request crackable ticket material for a SPN account
  GET /acl               permission relationships (the BloodHound view)
  GET /flag              the objective

Objectives:
 1. Enumerate the directory and find SPN-bearing service accounts.
 2. Kerberoast them, then crack the weak ones offline.
 3. Follow what each cracked account can reach.
 4. Find the unconstrained delegation host.
 5. Reach Domain Admin and collect the flag.

Hints:
  Any authenticated user may request a service ticket. No special rights needed.
  Weak service passwords fall quickly to a targeted wordlist plus rules.
  Unconstrained delegation caches tickets for whoever authenticates to it.
EOF
sleep infinity
