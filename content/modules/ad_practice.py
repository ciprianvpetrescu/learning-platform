from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "ad-kerberos", "cat": "windows", "title": "Kerberos In Practice",
 "tier": M, "points": 175,
 "summary": "Tickets, service accounts and why one weak password can unravel a domain.",
 "theory": [
  ("The Ticket Dance", "Kerberos avoids sending passwords around the network. You authenticate once to the Key Distribution Centre and receive a Ticket Granting Ticket. To reach a service, you present the TGT and get a service ticket encrypted with that service account's key. The design is elegant; the weakness is that any authenticated user may request a service ticket for any service that has a Service Principal Name registered. Nothing about the request requires you to be authorised for the service, only that you can ask."),
  ("Roasting", "A service ticket is encrypted with the service account's password hash. An attacker who requests one can take it home and crack it offline, at their own pace, without ever touching the domain again. If the service account has a weak password, or worse, if it is a computer account with a predictable password, the ticket falls quickly. The defence is long, random service-account passwords, rotated, and managed accounts whose passwords nobody knows in the first place. If a password is never typed, it cannot be weak."),
  ("Delegation", "Kerberos allows a service to act on your behalf, which is necessary for multi-tier applications and dangerous when granted broadly. Unconstrained delegation lets a compromised host impersonate anyone who authenticates to it, including domain administrators. Constrained delegation narrows this to specific services, and resource-based constrained delegation is narrower still but has its own abuse path when attackers can write to the target's attributes. Every delegation right is a potential privilege escalation and should be inventoried."),
  ("Credential Material On Disk", "Windows caches secrets: LSA secrets, cached domain credentials for offline logon, and in some configurations plaintext or reversible passwords in service configuration. A local administrator on a workstation often yields more than a local administrator's own rights, because the machine holds other people's cached material. The defensive response is tiered administration: domain-admin credentials never log on to machines a lower-privileged user can fully control."),
 ],
 "labs": ["game-kerberos-flow", "game-ad-path"],
 "quiz": [
  {"q": "What does a service ticket give an attacker?", "a": ["Nothing useful", "Material encrypted with the service account key, crackable offline", "Direct admin access", "The user's password"], "c": 1, "why": "Offline cracking means no further contact with the target is needed."},
  {"q": "Why is unconstrained delegation dangerous?", "a": ["It is slow", "A compromised host can impersonate anyone who authenticates to it", "It breaks DNS", "It uses UDP"], "c": 1, "why": "The host captures a usable ticket for every account that connects."},
  {"q": "Best defence for a service account with an SPN?", "a": ["Short password rotated monthly", "Long random password, ideally managed and unknown to humans", "Disable auditing", "Use the same password as the domain admin"], "c": 1, "why": "A password nobody knows cannot be guessed, phished or cracked by familiarity."},
  {"q": "Tiered administration prevents what?", "a": ["Kerberos entirely", "High-value credentials being exposed on low-trust machines", "DNS resolution", "Logging"], "c": 1, "why": "If the credential never touches the machine, the machine cannot leak it."},
 ],
},
{
 "id": "ad-lateral", "cat": "windows", "title": "Lateral Movement & Persistence",
 "tier": H, "points": 200,
 "summary": "How an intrusion spreads through a domain, and how it stays after the noise dies down.",
 "theory": [
  ("Movement Methods", "Remote execution comes in several flavours: service creation, scheduled tasks, WMI, WinRM, remote registry, and the classic PsExec pattern that leaves a service behind. Each has a distinct forensic footprint, and blue teams should know all of them rather than tuning for one. The common thread is that the attacker needs administrative rights on the target and a way to run commands, so restricting who is an administrator where, and preventing credential reuse across machines, removes the path entirely."),
  ("Pass The Hash And Friends", "With a password hash rather than a password you can still authenticate in many configurations, because the protocol accepts the hash as proof. This breaks the assumption that a hash is a safe thing to store. Defences are practical: credential Guard or equivalent features that bind logon to a machine, removing local admin rights so hashes are not harvested in the first place, and monitoring for the technique's characteristic authentications."),
  ("Persistence", "Attackers persist through scheduled tasks, services, WMI event subscriptions, startup folders, registry run keys, and backdoored accounts. The most durable persistence is often the least technical: a service account nobody audits, or a certificate granted long validity for certificate-based authentication. When responding to an intrusion, removing the obvious persistence without understanding the mechanism guarantees a second incident."),
  ("Defensive Posture", "Assume breach, and design so that a single workstation compromise does not equal a domain compromise. Separate administrative accounts from user accounts, never browse or read email as a domain administrator, monitor for the movement techniques, and keep an accurate inventory of privileged accounts and delegation rights. Most intrusions are not sophisticated; they are opportunistic use of misconfiguration that nobody had looked at in years."),
 ],
 "labs": ["game-ad-path", "game-exploit-chain"],
 "quiz": [
  {"q": "What is required for most lateral movement techniques?", "a": ["Physical access", "Administrative rights on the target and a way to execute", "A zero-day", "DNS control"], "c": 1, "why": "Movement is a discipline issue more often than a vulnerability issue."},
  {"q": "Pass the hash works because:", "a": ["Hashes are reversible", "The protocol accepts the hash as authentication proof", "Passwords are stored plainly", "Kerberos is broken"], "c": 1, "why": "The hash becomes a bearer token, so protecting it is as important as protecting the password."},
  {"q": "Which persistence is hardest to notice?", "a": ["A loud scheduled task", "A quietly added service account or long-lived certificate", "A renamed binary", "A startup folder shortcut"], "c": 1, "why": "Accounts and certificates blend into the legitimate baseline."},
  {"q": "Why does removing persistence require understanding it?", "a": ["It does not", "Otherwise the mechanism recreates it and you get a second incident", "To blame someone", "For reporting"], "c": 1, "why": "If the mechanism survives, so does the attacker."},
 ],
},
{
 "id": "ad-hardening", "cat": "windows", "title": "Hardening A Domain",
 "tier": M, "points": 150,
 "summary": "Practical controls that remove whole classes of attack path.",
 "theory": [
  ("Tiered Administration", "Divide accounts and systems into tiers: tier zero is the domain controllers and identity infrastructure, tier one is servers, tier two is workstations and users. Credentials from a higher tier never authenticate to a lower tier. This single discipline removes most realistic domain escalation paths, because the attacker who owns a workstation no longer holds anything that opens the server tier."),
  ("Privilege Hygiene", "Revisit who is an administrator everywhere, and remove standing privilege in favour of just-in-time elevation. Most organisations have far more privileged accounts than they believe, including stale ones belonging to former staff or forgotten service accounts. Inventory them continuously, not once a year, and treat every privileged account as a compromised account waiting for its moment."),
  ("Authentication Controls", "Protect privileged authentication with hardware-backed credentials and machine-bound logon. Disable legacy protocols that cannot enforce strong authentication, because an environment with them enabled can be downgraded to weaker authentication by any client that asks. Enforce the protocol floor rather than trusting clients to choose well."),
  ("Detection And Coverage", "Log the events that matter: privileged group changes, delegation modifications, service account activity, and the authentication patterns that movement produces. Attackers who know log sources are ineffective will target them, so monitor your monitoring. Detection is not a product you install but a hypothesis you keep testing against your own environment."),
 ],
 "labs": ["game-ad-path", "game-alert-triage"],
 "quiz": [
  {"q": "What is tier zero?", "a": ["Workstations", "Domain controllers and identity infrastructure", "Printers", "User laptops"], "c": 1, "why": "Compromising tier zero means compromising the identity system itself."},
  {"q": "Why remove standing privilege?", "a": ["Performance", "A compromised always-admin account is a direct path to everything", "Licensing", "Simplicity"], "c": 1, "why": "Privilege that exists at rest is privilege an attacker can find."},
  {"q": "Why disable legacy authentication protocols?", "a": ["They are slow", "They allow authentication to be downgraded to weaker forms", "They use bandwidth", "They are complex"], "c": 1, "why": "If a weaker path exists, someone will use it, attacker or not."},
  {"q": "Detection is best described as:", "a": ["A product", "A hypothesis continually tested against the environment", "A firewall rule", "A one-time project"], "c": 1, "why": "Coverage decays as the environment changes, so it needs constant validation."},
 ],
},
]
