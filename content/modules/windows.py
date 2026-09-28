from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "win-ad-basics", "cat": "windows", "title": "Active Directory Fundamentals",
 "tier": E, "points": 125,
 "summary": "Domains, forests, OUs, trusts, Group Policy and how authentication actually works.",
 "theory": [
  ("Structure", "A domain is an administrative and authentication boundary; a forest is a collection of domains sharing a schema and a global catalogue. Organisational units arrange objects for delegation and policy, and they are not security boundaries no matter how much they look like folders. Trusts connect domains and forests, and every trust is a path that attackers will follow."),
  ("Authentication", "Kerberos is the default. The client authenticates once to the key distribution centre and receives a ticket-granting ticket. For each service it wants, it presents that ticket and receives a service ticket encrypted with the service account's key. The domain controller holds a copy of every account's secret and is therefore the single most valuable machine in the environment."),
  ("Group Policy", "GPOs apply configuration to users and computers. They can also be abused: a policy that runs a script, or installs software, or sets a scheduled task, applies to everything in scope. Control over a GPO linked to a sensitive OU is equivalent to control over everything in that OU, and often over more through the logon scripts involved."),
  ("The Attacker View", "Enumerate relentlessly: users, groups, computers, sessions, shares, trusts and permissions. Everything authenticates to something, and the relationships between objects are the map. BloodHound collects those relationships and produces a graph where the shortest path from your foothold to domain admin is usually visible in seconds. The complexity that makes AD manageable is the same complexity that makes it attackable."),
 ],
 "labs": ["box-ad-enum", "game-ad-path"],
 "quiz": [
  {"q": "Is an organisational unit a security boundary?", "a": ["Yes", "No, it is for delegation and policy, not isolation", "Only in forests", "Only with GPOs"], "c": 1, "why": "OUs organise administration; they do not contain compromise."},
  {"q": "What holds every account secret in a domain?", "a": ["Each workstation", "The domain controller", "The file server", "The DNS server"], "c": 1, "why": "The KDC holds the keys, which is why it is the primary target."},
  {"q": "The first ticket a Kerberos client obtains is:", "a": ["Service ticket", "Ticket-granting ticket", "Golden ticket", "Silver ticket"], "c": 1, "why": "The TGT is presented to get service tickets, avoiding repeated password entry."},
  {"q": "Why is BloodHound used in AD attacks?", "a": ["Cracking hashes", "Mapping relationships and shortest paths to privilege", "Scanning ports", "Capturing packets"], "c": 1, "why": "It turns object permissions into a graph you can navigate."},
 ],
},
{
 "id": "win-ad-attack", "cat": "windows", "title": "AD Attack Techniques",
 "tier": H, "points": 200,
 "summary": "Kerberoasting, ASREP roasting, delegation abuse, DCSync and lateral movement.",
 "theory": [
  ("Kerberoasting", "Any authenticated user may request a service ticket for any service principal name. The ticket is encrypted with the service account's password-derived key, and it is handed to you. Take it offline and crack it, and if the service account has a weak password and high privilege, you have escalation. It requires no special permissions, which is what makes it so widely applicable."),
  ("ASREP Roasting", "Accounts without pre-authentication enabled will hand out a response encrypted with their own key to anyone who asks. Again, offline cracking. It is rarer than Kerberoasting because it requires that setting, but it works without any credentials at all, which makes it a valuable first step when all you have is network access."),
  ("Delegation", "Kerberos delegation lets a service act on behalf of a user. Unconstrained delegation means the service can impersonate anyone to anything, so coercing a privileged user to authenticate to it hands over their ticket. Constrained delegation limits it to specific services, and resource-based constrained delegation gives the target control over who may delegate to it, which is abusable when you can write that attribute. All three are frequently misconfigured."),
  ("DCSync And Golden Tickets", "DCSync abuses the directory replication protocol. An account with replication rights can request password hashes from a domain controller as though it were another DC, without touching the machine. That is the end of the game: the krbtgt hash lets you forge a ticket-granting ticket valid for anything, and the golden ticket survives password resets of every account except krbtgt itself. Silver tickets forge service tickets for a specific service. Detection relies on watching for replication from hosts that should not be replicating."),
 ],
 "labs": ["box-kerberoast", "game-kerberos-flow"],
 "quiz": [
  {"q": "What is required to perform Kerberoasting?", "a": ["Domain admin", "Any valid domain user account", "Physical access", "A domain controller"], "c": 1, "why": "Any authenticated user may request a ticket for any SPN."},
  {"q": "ASREP roasting works when:", "a": ["Kerberos is disabled", "An account has pre-authentication disabled", "The password is strong", "SMB signing is on"], "c": 1, "why": "Without pre-auth, the KDC returns a crackable response to anyone."},
  {"q": "Unconstrained delegation allows:", "a": ["Reading email", "Impersonating any user who authenticates to that service", "Resetting passwords", "Reading files"], "c": 1, "why": "The service receives and caches tickets for delegating users."},
  {"q": "What does DCSync abuse?", "a": ["SMB", "The directory replication protocol", "LDAP bind", "Kerberos pre-auth"], "c": 1, "why": "It requests replicated secrets as though it were a domain controller."},
  {"q": "Which credential does a golden ticket require?", "a": ["Any user hash", "The krbtgt account hash", "The domain SID only", "A service account hash"], "c": 1, "why": "krbtgt signs ticket-granting tickets, so its key forges anything."},
 ],
},
]
