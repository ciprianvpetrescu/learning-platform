"""Categories and difficulty tiers."""
F, E, M, H, I = "Fundamental", "Easy", "Medium", "Hard", "Insane"

CATEGORIES = {
 "networking": {"name": "Networking", "icon": "network", "color": "#3b82f6",
   "blurb": "Packets, subnets, routing, switching, DNS, DHCP and the protocols the internet runs on."},
 "linux": {"name": "Linux Fundamentals", "icon": "terminal", "color": "#f59e0b",
   "blurb": "The shell, permissions, processes, services and privilege escalation."},
 "web": {"name": "Web Application Security", "icon": "globe", "color": "#22c55e",
   "blurb": "SQL injection, XSS, LFI, IDOR, SSRF and the OWASP Top Ten."},
 "crypto": {"name": "Cryptography", "icon": "lock", "color": "#a855f7",
   "blurb": "Classical ciphers, hashing, symmetric and asymmetric crypto, TLS, and how they break."},
 "forensics": {"name": "Digital Forensics", "icon": "search", "color": "#ec4899",
   "blurb": "Disk images, memory dumps, file carving, steganography and timeline analysis."},
 "osint": {"name": "OSINT & Reconnaissance", "icon": "radar", "color": "#06b6d4",
   "blurb": "Passive and active information gathering, DNS enumeration and footprinting."},
 "malware": {"name": "Malware Analysis", "icon": "virus", "color": "#ef4444",
   "blurb": "Static and dynamic analysis, obfuscation, C2 detection and YARA rules."},
 "netsec": {"name": "Network Security", "icon": "shield", "color": "#14b8a6",
   "blurb": "Scanning, sniffing, Metasploit, pivoting and firewall evasion."},
 "cloud": {"name": "Cloud & Containers", "icon": "cloud", "color": "#6366f1",
   "blurb": "Docker escapes, Kubernetes misconfiguration, IAM flaws and metadata attacks."},
 "blueteam": {"name": "Blue Team & SOC", "icon": "eye", "color": "#0ea5e9",
   "blurb": "Detection, log analysis, incident response, SIEM queries and threat hunting."},
 "windows": {"name": "Active Directory", "icon": "window", "color": "#eab308",
   "blurb": "Kerberoasting, ASREP, DCSync, BloodHound and lateral movement."},
 "coding": {"name": "Secure Coding", "icon": "code", "color": "#84cc16",
   "blurb": "Input validation, authorisation, secrets handling and dependency hygiene."},
}
