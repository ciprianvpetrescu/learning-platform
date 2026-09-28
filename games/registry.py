"""Game definitions: interactive, scored, category-mapped exercises.

Each game has a `kind` the frontend knows how to render:
  quiz      - multiple choice with timer
  input     - free-text answer, validated server-side
  builder   - assemble a sequence / pick components
  simulator - full interactive lab (networking sim, terminal)
"""

GAMES = [
  # ---- NETWORKING ----
  {
    "id": "game-packet-trace", "cat": "networking", "title": "Packet Trace Puzzle",
    "kind": "builder", "points": 100,
    "blurb": "Order the packets of a TCP session and spot the anomaly.",
    "rounds": 6,
  },
  {
    "id": "game-subnet-speedrun", "cat": "networking", "title": "Subnetting Speedrun",
    "kind": "input", "points": 150,
    "blurb": "Sixty seconds of CIDR arithmetic. Network, broadcast, usable hosts.",
    "seconds": 60,
  },
  {
    "id": "game-route-diagnose", "cat": "networking", "title": "Routing Table Diagnosis",
    "kind": "quiz", "points": 125,
    "blurb": "Given a routing table and a destination, where does the packet go?",
    "rounds": 8,
  },
  {
    "id": "game-dns-hunt", "cat": "networking", "title": "DNS Record Hunt",
    "kind": "input", "points": 125,
    "blurb": "Identify the record type that solves each resolution problem.",
    "seconds": 90,
  },
  {
    "id": "game-header-hunt", "cat": "networking", "title": "HTTP Header Forensics",
    "kind": "quiz", "points": 125,
    "blurb": "Read a raw response and name the technology, the flaw, or the missing control.",
    "rounds": 8,
  },
  # ---- LINUX ----
  {
    "id": "game-cmdline-gauntlet", "cat": "linux", "title": "Command Line Gauntlet",
    "kind": "input", "points": 150,
    "blurb": "Achieve the described effect with the right command. Many answers accepted.",
    "rounds": 10,
  },
  {
    "id": "game-privesc-path", "cat": "linux", "title": "Privilege Escalation Path",
    "kind": "builder", "points": 175,
    "blurb": "Given an enumeration dump, choose the winning escalation path.",
    "rounds": 5,
  },
  {
    "id": "game-log-whodunit", "cat": "linux", "title": "Log Whodunit",
    "kind": "quiz", "points": 150,
    "blurb": "A breach left traces. Read the logs and name the technique.",
    "rounds": 8,
  },
  # ---- WEB ----
  {
    "id": "game-sqli-puzzle", "cat": "web", "title": "SQL Injection Workshop",
    "kind": "input", "points": 175,
    "blurb": "Craft the payload that extracts what the level demands.",
    "rounds": 8,
  },
  {
    "id": "game-xss-builder", "cat": "web", "title": "XSS Payload Builder",
    "kind": "input", "points": 150,
    "blurb": "Break out of the given context with a payload that executes.",
    "rounds": 8,
  },
  {
    "id": "game-traversal-hunt", "cat": "web", "title": "Path Traversal Hunt",
    "kind": "input", "points": 150,
    "blurb": "Reach the file through the filter. Encodings encouraged.",
    "rounds": 8,
  },
  {
    "id": "game-auth-bypass", "cat": "web", "title": "Auth Bypass Challenge",
    "kind": "quiz", "points": 150,
    "blurb": "Identify the authentication flaw in each scenario.",
    "rounds": 8,
  },
  {
    "id": "game-csrf-forge", "cat": "web", "title": "CSRF Forge",
    "kind": "builder", "points": 150,
    "blurb": "Assemble a working cross-site request against the target.",
    "rounds": 5,
  },
  {
    "id": "game-ssrf-filter", "cat": "web", "title": "SSRF Filter Escape",
    "kind": "input", "points": 175,
    "blurb": "Get past the blocklist and reach the metadata service.",
    "rounds": 7,
  },
  # ---- CRYPTO ----
  {
    "id": "game-caesar-crack", "cat": "crypto", "title": "Caesar Cracker",
    "kind": "input", "points": 100,
    "blurb": "Recover the plaintext. Frequency analysis is your friend.",
    "rounds": 6,
  },
  {
    "id": "game-vigenere-break", "cat": "crypto", "title": "Vigenere Cryptanalysis",
    "kind": "input", "points": 150,
    "blurb": "Find the key length, then the key, then the message.",
    "rounds": 5,
  },
  {
    "id": "game-hash-crack", "cat": "crypto", "title": "Hash Identification & Cracking",
    "kind": "input", "points": 150,
    "blurb": "Identify the algorithm, then recover the password.",
    "rounds": 8,
  },
  {
    "id": "game-ecb-detect", "cat": "crypto", "title": "ECB Detection",
    "kind": "quiz", "points": 125,
    "blurb": "Which ciphertext was produced by ECB mode, and why can you tell?",
    "rounds": 6,
  },
  {
    "id": "game-rsa-recover", "cat": "crypto", "title": "Broken RSA Recovery",
    "kind": "input", "points": 200,
    "blurb": "Small modulus, shared prime, or reused nonce. Recover the plaintext.",
    "rounds": 5,
  },
  # ---- FORENSICS ----
  {
    "id": "game-file-carve", "cat": "forensics", "title": "File Carving Challenge",
    "kind": "input", "points": 150,
    "blurb": "Find the hidden file inside the blob and identify its type.",
    "rounds": 6,
  },
  {
    "id": "game-stego-hunt", "cat": "forensics", "title": "Steganography Hunt",
    "kind": "input", "points": 150,
    "blurb": "The flag is hidden in the image. Find it.",
    "rounds": 6,
  },
  {
    "id": "game-evidence-order", "cat": "forensics", "title": "Order of Volatility",
    "kind": "builder", "points": 100,
    "blurb": "Arrange evidence collection in the correct order.",
    "rounds": 5,
  },
  {
    "id": "game-injected-process", "cat": "forensics", "title": "Memory Anomaly Spotter",
    "kind": "quiz", "points": 175,
    "blurb": "Given a process listing, identify the injected or hidden process.",
    "rounds": 6,
  },
  # ---- OSINT ----
  {
    "id": "game-osint-profile", "cat": "osint", "title": "OSINT Profile Build",
    "kind": "quiz", "points": 125,
    "blurb": "Given scattered public data, identify the person, place or technology.",
    "rounds": 8,
  },
  {
    "id": "game-vhost-hunt", "cat": "osint", "title": "Virtual Host Hunt",
    "kind": "input", "points": 150,
    "blurb": "Which Host header value reveals a hidden site?",
    "rounds": 6,
  },
  {
    "id": "game-attack-surface", "cat": "osint", "title": "Attack Surface Ranking",
    "kind": "builder", "points": 150,
    "blurb": "Rank the findings by real-world risk.",
    "rounds": 5,
  },
  # ---- MALWARE ----
  {
    "id": "game-strings-triage", "cat": "malware", "title": "Strings Triage",
    "kind": "input", "points": 150,
    "blurb": "Identify the capability, C2 address or family from the strings dump.",
    "rounds": 7,
  },
  {
    "id": "game-c2-detect", "cat": "malware", "title": "C2 Beacon Detection",
    "kind": "quiz", "points": 150,
    "blurb": "Which host is beaconing, and to where?",
    "rounds": 6,
  },
  {
    "id": "game-rule-tune", "cat": "malware", "title": "Detection Rule Tuning",
    "kind": "builder", "points": 150,
    "blurb": "Fix the noisy rule without breaking detection.",
    "rounds": 5,
  },
  # ---- NETSEC ----
  {
    "id": "game-port-deduce", "cat": "netsec", "title": "Port Scan Deduction",
    "kind": "input", "points": 150,
    "blurb": "Given scan output, identify the service, OS or firewall behaviour.",
    "rounds": 8,
  },
  {
    "id": "game-beacon-hunt", "cat": "netsec", "title": "Beacon Hunt",
    "kind": "quiz", "points": 150,
    "blurb": "Find the periodic callout hiding in quiet traffic.",
    "rounds": 6,
  },
  {
    "id": "game-exploit-chain", "cat": "netsec", "title": "Exploit Chain Assembly",
    "kind": "builder", "points": 200,
    "blurb": "Sequence the steps that turn an open port into a shell.",
    "rounds": 6,
  },
  {
    "id": "game-ids-triage", "cat": "netsec", "title": "IDS Alert Triage",
    "kind": "quiz", "points": 150,
    "blurb": "Real attack or false positive? Decide and prioritise.",
    "rounds": 8,
  },
  # ---- CLOUD ----
  {
    "id": "game-container-config", "cat": "cloud", "title": "Container Config Audit",
    "kind": "quiz", "points": 150,
    "blurb": "Spot the fatal line in each container configuration.",
    "rounds": 8,
  },
  {
    "id": "game-rbac-path", "cat": "cloud", "title": "RBAC Escalation Path",
    "kind": "builder", "points": 175,
    "blurb": "From this service account, reach cluster admin.",
    "rounds": 5,
  },
  {
    "id": "game-iam-escalate", "cat": "cloud", "title": "IAM Escalation",
    "kind": "quiz", "points": 175,
    "blurb": "Given a policy set, find the permission that grants more.",
    "rounds": 7,
  },
  # ---- BLUETEAM ----
  {
    "id": "game-alert-triage", "cat": "blueteam", "title": "Alert Triage Queue",
    "kind": "quiz", "points": 150,
    "blurb": "Twenty alerts, limited time. Prioritise correctly.",
    "rounds": 10,
  },
  {
    "id": "game-incident-room", "cat": "blueteam", "title": "Incident Room",
    "kind": "builder", "points": 175,
    "blurb": "Running incident. Choose the correct next action.",
    "rounds": 8,
  },
  # ---- WINDOWS ----
  {
    "id": "game-ad-path", "cat": "windows", "title": "Shortest Path to Domain Admin",
    "kind": "builder", "points": 225,
    "blurb": "BloodHound output is on the table. Find the path.",
    "rounds": 6,
  },
  {
    "id": "game-kerberos-flow", "cat": "windows", "title": "Kerberos Flow Builder",
    "kind": "builder", "points": 200,
    "blurb": "Assemble the ticket exchange and name the abuse.",
    "rounds": 6,
  },
  # ---- CODING ----
  {
    "id": "game-secure-review", "cat": "coding", "title": "Secure Code Review",
    "kind": "quiz", "points": 150,
    "blurb": "Find the vulnerability in each snippet and pick the real fix.",
    "rounds": 10,
  },
]

BY_ID = {g["id"]: g for g in GAMES}

def by_id(gid):
    return BY_ID.get(gid)

def list_for_category(cat):
    return [g for g in GAMES if g["cat"] == cat]
