from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "code-crypto", "cat": "coding", "title": "Cryptography In Application Code",
 "tier": M, "points": 150,
 "summary": "Choosing primitives, storing passwords, and the mistakes that quietly undo both.",
 "theory": [
  ("Never Roll Your Own", "Use a well-reviewed library and its high-level interface. The historical failures are almost never broken mathematics; they are correct algorithms wired up wrongly: a static initialisation vector, a missing integrity check, a key derived from a password with no salt, or a comparison that leaks timing. Choose an authenticated encryption construction so that confidentiality and integrity come together and cannot be separated by accident."),
  ("Password Storage", "Passwords are hashed with a memory-hard, deliberately slow function and a unique random salt per password. A salt stops precomputation from being shared between users; slowness makes each guess expensive. Tune the cost so that a single verification takes a noticeable fraction of a second, and store the parameters alongside the hash so you can raise them later and rehash on next successful login."),
  ("Randomness", "A cryptographically secure random source for anything security-relevant: tokens, session identifiers, salts, keys, reset links. A general-purpose random number generator is seeded predictably and is fine for games and sampling, and catastrophic for secrets. This bug hides well because the code runs and the values look random to a human. If a token is guessable, every control built on it collapses."),
  ("Key Management", "Keys live somewhere and rotation is a design requirement, not an afterthought. Version your keys so old data remains decryptable while new data uses the current key, and plan for the day a key must be revoked. Encrypting data with a key that sits in the same database, next to the ciphertext, protects against almost nothing except a mislaid backup."),
 ],
 "labs": ["game-ecb-detect", "game-hash-crack"],
 "quiz": [
  {"q": "What is a static IV", "a": ["A performance feature", "A serious flaw that leaks patterns between encryptions", "Required by AES", "A synonym for salt"], "c": 1, "why": "Identical plaintexts produce identical ciphertexts, revealing structure."},
  {"q": "Why use a slow password hash?", "a": ["Tradition", "To make each offline guess expensive", "To save space", "To avoid salts"], "c": 1, "why": "Cost per guess is the only lever you have against offline cracking."},
  {"q": "Why must security tokens use a CSPRNG?", "a": ["Speed", "A predictable generator makes tokens guessable", "Portability", "Compression"], "c": 1, "why": "If an attacker can predict the next value, the token is decorative."},
  {"q": "Authenticated encryption gives you:", "a": ["Only confidentiality", "Confidentiality and integrity together", "Only integrity", "Compression"], "c": 1, "why": "Wiring them separately is how integrity checks get forgotten."},
 ],
},
{
 "id": "code-deps", "cat": "coding", "title": "Dependencies & Supply Chain",
 "tier": M, "points": 150,
 "summary": "The code you did not write is still your attack surface.",
 "theory": [
  ("The Real Dependency Graph", "Most applications are mostly other people's code, and the transitive graph is far larger than the direct list. You are responsible for what you ship, not merely for what you chose. Maintain an inventory of exactly what versions are deployed, because you cannot respond to an advisory in a component you cannot name. An inventory that is generated automatically from the build is trustworthy; one maintained by hand drifts immediately."),
  ("Version Pinning And Updates", "Pin exact versions so builds are reproducible, but pinning is not a security strategy on its own: it freezes you at a known-vulnerable version forever if nothing else changes. The workable pattern is pinned builds plus a routine, low-friction path to update, with automated alerts when a dependency you use has a published issue that actually affects your usage."),
  ("Typosquatting And Malicious Packages", "Attackers publish packages with names close to popular ones, or take over abandoned ones, and the payload often runs at install time before any application code executes. Verify the package name character by character, check the publisher and download history, and be cautious about adding a dependency for a task you could do in a few lines. Every dependency is a permanent relationship with a stranger."),
  ("Build Integrity", "The build should be reproducible and the artefact should be traceable to a specific source revision. Sign what you publish and verify what you consume. An attacker who can alter your build pipeline does not need to find a vulnerability in your code at all, and this is why the pipeline is a high-value target and should be treated with the same rigour as production."),
 ],
 "labs": ["game-secure-review"],
 "quiz": [
  {"q": "Why is a dependency inventory essential?", "a": ["Licensing only", "You cannot respond to an advisory in a component you cannot name", "It is required by law", "Performance"], "c": 1, "why": "Incident response starts with knowing what you are running."},
  {"q": "Pinning versions alone:", "a": ["Fixes supply chain risk", "Freezes you at a possibly vulnerable version", "Is illegal", "Improves performance"], "c": 1, "why": "Pinning plus an update path is the workable combination."},
  {"q": "When does a malicious package often execute?", "a": ["Never", "At install time, before application code runs", "Only in production", "Only at build"], "c": 1, "why": "Install hooks run with your privileges, before you ever call the library."},
  {"q": "Why is the build pipeline high value?", "a": ["It is slow", "Altering it compromises every artefact without touching your source", "It uses disk", "It is public"], "c": 1, "why": "One change there reaches every downstream deployment."},
 ],
},
{
 "id": "code-testing", "cat": "coding", "title": "Testing Security Behaviour",
 "tier": H, "points": 175,
 "summary": "Making security properties something the test suite can actually catch.",
 "theory": [
  ("Testing Negative Cases", "Unit tests usually prove that correct input produces correct output. Security lives in the negative space: malformed input, wrong roles, expired sessions, objects belonging to somebody else. A test suite that never asserts a refusal cannot detect a regression that removes one. Write the refusal as explicitly as the success, and treat a disabled authorisation check as a failing build, not a code review comment."),
  ("Regression Tests From Incidents", "Every real vulnerability should leave behind a test that fails without the fix. This turns a one-time lesson into a permanent property and makes the fix verifiable by anyone. It also protects against the common regression where a later refactor reintroduces the flaw because the original reasoning was not captured anywhere durable."),
  ("Automated Analysis", "Static and dynamic scanners, dependency auditing and secret scanning all have high false-positive rates, and that is acceptable if they are wired into the build and triaged rather than ignored. The value is in catching the mechanical issues so human attention goes to the logic ones that tools cannot see. A scanner whose findings nobody reads is worse than no scanner, because it creates the impression of coverage."),
  ("Threat Modelling As Design", "Before writing code, ask what could go wrong, who benefits, and what the system trusts. This is not a ceremony or a document nobody reads; it is a short, honest conversation about trust boundaries that changes the design. Most serious flaws are visible at that stage to someone who is looking, and invisible later to everyone."),
 ],
 "labs": ["game-secure-review", "lab-code-review"],
 "quiz": [
  {"q": "What does a test suite that only checks valid input fail to detect?", "a": ["Performance regressions", "Removal of authorisation refusals", "Syntax errors", "Nothing"], "c": 1, "why": "A refusal that is never asserted can vanish silently."},
  {"q": "Why write a regression test for each real vulnerability?", "a": ["For metrics", "It makes the fix permanent and verifiable", "To blame the author", "It is required"], "c": 1, "why": "The test encodes the lesson somewhere that survives refactoring."},
  {"q": "Scanners are most useful when:", "a": ["Run once", "Wired into the build and actually triaged", "Ignored", "Bought and shelved"], "c": 1, "why": "Unread findings create false confidence rather than safety."},
  {"q": "Threat modelling is valuable because:", "a": ["It is a compliance box", "Most serious flaws are visible at design stage to someone looking", "It replaces testing", "It is fast"], "c": 1, "why": "Design-time decisions are cheap to change and expensive to patch later."},
 ],
},
]
