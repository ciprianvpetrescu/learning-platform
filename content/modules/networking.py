from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "net-fundamentals", "cat": "networking", "title": "Network Fundamentals",
 "tier": F, "points": 50,
 "summary": "The OSI and TCP/IP models, encapsulation, and what actually happens when you load a page.",
 "theory": [
  ("The Two Models", "OSI has seven layers; TCP/IP collapses them into four. For attacking and defending, the useful framing is: link (Ethernet, MAC, ARP), internet (IP, ICMP, routing), transport (TCP, UDP, ports), and application (HTTP, DNS, SMTP). Every tool you will ever use operates at one of these, and knowing which layer a failure lives at tells you what to try next."),
  ("Encapsulation", "When you send data, each layer wraps the one above it. An HTTP request becomes a TCP segment carrying source and destination port and a sequence number; that becomes an IP packet with addresses and a TTL; that becomes an Ethernet frame with MAC addresses; that becomes signals on wire or radio. A packet capture shows all of these at once, which is why Wireshark is confusing until you know which layer you are reading."),
  ("The Life Of A Web Request", "You type a name. The resolver queries DNS, recursively, from root to TLD to authoritative. You get an IP. Your host checks its ARP cache for the destination if it is local, or for the gateway if not. A TCP three-way handshake opens the connection: SYN, SYN-ACK, ACK. The HTTP request goes out and the response comes back. Every stage is a place to be attacked: DNS spoofing, ARP poisoning, TCP reset injection, TLS downgrade."),
  ("Ports And Services", "Ports are 16-bit, 0 to 65535, with well-known services clustering below 1024. Keep these in your head: 21 FTP, 22 SSH, 23 Telnet, 25 SMTP, 53 DNS, 80 HTTP, 110 POP3, 139 and 445 SMB, 1433 MSSQL, 3306 MySQL, 3389 RDP, 5432 PostgreSQL, 8080 alternate HTTP. An open port is a service, a service is code, and code has bugs."),
 ],
 "labs": ["lab-first-scan", "game-packet-trace"],
 "quiz": [
  {"q": "At which OSI layer does a router primarily operate?", "a": ["Layer 2 Data Link", "Layer 3 Network", "Layer 4 Transport", "Layer 7 Application"], "c": 1, "why": "Routers forward based on IP addresses, which live at layer 3."},
  {"q": "Which protocol resolves an IP address to a MAC address locally?", "a": ["DNS", "DHCP", "ARP", "ICMP"], "c": 2, "why": "ARP maps layer 3 addresses to layer 2 within a broadcast domain."},
  {"q": "What is the order of the TCP handshake?", "a": ["ACK, SYN, SYN-ACK", "SYN, SYN-ACK, ACK", "SYN, ACK, SYN-ACK", "SYN-ACK, SYN, ACK"], "c": 1, "why": "Client SYN, server SYN-ACK, client ACK. Three packets, no data yet."},
  {"q": "Port 445 is associated with which service?", "a": ["Telnet", "SMB", "RDP", "MySQL"], "c": 1, "why": "445 is SMB over TCP, Windows file sharing and a perennial attack surface."},
  {"q": "What does a TTL value represent?", "a": ["Connection lifetime", "Maximum hops before a packet is dropped", "DNS cache age", "TLS session length"], "c": 1, "why": "TTL decrements at each hop and drops at zero, generating an ICMP message. Traceroute abuses this deliberately."},
  {"q": "Which is not found in a TCP header?", "a": ["Sequence number", "Window size", "Source IP address", "Flags"], "c": 2, "why": "Source and destination IP live in the IP header; TCP knows only ports, sequence, flags and windows."},
 ],
},
{
 "id": "net-subnetting", "cat": "networking", "title": "IP Addressing & Subnetting",
 "tier": F, "points": 75,
 "summary": "CIDR notation, masks, calculating hosts and ranges. The arithmetic that trips up every interview.",
 "theory": [
  ("Classless Addressing", "An IPv4 address is 32 bits. A CIDR suffix says how many are network bits. Slash twenty-four means 24 network bits and 8 host bits, giving 254 usable addresses. Slash thirty gives 2 usable. The mask is that same count of ones: slash twenty-four is 255.255.255.0."),
  ("The Arithmetic", "To find the network address, AND the address with the mask. To find the broadcast, set every host bit to one. Usable hosts are everything between. Block size is 256 minus the interesting octet of the mask: with slash twenty-six the octet is 192, block size 64, so subnets begin at 0, 64, 128, 192. Drill this until it is instant."),
  ("Private Ranges And NAT", "Ten slash eight, 172.16 through 172.31, and 192.168 slash sixteen are private and not internet routable. NAT rewrites addresses at the boundary. Do not assume that makes internal topology invisible: SSRF and misconfigured proxies reach inside happily."),
 ],
 "labs": ["game-subnet-speedrun"],
 "quiz": [
  {"q": "How many usable hosts in a /29?", "a": ["4", "6", "8", "14"], "c": 1, "why": "Three host bits is 8 addresses, minus network and broadcast leaves 6."},
  {"q": "Subnet mask for a /26?", "a": ["255.255.255.128", "255.255.255.192", "255.255.255.224", "255.255.255.240"], "c": 1, "why": "26 is 24 plus 2, so the last octet is 11000000 binary, which is 192."},
  {"q": "Broadcast address of 192.168.10.0/25?", "a": ["192.168.10.126", "192.168.10.127", "192.168.10.128", "192.168.10.255"], "c": 1, "why": "A /25 covers 0 to 127, so the broadcast is the last address in that half."},
  {"q": "Is 172.20.5.9 private?", "a": ["Yes", "No"], "c": 0, "why": "172.16.0.0 through 172.31.255.255 is a private range."},
  {"q": "Two hosts, 10.0.0.5/30 and 10.0.0.6/30. Same subnet?", "a": ["Yes", "No"], "c": 0, "why": "A /30 spans four addresses; 4 and 5 and 6 and 7 form usable pairs, and .4 to .7 is one block. Both fall in it."},
  {"q": "Which prefix gives exactly 2 usable addresses?", "a": ["/30", "/31", "/32", "/29"], "c": 0, "why": "/30 leaves 2 host bits = 4 addresses, 2 usable. A /31 is point-to-point per RFC 3021 and a /32 is a single host."},
 ],
},
]

