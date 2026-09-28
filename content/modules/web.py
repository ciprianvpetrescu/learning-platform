from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "web-owasp", "cat": "web", "title": "OWASP Top Ten Overview",
 "tier": F, "points": 50,
 "summary": "The ten categories that cover most real-world web vulnerabilities, and how they connect.",
 "theory": [
  ("Why A List At All", "A taxonomy is a memory aid, not a syllabus. The Top Ten groups the failure modes that keep appearing in breach reports: broken access control, injection, insecure design, security misconfiguration, vulnerable components, authentication failures, logging failures. Learn the categories so an unfamiliar application gives you a checklist of questions rather than a blank stare."),
  ("Broken Access Control", "The most common serious flaw and the least glamorous. The application simply fails to check whether you are allowed to do the thing you are doing. Change an identifier and see someone else's record; post to an admin endpoint and it complies; request a page directly and the hidden button turns out to be decoration. Authorisation must be checked server-side, per object, every time, and frequently is not."),
  ("Injection", "Data supplied by the user is interpreted as code by a downstream language: SQL, the shell, an XML parser, a template engine. The fix is separation, not sanitisation. Parameterised queries so the structure is fixed before data binds; argument arrays rather than shell strings; context-aware output encoding. Injection persists because concatenation is easy and the correct API takes two more minutes."),
  ("Misconfiguration And Components", "Default credentials shipped and never changed, directory listing left on, verbose errors exposing stack traces, public buckets, sample applications still installed. Then dependencies: a framework with a known CVE, a Javascript library from 2019, an image with a vulnerable base. Most of what gets exploited was publicly known for months."),
 ],
 "labs": ["box-web-easy", "game-sqli-puzzle"],
 "quiz": [
  {"q": "Which category tops real-world findings most often?", "a": ["Injection", "Broken access control", "Cryptographic failures", "Logging failures"], "c": 1, "why": "Missing or ineffective authorisation accounts for the largest share of serious findings."},
  {"q": "The reliable fix for SQL injection is:", "a": ["Escaping quotes", "Parameterised queries", "Blocking SELECT", "Hiding errors"], "c": 1, "why": "Parameters bind data after structure is fixed, so data can never become syntax."},
  {"q": "A public cloud storage bucket is which category?", "a": ["Injection", "Security misconfiguration", "Broken authentication", "SSRF"], "c": 1, "why": "The capability existed and was left open."},
  {"q": "Why do vulnerable components rank highly?", "a": ["Hard to detect", "Known flaws are documented and often unpatched", "Only old systems", "Need physical access"], "c": 1, "why": "Public exploits circulate, so a version number is often all that is needed."},
 ],
},
{
 "id": "web-sqli", "cat": "web", "title": "SQL Injection",
 "tier": E, "points": 125,
 "summary": "Union, error-based, boolean-blind and time-blind injection, plus using sqlmap properly.",
 "theory": [
  ("The Core Idea", "A query is built by gluing input into SQL. Supply a quote and you break out of the string literal, and the rest of your input parses as SQL. Three questions decide your technique: does the application show query results, does it show database errors, and does its behaviour change with the truth of a condition. Yes, yes, no means union-based. No, yes, no means error-based. No, no, yes means blind."),
  ("Union-Based", "Append a UNION SELECT and match the column count, choosing columns that render on the page. Establish the count with ORDER BY incrementing until it errors, or by unioning increasing nulls. Then read information_schema, list tables, list columns, pull data. The cleanest technique when output reflects."),
  ("Blind Injection", "No output means yes and no questions. Boolean-blind compares responses for AND one equals one against AND one equals two, then extracts character by character with SUBSTRING. Time-blind uses a conditional delay, so slowness means true. Slow but reliable, and sqlmap automates it well."),
  ("Beyond Read", "Injection is not only data theft. With FILE privileges you read server files; with write access and a web directory you drop a web shell and get code execution. Stacked queries allow INSERT, UPDATE, DELETE when the driver permits. MySQL has LOAD_FILE and INTO OUTFILE; Microsoft SQL Server has xp_cmdshell for operating system commands. The impact ceiling is the database account's privileges."),
 ],
 "labs": ["box-web-easy", "game-sqli-puzzle", "lab-sqlmap"],
 "quiz": [
  {"q": "ORDER BY 3 works and 4 errors. What follows?", "a": ["Table has 4 columns", "Query returns 3 columns", "Database is MySQL", "Nothing"], "c": 1, "why": "ORDER BY counts result positions, so the query returns three columns."},
  {"q": "Best technique for no output, no errors, but behaviour changes?", "a": ["Union", "Boolean-blind", "Error-based", "Stacked"], "c": 1, "why": "You only have a true or false signal."},
  {"q": "Which MySQL clause writes results to a server file?", "a": ["LOAD_FILE", "INTO OUTFILE", "EXPORT", "WRITE"], "c": 1, "why": "INTO OUTFILE writes to a path, and a writable web root makes that code execution."},
  {"q": "What does sqlmap --os-shell attempt?", "a": ["Local shell", "Operating system shell via database features", "Schema dump", "Login brute force"], "c": 1, "why": "It abuses xp_cmdshell or file writes to run commands on the host."},
  {"q": "Is escaping quotes an acceptable primary defence?", "a": ["Yes", "No, parameterisation is", "With a WAF", "Only MySQL"], "c": 1, "why": "Escaping is charset and context dependent; parameter binding removes the bug class."},
 ],
},
{
 "id": "web-xss", "cat": "web", "title": "Cross-Site Scripting",
 "tier": E, "points": 125,
 "summary": "Stored, reflected and DOM-based XSS, session theft, and why encoding must be contextual.",
 "theory": [
  ("Three Flavours", "Reflected input comes straight back, so you need a victim to click a link. Stored input is saved and served to everyone viewing the page, which is far more dangerous and needs no social engineering. DOM-based takes attacker-controlled data from the URL and writes it into the page entirely client-side, so the server never sees the payload and no server-side filter can catch it."),
  ("What An Attacker Does With It", "Read the session cookie when it is not HttpOnly and hijack the account. Make authenticated requests as the victim, which defeats CSRF tokens because the request originates in the page. Rewrite the login form to steal credentials. Keylog. Mine the DOM for tokens. In an administrative context, XSS is often the route to full server compromise through the admin's own session."),
  ("Context Matters", "Payloads must be valid where they land. In an element body you open a script tag. In an attribute you close the quote and add an event handler. In a Javascript string you break out with a quote, or use template literals when quotes are filtered. In a URL you may use the javascript scheme. No single generic filter covers all of these, so output encoding must be per context."),
  ("Defence", "Contextual output encoding at render time, from a framework that does it by default rather than hand-rolled escaping. Content Security Policy as defence in depth, restricting inline script so injection struggles to execute. HttpOnly cookies blunt session theft though XSS can still act as the user. Treat innerHTML, document.write and eval as hazards when fed untrusted data."),
 ],
 "labs": ["box-xss", "game-xss-builder"],
 "quiz": [
  {"q": "Which XSS needs no victim to click a link?", "a": ["Reflected", "Stored", "DOM-based", "Self-XSS"], "c": 1, "why": "Stored payloads execute for every viewer of the affected page."},
  {"q": "Payload lands in a single-quoted HTML attribute. First move?", "a": ["Add script tags", "Close the quote and add an event handler", "URL encode", "Add a comment"], "c": 1, "why": "You break the quoting, then introduce an event handler such as onmouseover."},
  {"q": "Does HttpOnly fully prevent XSS impact?", "a": ["Yes", "No, it only blocks cookie theft", "With SameSite", "On modern browsers"], "c": 1, "why": "Script still runs in the victim's session and can make authenticated requests."},
  {"q": "What does CSP provide?", "a": ["Encryption", "Restrictions on what scripts run and from where", "Password policy", "Rate limiting"], "c": 1, "why": "It limits execution and exfiltration even when injection succeeds."},
  {"q": "Which DOM sink is dangerous with untrusted data?", "a": ["textContent", "innerHTML", "innerText", "createTextNode"], "c": 1, "why": "innerHTML parses markup; textContent treats input as text."},
 ],
},
]

