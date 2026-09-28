"""Vulnerable box definitions.

Each box is a Docker container from our own image set, spawned on an isolated
bridge network per user, reachable only from the Kali terminal container on the
same bridge. Flags are per-spawn randomised but derivable from the exploit path.
"""

BOXES = [
 {
  "id": "box-web-easy", "cat": "web", "title": "Recruit", "tier": "Easy", "points": 100,
  "summary": "A small PHP corporate site. Login form, and a file parameter nobody validated.",
  "ports": [80], "flag_path": "/var/www/flag.txt", "entry": "http://TARGET:80/",
  "hints": ["Start with a directory sweep", "The downloads page takes a file parameter", "You do not need credentials for everything"],
  "skills": ["sql injection", "path traversal", "directory discovery"],
  "teaches": "Web app reconnaissance leading to injection and file disclosure.",
  "flag": "/var/www/flag.txt",
 },
 {
  "id": "box-xss", "cat": "web", "title": "Guestbook", "tier": "Easy", "points": 100,
  "summary": "A message board that stores whatever you give it. The admin bot reads every entry.",
  "ports": [80], "entry": "http://TARGET:80/",
  "hints": ["Stored beats reflected when a bot visits", "The bot has a cookie worth having", "No HttpOnly, of course"],
  "skills": ["stored xss", "session theft", "cookie flags"],
  "teaches": "Why stored XSS against a privileged visitor is a session compromise.",
 },
 {
  "id": "box-idor", "cat": "web", "title": "Ledger", "tier": "Easy", "points": 100,
  "summary": "A small invoicing app. You have an account. You would like someone else's.",
  "ports": [80], "entry": "http://TARGET:80/",
  "hints": ["Inspect every request after login", "Identifiers are sequential", "Exports are not access-controlled either"],
  "skills": ["idor", "access control", "api enumeration"],
  "teaches": "Object-level authorisation failures, the most common serious web flaw.",
 },
 {
  "id": "box-lfi", "cat": "web", "title": "Pamphlet", "tier": "Medium", "points": 150,
  "summary": "A CMS with a page loader, a log the server writes to, and a writable upload directory.",
  "ports": [80], "entry": "http://TARGET:80/",
  "hints": ["The page parameter does not check anything", "You can influence the log content", "Session files live somewhere predictable"],
  "skills": ["lfi", "log poisoning", "rce"],
  "teaches": "Local file inclusion escalated to remote code execution.",
 },
 {
  "id": "box-ssrf", "cat": "web", "title": "Fetcher", "tier": "Medium", "points": 150,
  "summary": "A URL preview service with a blocklist that someone wrote by hand.",
  "ports": [80], "entry": "http://TARGET:80/",
  "hints": ["The blocklist matches strings, not destinations", "There is an internal service on 127.0.0.1", "Alternative IP representations exist"],
  "skills": ["ssrf", "filter bypass", "internal enumeration"],
  "teaches": "SSRF reaching an internal admin service.",
 },
 {
  "id": "box-sqli", "cat": "web", "title": "Archive", "tier": "Medium", "points": 175,
  "summary": "A document archive with a search. Error output included, because it is a development build.",
  "ports": [80], "entry": "http://TARGET:80/",
  "hints": ["Errors are visible, so start with union", "There is an admin table", "The database user can write files"],
  "skills": ["sql injection", "union based", "file write to webshell"],
  "teaches": "Union injection through to web shell via INTO OUTFILE.",
 },
 {
  "id": "box-linux-privesc", "cat": "linux", "title": "Bastion", "tier": "Medium", "points": 150,
  "summary": "You land as a low-privilege user over SSH. Root is somewhere above you.",
  "ports": [22, 80], "entry": "ssh user@TARGET",
  "hints": ["Run sudo -l first", "Check for setuid binaries outside the package list", "Someone left a writable script that root runs"],
  "skills": ["enumeration", "sudo abuse", "suid", "cron"],
  "teaches": "Systematic Linux privilege escalation from a user shell.",
 },
 {
  "id": "box-forensics", "cat": "forensics", "title": "Coldcase", "tier": "Medium", "points": 150,
  "summary": "A disk image with deleted files, a hidden archive and timestamps that do not line up.",
  "ports": [], "entry": "Image at /home/analyst/case.dd",
  "hints": ["Carve the unallocated space", "Check metadata on the recovered images", "One archive needs a word from the documents"],
  "skills": ["file carving", "metadata", "timestomping", "archive recovery"],
  "teaches": "Dead disk investigation from image to flag.",
 },
 {
  "id": "box-memory", "cat": "forensics", "title": "Volatile", "tier": "Hard", "points": 200,
  "summary": "A memory image from a suspected compromised workstation. Fileless infection.",
  "ports": [], "entry": "Image at /home/analyst/mem.raw",
  "hints": ["Start with processes that do not exist on disk", "One process has injected memory", "The C2 is in the network artefacts"],
  "skills": ["volatility", "injection detection", "network artefacts"],
  "teaches": "Memory forensics on a fileless compromise.",
 },
 {
  "id": "box-malware-static", "cat": "malware", "title": "Sample", "tier": "Medium", "points": 175,
  "summary": "An unknown binary. Do not run it. Yet.",
  "ports": [], "entry": "Sample at /home/analyst/sample.bin",
  "hints": ["Strings first, always", "The imports tell you capability", "It unpacks at runtime"],
  "skills": ["static analysis", "strings", "pe headers", "capability triage"],
  "teaches": "Understanding a binary without executing it.",
 },
 {
  "id": "box-docker-escape", "cat": "cloud", "title": "Privileged", "tier": "Hard", "points": 225,
  "summary": "You have a shell inside a container. The host is right there.",
  "ports": [22], "entry": "ssh into the container, get out of it",
  "hints": ["Check your capabilities", "Look at the mounts", "Is that socket real"],
  "skills": ["container escape", "capabilities", "host mounts"],
  "teaches": "How a misconfigured container becomes host compromise.",
 },
 {
  "id": "box-kerberoast", "cat": "windows", "title": "Woodland", "tier": "Hard", "points": 225,
  "summary": "A small Windows domain. You have one low-privilege credential.",
  "ports": [445, 88, 389], "entry": "credential provided in the briefing",
  "hints": ["Any user can request a service ticket", "One service account has a weak password", "Follow what that account can reach"],
  "skills": ["kerberoasting", "ad enumeration", "lateral movement"],
  "teaches": "Active Directory attack paths from a single user credential.",
 },
 {
  "id": "box-metasploitable", "cat": "netsec", "title": "Classic", "tier": "Easy", "points": 125,
  "summary": "A deliberately vulnerable host with a long list of services and known exploits.",
  "ports": [21, 22, 80, 139, 445, 3306, 5432, 8180], "entry": "http://TARGET:80/",
  "hints": ["Enumerate every port properly", "There is a known backdoor on one service", "The web app has well-documented flaws"],
  "skills": ["enumeration", "known exploits", "metasploit"],
  "teaches": "Classic exploitation of unpatched services.",
 },
 {
  "id": "box-network-lab", "cat": "networking", "title": "Topology", "tier": "Medium", "points": 175,
  "summary": "A routed lab network: a firewall, two internal segments and a DNS server.",
  "ports": [], "entry": "Lab network, see briefing",
  "hints": ["Map the topology before touching anything", "One segment is reachable through a second interface", "The DNS server will tell you everything if asked"],
  "skills": ["network mapping", "routing", "dns enumeration", "pivoting"],
  "teaches": "Network recon and pivoting across segmented networks.",
 },
]

BY_ID = {b["id"]: b for b in BOXES}