MODULES += [
{
 "id": "net-routing", "cat": "networking", "title": "Routing & Switching",
 "tier": E, "points": 100,
 "summary": "Static and dynamic routing, VLANs, spanning tree, and how traffic finds its way.",
 "theory": [
  ("How A Router Decides", "A router holds destination prefixes with next hops and metrics. It picks the longest matching prefix: a slash thirty-two beats a slash twenty-four beats the default route. Ties break on administrative distance, then metric. Predicting this is how you forecast where packets go, and broken routing is a classic way to bypass segmentation."),
  ("VLANs", "A VLAN is a broadcast domain made by configuration rather than wiring. Trunks carry multiple VLANs, tagging frames with a four-byte 802.1Q header. VLAN hopping abuses trunk misconfiguration, by double-tagging frames or by negotiating a trunk from a client port. Segmentation is a security control, and a leaking trunk is where it fails."),
  ("Spanning Tree", "Redundant switch links create loops, and Ethernet has no TTL, so loops become broadcast storms. Spanning Tree elects a root bridge and blocks redundant paths. An attacker who wins the root bridge election funnels all traffic through their machine, which is a bridge to full layer 2 interception."),
  ("Dynamic Routing", "OSPF floods link state within an area; BGP exchanges reachability between autonomous systems and runs the internet. Both trust peers far too much by default. Route injection is real, and accidents have blacked out large portions of the internet more than once."),
 ],
 "labs": ["game-route-diagnose", "lab-routing-tables"],
 "quiz": [
  {"q": "Routes for 10.0.0.0/8 via A and 10.1.0.0/16 via B. Which is used for 10.1.5.1?", "a": ["The /8", "The /16", "Load-balanced", "Dropped"], "c": 1, "why": "Longest prefix match: /16 is more specific than /8."},
  {"q": "What does 802.1Q add to a frame?", "a": ["Encryption", "A four-byte VLAN tag", "Error correction", "A checksum"], "c": 1, "why": "It inserts a tag identifying the VLAN."},
  {"q": "Purpose of Spanning Tree Protocol?", "a": ["Encrypt switch traffic", "Prevent layer 2 loops", "Assign IP addresses", "Route between VLANs"], "c": 1, "why": "STP blocks redundant paths so broadcast storms cannot form."},
  {"q": "Which runs the internet between autonomous systems?", "a": ["OSPF", "RIP", "BGP", "EIGRP"], "c": 2, "why": "BGP is the inter-domain routing protocol of the internet."},
  {"q": "Administrative distance is best described as what?", "a": ["Hops to destination", "Trustworthiness of a route source", "Link bandwidth", "Packet delay"], "c": 1, "why": "It ranks route sources: directly connected beats static beats OSPF beats RIP, and so on."},
 ],
},
{
 "id": "net-dns", "cat": "networking", "title": "DNS, DHCP & Core Services",
 "tier": E, "points": 100,
 "summary": "Name resolution from root to answer, DHCP, and the attacks that target both.",
 "theory": [
  ("Resolution In Detail", "A stub resolver asks a recursive resolver. If nothing is cached, the recursive resolver asks a root server, gets referred to the TLD, gets referred to the authoritative server, and receives the answer with a TTL. Record types: A and AAAA for addresses, CNAME for aliases, MX for mail, TXT for arbitrary text including SPF and DKIM, NS for delegation, PTR for reverse lookups, SOA for zone authority."),
  ("DNS Attacks", "Cache poisoning inserts false records so future queries get wrong answers; the Kaminsky attack brute-forced transaction IDs and source ports to make it practical. DNS tunneling smuggles data out through encoded subdomain queries, which is why detection watches query length and volume. Typosquatting and homographs use visually similar names."),
  ("DHCP", "A client broadcasts DISCOVER, servers reply OFFER, the client sends REQUEST, the server acknowledges. None of it is authenticated. A rogue DHCP server handing out itself as gateway and DNS puts an attacker in the middle of everything without exploiting a single bug. DHCP snooping is the countermeasure."),
  ("Zone Transfers", "AXFR asks a nameserver for the whole zone. It should be restricted and often is not, which hands you a full inventory of an organisation. It remains the easiest real win in external reconnaissance."),
 ],
 "labs": ["lab-dns-recon", "game-dns-hunt"],
 "quiz": [
  {"q": "Which record type maps a name to an IPv6 address?", "a": ["A", "AAAA", "CNAME", "MX"], "c": 1, "why": "AAAA is the IPv6 counterpart of A."},
  {"q": "What does AXFR do?", "a": ["Renews a lease", "Transfers an entire DNS zone", "Pings a nameserver", "Rotates a key"], "c": 1, "why": "Zone transfer, and when unrestricted it dumps every record."},
  {"q": "DHCP message order for a new client?", "a": ["OFFER, DISCOVER, ACK, REQUEST", "DISCOVER, OFFER, REQUEST, ACK", "REQUEST, ACK, DISCOVER, OFFER", "DISCOVER, REQUEST, OFFER, ACK"], "c": 1, "why": "DORA: Discover, Offer, Request, Acknowledge."},
  {"q": "Which TXT record use prevents mail spoofing?", "a": ["DKIM only", "SPF", "PTR", "CAA"], "c": 1, "why": "SPF lists which hosts may send mail for a domain. DKIM signs messages; both help, but SPF is the sender-authorisation record."},
  {"q": "DNS most commonly uses which transport?", "a": ["TCP only", "UDP port 53, with TCP for large responses and transfers", "ICMP", "SCTP"], "c": 1, "why": "Standard queries are UDP; responses over 512 bytes or zone transfers fall back to TCP."},
 ],
},
{
 "id": "net-http", "cat": "networking", "title": "HTTP, TLS & Web Architecture",
 "tier": E, "points": 100,
 "summary": "Requests, responses, cookies, headers, proxies and the TLS handshake.",
 "theory": [
  ("Anatomy Of A Request", "A request line with method and path, a Host header, then headers then an optional body. Methods: GET for retrieval and never for state change, POST to submit, PUT and PATCH to replace and modify, DELETE to remove, OPTIONS to ask what is allowed, HEAD for headers without a body. Status codes: 2xx success, 3xx redirect, 4xx client error, 5xx server error. Learn 200, 301, 302, 400, 401, 403, 404, 405, 500 and they will tell you most of what you need during testing."),
  ("Cookies And Sessions", "The server sets a cookie with Set-Cookie; the browser returns it with every matching request. Session cookies should be HttpOnly so script cannot read them, Secure so they never travel in clear, and SameSite to blunt cross-site requests. A session token that is predictable, unexpiring or not rotated after login is a vulnerability in itself."),
  ("The TLS Handshake", "Client sends ClientHello with supported versions and cipher suites. Server replies ServerHello with its choice and a certificate. The client validates the chain against trusted roots and checks the name matches. They derive shared keys, then exchange Finished messages. From there it is encrypted. Failures worth knowing: expired certs, hostname mismatch, self-signed chains, and version downgrade to something with known breaks."),
  ("Proxies And Caches", "A forward proxy acts for clients; a reverse proxy acts for servers and is where TLS usually terminates, which means it is also where misconfigurations leak headers. Caches return stored responses and cause interesting bugs when they cache something they should not, like an authenticated page or a redirect. Trusting X-Forwarded-For blindly is how IP allowlists get bypassed."),
 ],
 "labs": ["lab-http-inspect", "game-header-hunt"],
 "quiz": [
  {"q": "Which method should never change server state?", "a": ["POST", "GET", "PUT", "DELETE"], "c": 1, "why": "GET is defined as safe and idempotent; breaking that invites CSRF and caching bugs."},
  {"q": "What does HttpOnly on a cookie prevent?", "a": ["Network interception", "JavaScript reading the cookie", "CSRF", "Cookie expiry"], "c": 1, "why": "It hides the cookie from document.cookie, blunting session theft via XSS. It does not stop CSRF."},
  {"q": "401 versus 403?", "a": ["Same thing", "401 not authenticated, 403 authenticated but not permitted", "401 server error, 403 client error", "403 means not found"], "c": 1, "why": "401 means you have not proven who you are; 403 means you have and you still may not."},
  {"q": "What is the first message in a TLS handshake?", "a": ["ServerHello", "ClientHello", "Finished", "Certificate"], "c": 1, "why": "The client speaks first, announcing supported versions and ciphers."},
  {"q": "Which header commonly leaks the backend server technology?", "a": ["Accept", "Server", "Content-Length", "Cache-Control"], "c": 1, "why": "The Server header frequently names the software and version, which saves an attacker work."},
 ],
},
]