MODULES += [
{
 "id": "web-access", "cat": "web", "title": "Access Control, IDOR & Authentication",
 "tier": E, "points": 125,
 "summary": "Horizontal and vertical privilege boundaries, IDOR, session flaws and JWT mistakes.",
 "theory": [
  ("Horizontal And Vertical", "Horizontal escalation means reaching another user's data at your own privilege level: reading the orders of user 1002 by changing an identifier. Vertical means reaching a higher privilege level: a normal user hitting an admin function. Both share one root cause, that the server trusts the client to behave. Tamper with every identifier, path, parameter and header, and request endpoints the interface never showed you."),
  ("IDOR In Practice", "Insecure direct object reference is when an identifier is the only thing between you and someone else's record. Sequential integers, predictable UUID version ones, base64 compound keys and GUIDs leaked elsewhere all fall to it. Look in API paths, download links, invoice and receipt URLs, exported documents, anything taking an id parameter."),
  ("Authentication Failures", "Weak password policy and no lockout enable brute force. User enumeration through differing error messages or response times tells an attacker which accounts exist. Reset flows that leak tokens or email weak ones. Session fixation where the identifier does not change at login. Missing logout invalidation. Remember-me tokens derived from predictable data. Multi-step logins where the second step can simply be skipped."),
  ("JWT Pitfalls", "The algorithm sits in the token header and libraries have historically honoured the header rather than enforcing expectation. Accepting the none algorithm lets you forge tokens trivially. Trusting the key identifier header can point at a file the server will read. Weak HMAC secrets fall to offline cracking. Missing expiry and audience validation mean a stolen token is good forever, anywhere."),
 ],
 "labs": ["box-idor", "game-auth-bypass"],
 "quiz": [
  {"q": "Changing user_id=1042 to 1043 exposes another customer's data. This is:", "a": ["Vertical escalation", "Horizontal escalation or IDOR", "SQL injection", "XSS"], "c": 1, "why": "Reaching a peer's data at your own level is horizontal movement."},
  {"q": "Different errors for bad username and bad password cause what?", "a": ["Good UX", "User enumeration", "Rate limiting", "MFA bypass"], "c": 1, "why": "It confirms which accounts exist before password attacks begin."},
  {"q": "Setting a JWT algorithm to none does what?", "a": ["Encrypts it", "Removes signature verification", "Adds entropy", "Rotates keys"], "c": 1, "why": "If the server honours the header, an unsigned token passes validation."},
  {"q": "Session fixation is fixed by:", "a": ["Longer sessions", "Reissuing the session identifier at login", "Adding CSRF tokens", "Using HTTPS"], "c": 1, "why": "A new identifier on authentication breaks the attacker's pre-set session."},
  {"q": "Why does CSRF not stop an attacker who already has XSS?", "a": ["It does", "The request originates from the page, so tokens are readable and reusable", "Tokens expire", "SameSite blocks it"], "c": 1, "why": "XSS runs same-origin, so it can read the token and issue the request itself."},
 ],
},
{
 "id": "web-lfi", "cat": "web", "title": "File Inclusion, Upload & Traversal",
 "tier": M, "points": 150,
 "summary": "Reading arbitrary files, escaping the web root, and turning uploads into code execution.",
 "theory": [
  ("Traversal", "A parameter like page=about gets concatenated into a filesystem path. Supply enough parent directory sequences and you walk out of the intended directory, then down into etc slash passwd. URL encoding, double encoding and mixed encodings bypass naive filters. Null bytes once terminated strings in older runtimes. If you cannot traverse, consider absolute paths or symlinks already present."),
  ("Local File Inclusion", "When the application includes and executes the file rather than displaying it, traversal becomes inclusion. Reading a configuration file yields credentials. Reading a log file where you have already caused an entry containing PHP code turns inclusion into execution, which is log poisoning. Session files, upload directories and access logs are the favourite targets for exactly this reason."),
  ("Remote File Inclusion", "If the runtime permits including remote URLs, host a payload and point the parameter at it. Modern PHP disables allow_url_include by default, but the bug class appears elsewhere and in templating engines. When RFI works it is usually instant code execution, so test it before investing in escalation."),
  ("Uploads", "An upload checking only the extension, or only the content type header, or only client-side Javascript, is not checked. Bypasses include alternative extensions the server still executes, double extensions, case variation, trailing dot or space, content type spoofing and polyglot files valid as both image and script. If the upload directory is web-accessible and executing, the upload is a web shell. If it is not, look for a filename or path you can influence to write elsewhere."),
 ],
 "labs": ["box-lfi", "game-traversal-hunt"],
 "quiz": [
  {"q": "From /var/www/html/pages/, how do you reach /etc/passwd?", "a": ["../etc/passwd", "../../../../etc/passwd", "/etc/passwd", "%2fetc%2fpasswd"], "c": 1, "why": "Four levels climb out of pages, html, www and var to reach root."},
  {"q": "What is log poisoning for?", "a": ["Hiding traffic", "Getting code into a file you can then include", "Clearing evidence", "Rate limiting"], "c": 1, "why": "You inject code into a log via a request, then include that log to execute it."},
  {"q": "Which is NOT a valid upload bypass?", "a": ["shell.pHp", "shell.php.jpg", "shell.php%00.jpg", "shell.php with correct magic bytes and a real check"], "c": 3, "why": "Content validated against magic bytes plus an allowlist of extensions and a non-executable store is the actual fix."},
  {"q": "Why is an upload directory outside the web root important?", "a": ["It is faster", "Files cannot be requested or executed directly", "It saves space", "It enables HTTPS"], "c": 1, "why": "If it is not reachable by URL and not executed, a stored script is inert."},
 ],
},
{
 "id": "web-ssrf", "cat": "web", "title": "SSRF & Request Forgery",
 "tier": M, "points": 150,
 "summary": "Making the server issue requests on your behalf, reaching internal networks and cloud metadata.",
 "theory": [
  ("The Premise", "The application fetches a URL you supply: a webhook, an image importer, a PDF generator, a URL preview, an XML parser resolving external entities. Because the request comes from the server, it reaches places you cannot: localhost services, internal admin panels, and the cloud instance metadata endpoint. This is the pivot that turns an external web bug into internal network access."),
  ("The Cloud Metadata Target", "Cloud instances expose metadata on a link-local address at 169.254.169.254. Historically this returned temporary credentials for the instance's role with a simple request, which is a full account compromise from a single SSRF. Providers now often require a token header first, but misconfigured or older setups still hand credentials over directly. Internal service discovery, configuration and secrets often live on the same plane."),
  ("Bypassing Filters", "Blocklists are defeated by alternative representations. Decimal, octal and hexadecimal IP forms, IPv6 forms including the mapped IPv4 range, DNS names you control that resolve to internal addresses, redirects from your server to the target, and URL parsing quirks where the filter and the HTTP client disagree about which host is which. A filter that validates the string rather than the resolved destination will lose."),
  ("Blind SSRF", "Often you get no response content, only timing or error differences. That is still enough: port scan internal ranges by response time, detect services by error text, and hit state-changing internal endpoints without reading anything back. Blind SSRF is worth reporting when it can reach an unauthenticated internal admin action."),
 ],
 "labs": ["box-ssrf", "game-ssrf-filter"],
 "quiz": [
  {"q": "What is the classic SSRF target on cloud instances?", "a": ["127.0.0.1:22", "169.254.169.254 metadata", "8.8.8.8", "The CDN"], "c": 1, "why": "The metadata endpoint can return temporary credentials for the instance role."},
  {"q": "Why does SSRF matter more than a normal request?", "a": ["It is faster", "The server's network position reaches internal services you cannot", "It bypasses TLS", "It is anonymous"], "c": 1, "why": "The request originates from the server, inside the trust boundary."},
  {"q": "Which is a valid filter bypass?", "a": ["Blocking 127.0.0.1", "Using the decimal representation of the IP", "Blocking localhost", "Requiring HTTPS"], "c": 1, "why": "Decimal, octal and hex forms resolve to the same address while dodging string matching."},
  {"q": "Best defensive control against SSRF?", "a": ["URL blocklist", "Resolve then validate against an allowlist, and block link-local and loopback", "Disable HTTP", "Add a CAPTCHA"], "c": 1, "why": "Validate the actual destination after resolution, using allowlisting, and deny internal ranges."},
 ],
},
{
 "id": "web-csrf", "cat": "web", "title": "CSRF, CORS & Same-Origin",
 "tier": M, "points": 150,
 "summary": "How browsers decide what a page may do to another origin, and where that trust breaks.",
 "theory": [
  ("Same-Origin Policy", "Two URLs share an origin when scheme, host and port all match. The browser permits reading responses only from your own origin, but it has historically been happy to send requests cross-origin, which is the gap CSRF lives in. Understanding exactly which parts are blocked, requests, reads or cookies, is the difference between a finding and a false positive."),
  ("CSRF", "A state-changing request is triggered from another site, and the victim's cookies ride along automatically. The classic form is an auto-submitting form or an image tag pointed at a state-changing GET. Defences are anti-CSRF tokens bound to the session, SameSite cookies, and checking Origin or Referer. A token that is never validated server-side, or one that is not bound to the session, provides nothing. GET requests must never change state."),
  ("CORS", "Cross-Origin Resource Sharing relaxes the same-origin policy deliberately through response headers. Access-Control-Allow-Origin reflecting the request's Origin is fine only if credentials are not allowed; combined with Access-Control-Allow-Credentials true, it means any site can read authenticated responses. Reflecting Origin with a naive substring check, or trusting a null origin from a sandboxed iframe, are the common mistakes."),
  ("Clickjacking And Framing", "If a page can be framed, it can be overlaid with a transparent layer so the victim clicks a button they cannot see. X-Frame-Options DENY and the CSP frame-ancestors directive are the controls. Frame-busting Javascript is a weaker defence because it can be defeated by sandbox attributes."),
 ],
 "labs": ["game-csrf-forge", "lab-cors-check"],
 "quiz": [
  {"q": "What exactly is an origin?", "a": ["Hostname only", "Scheme, host and port", "IP address", "Domain suffix"], "c": 1, "why": "All three must match; https on 443 and http on 80 are different origins."},
  {"q": "Which cookie attribute most directly mitigates CSRF?", "a": ["HttpOnly", "SameSite", "Secure", "Domain"], "c": 1, "why": "SameSite stops the browser attaching the cookie to genuine cross-site requests."},
  {"q": "Access-Control-Allow-Origin echoing the request Origin with credentials true is:", "a": ["Safe", "A serious flaw allowing any site to read authenticated data", "Required for API use", "Only a problem on HTTP"], "c": 1, "why": "It grants every origin credentialed read access."},
  {"q": "The robust anti-clickjacking control is:", "a": ["Frame-busting script", "X-Frame-Options DENY or CSP frame-ancestors", "Hiding the button", "SameSite cookies"], "c": 1, "why": "Frame-busting can be defeated by sandboxing; the headers cannot."},
 ],
},
]
