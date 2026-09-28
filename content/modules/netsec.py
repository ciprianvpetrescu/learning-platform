from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "netsec-scan", "cat": "netsec", "title": "Scanning & Enumeration with Nmap",
 "tier": E, "points": 100,
 "summary": "Host discovery, port scanning techniques, service and version detection, and NSE scripts.",
 "theory": [
  ("Discovery", "Host discovery decides what is alive before you scan ports. ARP works on the local segment and cannot be blocked by a firewall because it is layer two. ICMP echo is often filtered, so ping sweeps miss hosts. TCP SYN to a common port like 443 is the reliable alternative. Skipping discovery with no-ping is the right move once you know hosts exist."),
  ("Scan Types", "A SYN scan sends a SYN and never completes the handshake, which is fast and quieter than a full connect. A connect scan completes the handshake, which works without raw socket privileges. UDP is slow because there is no handshake, but it finds DNS, SNMP, DHCP and TFTP, which are frequently the interesting services. Null, FIN and XMAS scans set unusual flags and rely on how compliant stacks drop invalid packets, and they are useless against Windows, which ignores the whole technique."),
  ("Detection And Timing", "Version detection probes open ports and matches responses against a signature database. The operating system fingerprint uses TCP/IP stack quirks in initial sequence numbers and window sizes. Timing templates trade speed for noise, with paranoid being glacially slow and insane being fast and loud. Discovery is a journey, not an event, so a broad fast sweep followed by targeted deep scans on what matters is usually correct."),
  ("NSE", "The scripting engine runs Lua scripts for service-specific enumeration: SMB shares and users, HTTP directories and known paths, SSL ciphers and certificate details, database version and configuration. Use the discovery and safe categories by default, add vuln scripts when you have authorisation, and read the source of anything you run, because some scripts are noisier than their name suggests."),
 ],
 "labs": ["lab-first-scan", "game-port-deduce"],
 "quiz": [
  {"q": "Which scan never completes the TCP handshake?", "a": ["Connect scan", "SYN scan", "ACK scan", "UDP scan"], "c": 1, "why": "A SYN scan sends the initial packet and never ACKs, so the connection is never established."},
  {"q": "Why is UDP scanning slow?", "a": ["Encryption", "No handshake, so responses must be inferred from silence and ICMP", "Bandwidth limits", "It is not slow"], "c": 1, "why": "Without a handshake, absence of a reply is ambiguous and requires timeouts."},
  {"q": "Which nmap option enables service and version detection?", "a": ["-sV", "-O", "-sS", "-A only"], "c": 0, "why": "-sV probes and matches banners to signatures. -A bundles that with OS detection and scripts."},
  {"q": "A filtered port means:", "a": ["The service is down", "A firewall is dropping the probes", "The port is open", "The host is offline"], "c": 1, "why": "Filtered means no response arrived, typically from a drop rule."},
  {"q": "Which scan type fails against Windows hosts?", "a": ["SYN", "FIN and XMAS, because Windows ignores the RFC behaviour", "Connect", "UDP"], "c": 1, "why": "Stacks that do not follow the invalid-flag rules report everything closed."},
 ],
},
{
 "id": "netsec-sniff", "cat": "netsec", "title": "Packet Analysis & Sniffing",
 "tier": E, "points": 125,
 "summary": "Capturing traffic, reading protocols, and the layer two attacks that enable interception.",
 "theory": [
  ("Capture Setup", "A switched network only shows you your own traffic, so interception requires either a mirrored port, a tap, or an active layer two attack. Capture filters are applied in the kernel and reduce load before packets are copied; display filters are applied afterwards and are what you actually live in. Capture broadly, filter at analysis time when you are unsure what matters, and capture briefly and precisely when you are not."),
  ("Reading Traffic", "Follow a TCP stream to reconstruct a conversation. Look for credentials in clear text: FTP, Telnet, HTTP basic auth, POP3, SNMP community strings. Look for interesting paths in HTTP, unusual user agents, long POST bodies, and errors that reveal internals. Then look for what should not be happening at all: plaintext protocols that should be encrypted, DNS queries to unexpected domains, and periodic callbacks that suggest beaconing."),
  ("Layer Two Attacks", "ARP has no authentication, so a gratuitous reply claiming to be the gateway poisons everyone's cache and routes traffic through you. MAC flooding overfills a switch's CAM table until it starts flooding all ports. Rogue DHCP servers hand out themselves as gateway. Spanning tree manipulation changes the topology. Every one of these is a real technique and every one has a standard defence: dynamic ARP inspection, port security, DHCP snooping, BPDU guard."),
  ("Encrypted Traffic", "You cannot read TLS content, but metadata survives. Certificate common names and SAN entries reveal the service. Server name indication leaks the hostname. Traffic volume and timing reveal behaviour, and packet sizes can distinguish a file transfer from interactive typing. Beaconing is detectable by the regularity of the intervals alone, regardless of payload."),
 ],
 "labs": ["lab-pcap-read", "game-beacon-hunt"],
 "quiz": [
  {"q": "What is ARP poisoning for?", "a": ["Encryption", "Intercepting traffic by lying about MAC-to-IP mappings", "Port scanning", "Password cracking"], "c": 1, "why": "Forged ARP replies redirect traffic through the attacker's machine."},
  {"q": "Which protocol sends credentials in clear text?", "a": ["SSH", "HTTPS", "Telnet", "TLS"], "c": 2, "why": "Telnet has no encryption whatsoever, which is why it was replaced by SSH."},
  {"q": "You cannot read TLS payload, but you can still learn:", "a": ["Nothing", "Hostnames from SNI and certificate metadata, plus timing and volume patterns", "Passwords", "File contents"], "c": 1, "why": "Metadata is largely unencrypted and highly informative."},
  {"q": "What does MAC flooding achieve?", "a": ["Faster switching", "Overflows the CAM table so the switch floods all ports", "Encryption", "QoS"], "c": 1, "why": "With no table entries, the switch behaves like a hub and traffic is visible everywhere."},
 ],
},
{
 "id": "netsec-exploit", "cat": "netsec", "title": "Exploitation & Metasploit",
 "tier": M, "points": 150,
 "summary": "Vulnerability research, exploit selection, payloads, shells and post-exploitation.",
 "theory": [
  ("From Finding To Working Exploit", "A version number is a hypothesis, not a finding. Confirm the vulnerability actually triggers, check for prerequisites like a specific configuration or a reachable path, and understand what the exploit does before running it, because some are destructive or unstable. Reproducing the issue manually even after an exploit succeeds teaches you what to look for next time without automation."),
  ("Metasploit Workflow", "Search for a module, read the options, set the target, set the payload and check the defaults, then run it in a background job and interact. Reverse shells usually beat bind shells, because outbound connections are allowed through more firewalls than inbound. Modern installations prefer staged payloads that fetch the rest after the initial foothold, which keeps the first stage small."),
  ("Shells And TTY", "A basic shell has no job control, no tab completion and an unreliable Ctrl-C, which makes it miserable to work in. Upgrading to a proper TTY fixes that and is usually the first thing to do. On Linux with Python available, a one-liner spawning a pty gives a real terminal. On Windows, plenty of alternatives exist. Persistence, privilege escalation and lateral movement all get easier once the shell is comfortable."),
  ("Reliability", "Exploit code is written by people against one specific environment and rarely covers every variant. When an exploit fails, read the error rather than rerunning it. Check target architecture, encoding, path assumptions, and whether the service is running the expected version. A failed exploit that crashed the service is a loud mistake, which is why testing against your own replica first is standard practice."),
 ],
 "labs": ["box-metasploitable", "game-exploit-chain"],
 "quiz": [
  {"q": "Why prefer a reverse shell?", "a": ["Faster", "Outbound connections traverse more firewalls than inbound", "Encrypted", "Stealthier"], "c": 1, "why": "The target connects out, which egress rules usually permit."},
  {"q": "First thing after getting a bare shell?", "a": ["Run nmap", "Upgrade to a full TTY", "Start cracking", "Exfiltrate data"], "c": 1, "why": "A proper terminal makes everything afterwards work correctly."},
  {"q": "What does a staged payload do?", "a": ["Runs everything at once", "Sends a small first stage that fetches the rest", "Avoids antivirus", "Encrypts traffic"], "c": 1, "why": "Keeping the initial payload small improves delivery reliability."},
  {"q": "Exploitation without understanding means:", "a": ["Faster results", "You cannot adapt when it fails or explain the impact", "Better stealth", "Higher reliability"], "c": 1, "why": "The tool breaks on the first variation and you have nothing to fall back on."},
 ],
},
{
 "id": "netsec-firewall", "cat": "netsec", "title": "Firewalls, IDS & Evasion",
 "tier": M, "points": 150,
 "summary": "How filtering works, how detection works, and what actually gets past both.",
 "theory": [
  ("Stateless And Stateful", "A stateless filter evaluates each packet against rules with no memory of prior packets, so allowing established return traffic means allowing all traffic in that direction. A stateful firewall tracks connections and permits replies to outbound requests automatically. Beyond that, a next-generation device inspects application content, which defeats the port-hopping trick of running a service on eighty to look like the web."),
  ("Rules And Order", "Firewalls evaluate rules in order and stop at the first match, so a permissive rule above a restrictive one makes the restrictive one irrelevant. The default policy at the bottom decides everything not matched. Default-deny is correct and painful; default-allow is common and dangerous. Auditing rule order is usually more productive than hunting for exotic bypasses."),
  ("IDS And IPS", "An IDS detects and alerts, an IPS sits inline and blocks. Signature detection matches known patterns and misses anything new; anomaly detection flags deviation from a baseline and produces false positives that erode trust; behaviour detection models attacker patterns and is the current state of the art. Evasion techniques target the parsing differences between the detection engine and the destination: fragmentation, overlapping segments, encoding, and TCP-level manipulation, so what the sensor sees differs from what the target reassembles."),
  ("Evasion Realities", "Scanning slowly and from multiple sources, using legitimate protocols for exfiltration, and blending into normal traffic patterns beat most technical evasion. Encrypted channels, allowed services and off-hours activity all reduce suspicion. Detection depends on the defender having the telemetry and the time, and the practical goal of evasion is to look unremarkable rather than to be invisible."),
 ],
 "labs": ["game-ids-triage", "lab-firewall-audit"],
 "quiz": [
  {"q": "How do firewalls evaluate rules?", "a": ["Lowest priority wins", "First match wins, top to bottom", "Randomly", "By specificity always"], "c": 1, "why": "Ordering is everything; a broad allow above a deny makes the deny dead code."},
  {"q": "The difference between IDS and IPS:", "a": ["None", "IDS alerts, IPS sits inline and blocks", "IPS is software only", "IDS encrypts traffic"], "c": 1, "why": "Prevention requires being in the path."},
  {"q": "Which is a classic IDS evasion technique?", "a": ["Using HTTPS", "Packet fragmentation so the sensor reassembles differently than the target", "Open ports", "Syn scanning"], "c": 1, "why": "Parsing differences are exploited so the sensor sees something harmless."},
  {"q": "Why does signature detection miss new attacks?", "a": ["Too slow", "No signature exists yet for something never seen", "Needs a GPU", "It does not"], "c": 1, "why": "Matching requires prior knowledge of the pattern."},
 ],
},
]
