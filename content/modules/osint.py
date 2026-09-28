from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "osint-passive", "cat": "osint", "title": "Passive Reconnaissance",
 "tier": F, "points": 75,
 "summary": "Gathering intelligence without touching the target, from certificates, DNS and public records.",
 "theory": [
  ("Why Passive First", "Anything you send to the target's infrastructure is visible to them. Passive reconnaissance uses third parties who already collected the data, so nothing touches the target and nothing appears in their logs. It is slower, and it is far safer. Start here, always."),
  ("Certificate Transparency", "Every publicly trusted certificate is logged by design. Querying those logs yields every hostname an organisation has ever requested a certificate for, including internal-sounding names, staging environments, and services that never appeared in any DNS record. This single source is responsible for a large share of accidental exposure discoveries."),
  ("DNS And Registration", "Historical DNS records show what used to point where, which reveals forgotten infrastructure. Registration data gives names, contact details and sometimes the technical contact's personal address. Zone transfers, when permitted, hand over the entire zone. Shodan and Censys index what services are actually exposed, and their historical data shows services that have since been closed."),
  ("People And Documents", "Job postings name the technologies in use. Conference talks and presentations name the architecture. Code repositories leak credentials, internal hostnames and configuration far more often than organisations believe. Social media reveals reporting structures, holiday schedules and technology preferences through what people casually mention. Metadata in published documents, written by the person who authored them, includes usernames and software versions."),
 ],
 "labs": ["lab-ct-recon", "game-osint-profile"],
 "quiz": [
  {"q": "Why start with passive reconnaissance?", "a": ["It is faster", "It never touches the target and leaves no trace in their logs", "It needs no tools", "It is more accurate"], "c": 1, "why": "You rely on third-party data that already exists."},
  {"q": "Which source reveals hostnames that never appear in DNS?", "a": ["Whois", "Certificate Transparency logs", "Shodan", "The Wayback Machine"], "c": 1, "why": "Every publicly trusted certificate is logged, including for internal-sounding names."},
  {"q": "A job advert is useful because:", "a": ["It gives a contact", "It names technologies and versions in use", "It reveals passwords", "It is always accurate"], "c": 1, "why": "Recruitment posts describe the stack in detail."},
  {"q": "What is OSINT in one sentence?", "a": ["Scanning with nmap", "Intelligence from publicly available sources", "Breaking passwords", "Exploit development"], "c": 1, "why": "It is collection and analysis of information that is already public."},
 ],
},
{
 "id": "osint-active", "cat": "osint", "title": "Active Enumeration",
 "tier": E, "points": 125,
 "summary": "DNS brute force, virtual host discovery, directory busting and service fingerprinting.",
 "theory": [
  ("Subdomain Enumeration", "Wordlists plus DNS resolution finds names that never appeared elsewhere. Tools differ in how they ask: some resolve directly, some use multiple public resolvers, some use passive sources and permutation engines. Combine them and deduplicate, because each misses things the others find. A wildcard record complicates everything, so check for one first and filter accordingly."),
  ("Virtual Hosts", "Many web servers host dozens of sites on one address, selected by the Host header. Sending a nonexistent Host and getting a default page tells you they exist. Fuzzing the Host header against a wordlist finds them, and virtual hosts are frequently less hardened than the main site because nobody remembers they are there."),
  ("Content Discovery", "Directory and file discovery with a wordlist finds admin panels, backups, configuration files, source maps and forgotten installers. Status codes matter: two hundred is a hit, three-oh-one and three-oh-two reveal a redirect, four-oh-one and four-oh-three prove existence without access, and a consistent custom four-oh-four versus a generic one distinguishes real routing. Recursive discovery on each hit extends the map."),
  ("Fingerprinting", "Banner grabbing, TLS certificate details, favicon hashes, HTTP header ordering and error page formats all reveal the technology and often the version. Version matters because it maps to public vulnerabilities. Do not rely on a single signal, since any of them can be spoofed or rewritten by a proxy."),
 ],
 "labs": ["lab-subdomain-enum", "game-vhost-hunt"],
 "quiz": [
  {"q": "Why check for a wildcard DNS record before brute forcing?", "a": ["Speed", "Every name resolves, producing false positives", "It blocks queries", "It reveals the zone"], "c": 1, "why": "A wildcard makes every guess look successful, so results must be filtered."},
  {"q": "How do you discover virtual hosts on one IP?", "a": ["Port scan", "Fuzz the Host header with a wordlist", "Ping", "Traceroute"], "c": 1, "why": "The server selects a site by the Host header value."},
  {"q": "A 401 response during directory discovery tells you:", "a": ["The path does not exist", "The path exists but requires authentication", "Rate limited", "Server error"], "c": 1, "why": "Existence is confirmed even though access is refused."},
  {"q": "Why fingerprint service versions?", "a": ["To look professional", "Versions map to known vulnerabilities", "To speed the scan", "To avoid detection"], "c": 1, "why": "A version string is often enough to select a public exploit."},
 ],
},
{
 "id": "osint-footprint", "cat": "osint", "title": "Attack Surface & OPSEC",
 "tier": M, "points": 125,
 "summary": "Mapping everything reachable, prioritising it, and not getting yourself caught doing it.",
 "theory": [
  ("Building The Map", "Combine every source into one inventory: domains, subdomains, IP ranges, cloud tenants, exposed services, mobile apps, APIs, and third-party integrations. Organisations do not have one attack surface, they have the sum of everything their suppliers run on their behalf. The forgotten marketing microsite from four years ago is the one that falls."),
  ("Prioritisation", "Score by exposure, exploitability and impact. An unauthenticated service with a public exploit facing the internet outranks an authenticated bug deep in an internal tool, no matter which is more intellectually satisfying. Ask what an attacker would actually use to get to the data, and work backwards from the data."),
  ("Operational Security", "Use infrastructure that is not attributable to you or your client. Rate-limit your own scanning, because volume is what triggers blocking and alerts. Understand that DNS queries, TLS handshakes and HTTP requests are all visible to the target and their providers. Keep a record of what you sent and when, both for your report and in case you are accused of something you did not do."),
  ("Scope Discipline", "Written authorisation defines what you may touch. A domain implies subdomains only if stated. A cloud tenant is not implicit. Third-party services are almost never in scope. Testing outside scope is not a mistake you can explain away afterwards, and the ability to say no to an interesting target outside scope is a professional skill."),
 ],
 "labs": ["game-attack-surface", "lab-scope-check"],
 "quiz": [
  {"q": "What belongs in an attack surface inventory?", "a": ["Owned domains only", "Every reachable asset including third parties acting for the organisation", "Only internet-facing servers", "Only what the client lists"], "c": 1, "why": "Suppliers and forgotten microsites are part of the real surface."},
  {"q": "Which finding is usually higher priority?", "a": ["Authenticated bug in an internal tool", "Unauthenticated internet-facing bug with a public exploit", "Missing security header", "Verbose error page"], "c": 1, "why": "Reachability and exploitability dominate."},
  {"q": "Why rate-limit your own scanning?", "a": ["Politeness", "Volume triggers detection, blocking and alerts", "Speed", "Accuracy"], "c": 1, "why": "Bursty high-volume activity is the loudest thing you can do."},
  {"q": "You find a related domain not listed in scope. You should:", "a": ["Test it anyway", "Report it and ask, but do not test", "Ignore it forever", "Post it publicly"], "c": 1, "why": "Scope is a legal boundary, and discovering more is a finding in itself."},
 ],
},
]
