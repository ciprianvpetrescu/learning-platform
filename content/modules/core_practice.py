from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "net-tls", "cat": "networking", "title": "TLS And Certificates",
 "tier": M, "points": 150,
 "summary": "What the padlock actually asserts, and the failures that look like success.",
 "theory": [
  ("The Handshake In One Breath", "The client and server agree on a cipher suite, the server proves possession of a private key matching a certificate, they derive a shared secret, and everything afterwards is encrypted and integrity-protected. Certificate validation is the part that makes the rest meaningful: without checking that the certificate chains to a trusted authority and matches the name you asked for, you have encryption to an unknown party."),
  ("Where It Breaks", "Expired certificates, hostname mismatches, self-signed certificates that applications were told to ignore, and protocol versions old enough to have practical attacks. A particularly quiet failure is a client library configured to skip verification entirely, often added during debugging and never removed, which produces a working connection and no security at all. The padlock in a browser reflects the browser's configuration, not your application's."),
  ("Downgrade And Stripping", "An attacker positioned on the path can attempt to negotiate a weaker version or strip encryption from a plain request entirely. Defences are straightforward and well supported: enforce a minimum protocol version, prefer forward-secret key exchange so that a future key compromise does not decrypt past traffic, and use transport security headers so a browser refuses to speak plaintext to a host it knows supports encryption."),
  ("Operational Reality", "Certificates expire, and expiry is the most common cause of an outage that looks like a security event. Automate issuance and renewal, monitor for impending expiry well before it bites, and keep the private key where it cannot be casually copied. Treat certificate automation itself as production infrastructure, because the day it fails silently is the day everything does."),
 ],
 "labs": ["game-packet-trace", "game-header-hunt"],
 "quiz": [
  {"q": "What does certificate validation add beyond encryption?", "a": ["Speed", "Assurance you are talking to the party named in the certificate", "Compression", "Caching"], "c": 1, "why": "Without validation you have a private channel to an unidentified endpoint."},
  {"q": "A client set to skip verification produces:", "a": ["An error", "A working connection with no security", "A warning", "Nothing"], "c": 1, "why": "It looks healthy precisely because it never complains."},
  {"q": "Forward secrecy protects against:", "a": ["Phishing", "Future compromise of a long-term key decrypting past traffic", "DDoS", "SQL injection"], "c": 1, "why": "Each session's key is not derivable from the long-term key alone."},
  {"q": "Most common cause of certificate-related outages?", "a": ["Attacks", "Expiry", "Cipher bugs", "DNS"], "c": 1, "why": "Automate renewal and monitor expiry; the maths rarely fails."},
 ],
},
{
 "id": "net-dhcp-arp", "cat": "networking", "title": "Layer Two: ARP, DHCP And Poisoning",
 "tier": M, "points": 150,
 "summary": "The protocols that have no authentication by design, and how networks survive them.",
 "theory": [
  ("ARP Has No Authentication", "A host asking who owns an address will believe whoever answers first. An attacker on the same segment can answer for a gateway and position themselves in the middle of all traffic without touching any routing configuration. This is not a flaw in an implementation; it is the design, and it is why layer two is a trust boundary that deserves the same suspicion as an unauthenticated API."),
  ("DHCP Server Spoofing", "A rogue DHCP server can hand out a default gateway and DNS server of the attacker's choosing, redirecting an entire segment before a single packet leaves the building. The defence is switch-level filtering that permits DHCP responses only from trusted ports, so a workstation cannot answer a broadcast it should only ever listen to."),
  ("Switch And VLAN Hygiene", "VLAN hopping and switch spoofing abuse the negotiation between a host and the switch, letting traffic cross a boundary the network designer believed was enforced. Disable dynamic trunk negotiation on access ports, place unused ports in an unused VLAN, and remember that VLANs are a partitioning tool, not an encryption boundary. Traffic within a VLAN is visible to anyone who can join it."),
  ("Surviving A Shared Segment", "Assume a hostile host on the local network and reduce what that buys the attacker: encrypt at the application layer so interception yields nothing readable, authenticate at the application layer so interception cannot be replayed usefully, and segment so that a compromised segment is not adjacent to the things that matter. On a wireless network this is not hypothetical; it is the default condition."),
 ],
 "labs": ["game-arp-trace", "game-dns-hunt"],
 "quiz": [
  {"q": "Why is ARP poisoning possible?", "a": ["A bug in switches", "ARP has no authentication, so the first answer wins", "Misconfigured DNS", "Weak passwords"], "c": 1, "why": "It is the protocol's design, not an implementation defect."},
  {"q": "A rogue DHCP server can:", "a": ["Only slow the network", "Redirect a segment's gateway and DNS", "Decrypt TLS", "Nothing significant"], "c": 1, "why": "It controls the first hop decisions for every client it serves."},
  {"q": "VLANs provide:", "a": ["Encryption", "Partitioning, not confidentiality", "Authentication", "Integrity"], "c": 1, "why": "Anyone inside the VLAN sees its traffic."},
  {"q": "Best way to survive a hostile segment?", "a": ["Trust the switch", "Encrypt and authenticate at the application layer", "Use a longer password", "Disable DNS"], "c": 1, "why": "Then interception yields nothing usable."},
 ],
},
{
 "id": "blue-hunting", "cat": "blueteam", "title": "Hypothesis-Driven Hunting",
 "tier": H, "points": 200,
 "summary": "Finding what your detections do not cover, before an adversary does.",
 "theory": [
  ("Start From A Technique", "Hunting begins with a specific attacker behaviour and a question: if this happened here, what would remain? That evidence might be a process ancestor, a command-line argument, an authentication pattern, a network destination, or nothing at all because the technique leaves no telemetry in this environment. Discovering that last case is the point, not a failure, because an unknown blind spot is worse than a known one."),
  ("Building The Query", "Write the search assuming no alert exists, because you are trying to prove whether one could. Begin broad enough to see normal activity, then narrow by the characteristics the technique cannot avoid. If your query returns nothing, check the data is actually collected before concluding the activity is absent: the most common hunting finding is a gap in collection rather than a clean environment."),
  ("Turning Findings Into Detection", "A hunt that produces nothing permanent is a one-off. Convert each finding into a detection with a test case, evaluate it against historical data for false positives, and document what it assumes about the environment. Detections decay as systems change, so attach an owner and a review date, otherwise coverage quietly rots back to where it started."),
  ("Measuring Coverage Honestly", "Enumerate the techniques relevant to your environment and mark for each whether you would detect it, would not, or do not know. The honest third category is usually the largest and the most valuable, because it is the list of things that would happen to you invisibly. Attackers do not choose sophisticated methods when simple ones are undetected, so closing the simple gaps first yields more than anything else."),
 ],
 "labs": ["game-alert-triage", "game-log-whodunit", "game-beacon-hunt"],
 "quiz": [
  {"q": "A hunt returns no results. First thing to check?", "a": ["The environment is clean", "Whether the data is actually collected", "The query syntax", "Nothing"], "c": 1, "why": "No evidence of activity is not the same as no activity."},
  {"q": "A hunt is most valuable when it:", "a": ["Ends in a report", "Produces a durable detection with a test case", "Finds nothing", "Runs once"], "c": 1, "why": "Otherwise you have to repeat the work forever."},
  {"q": "The most valuable coverage category is:", "a": ["We would detect it", "We do not know if we would detect it", "We would not detect it", "It does not apply"], "c": 1, "why": "Unknown coverage is where an attacker operates freely."},
  {"q": "Which gaps should be closed first?", "a": ["The most exotic", "The simple ones that are currently undetected", "None", "Only those in audits"], "c": 1, "why": "Adversaries prefer the easiest path, so simple gaps get used first."},
 ],
},
{
 "id": "blue-response", "cat": "blueteam", "title": "Incident Response Discipline",
 "tier": M, "points": 175,
 "summary": "Containment, evidence and the decisions that are made under pressure.",
 "theory": [
  ("Order Of Operations", "Preparation, identification, containment, eradication, recovery, lessons. The temptation under pressure is to jump to eradication, which usually destroys the evidence that would tell you how the attacker entered and whether anyone else is affected. Containment that stops the bleeding while preserving what happened is the hard part, and it should be a rehearsed decision rather than an improvised one."),
  ("Evidence Handling", "Preserve volatile data before it disappears: memory, network connections, running processes and logged-in sessions are gone on reboot. Maintain chain of custody for anything that might reach an investigation or a court, recording who handled it, when and why. A reboot that fixes the symptom often destroys the only record of the mechanism, which is why 'have you tried turning it off' is a poor first response to a security event."),
  ("Communication", "Decide in advance who is told what and who decides. Technical responders need facts, executives need impact and confidence, legal and regulatory obligations may impose deadlines that nobody in the room remembers. Silo the technical work from the speculation, and write down what you know and what you are assuming, because memory is unreliable and the distinction between the two is where most bad decisions originate."),
  ("Learning Without Blame", "A review that identifies a person produces defensiveness and no improvement; a review that identifies the conditions producing the outcome produces change. Ask how the system allowed this, and what would have to be true for it to happen again. Then actually implement those changes and verify them, or the next incident is a repeat with different names."),
 ],
 "labs": ["game-incident-room", "game-evidence-order"],
 "quiz": [
  {"q": "Why not immediately go to eradication?", "a": ["It is slow", "It usually destroys the evidence of how the attacker entered", "It costs money", "It is unprofessional"], "c": 1, "why": "Without the mechanism you cannot know the scope."},
  {"q": "Which data is lost on reboot?", "a": ["Disk contents", "Memory, connections and running processes", "Logs only", "Nothing"], "c": 1, "why": "Volatile evidence is precisely what you need and precisely what disappears."},
  {"q": "Good incident communication separates:", "a": ["Teams", "What is known from what is assumed", "Vendors", "Nothing"], "c": 1, "why": "Confusing the two is where most bad decisions come from."},
  {"q": "A useful post-incident review identifies:", "a": ["The guilty party", "The conditions enabling the outcome", "A scapegoat", "Nothing"], "c": 1, "why": "Blame produces defensiveness; conditions produce change."},
 ],
},
{
 "id": "cloud-identity-practice", "cat": "cloud", "title": "Cloud Identity And Permissions",
 "tier": M, "points": 175,
 "summary": "Roles, policies and how a small permission becomes an account-wide one.",
 "theory": [
  ("Permissions Compose", "Cloud authorisation is a graph: a role can assume other roles, and a policy can allow an action that grants further access. A single overly broad permission, such as the ability to modify policies or pass a role to a service, can be enough to escalate to full control. Reading a policy list is not enough; you have to follow what each permission can reach, which is why automated graph analysis replaced manual review in every environment large enough to matter."),
  ("The Metadata Service", "Cloud instances can usually query an internal endpoint for temporary credentials. Anything that can make an outbound request from the instance may therefore obtain those credentials, which turns a server-side request forgery or a command injection into cloud account access. Modern platforms mitigate with session-token headers and hop limits, and those mitigations only work if they are enforced everywhere rather than available for services that skip them."),
  ("Storage And Buckets", "Object storage misconfiguration is the single most reliable source of public data exposure. A bucket that was briefly public stays public until somebody notices, and search engines and scanners find them constantly. Store access at the object level deliberately, log access, and audit for public exposure continuously rather than as a periodic exercise."),
  ("Least Privilege In Practice", "Grant by workload rather than by convenience, prefer short-lived credentials over long-lived keys, and delete the access key that was created during an experiment three years ago. Establish a way to know which identity performed an action, because an environment without attributable identities cannot be investigated after the fact. Logging control-plane activity is not optional in any account that holds anything you care about."),
 ],
 "labs": ["game-iam-escalate", "game-container-config"],
 "quiz": [
  {"q": "Why is a single permission sometimes enough to escalate?", "a": ["Cloud is insecure", "Permissions compose: one can grant a path to others", "Human error only", "Because of DNS"], "c": 1, "why": "You must follow what a permission can reach, not just what it does."},
  {"q": "Why is the metadata service a target?", "a": ["It is slow", "It returns temporary credentials to anything that can request it", "It stores logs", "It is public"], "c": 1, "why": "A server-side request forgery becomes cloud account access."},
  {"q": "Most reliable source of cloud data exposure?", "a": ["Encryption", "Misconfigured object storage", "Firewalls", "DNS"], "c": 1, "why": "Public buckets persist until someone notices them."},
  {"q": "Why prefer short-lived credentials?", "a": ["Speed", "A key that does not exist cannot be leaked or reused", "Cost", "Simplicity"], "c": 1, "why": "Expiry bounds the value of a stolen credential."},
 ],
},
]
