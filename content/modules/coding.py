from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "code-input", "cat": "coding", "title": "Input Validation & Safe APIs",
 "tier": E, "points": 100,
 "summary": "Why validation is not sanitisation, and the APIs that remove whole bug classes.",
 "theory": [
  ("Validate, Do Not Sanitise", "Validation rejects input that does not meet an expectation. Sanitisation attempts to clean bad input into good input, and it fails in edge cases you did not imagine. Prefer strict allowlisting: an email field accepts an email shape, an integer field accepts digits, a country field accepts one of the known codes. Anything that does not match is rejected outright, and the error says nothing useful to an attacker."),
  ("Safe By Construction", "Parameterised queries, prepared statements, template engines with autoescaping, argument arrays instead of shell strings, safe parsers instead of regular expressions for structured data. These make the vulnerability unreachable rather than filtered. The distinction matters: filtering is a control you can get wrong, whereas an API that has no string-concatenation path cannot be wrong in that way at all."),
  ("Encoding At The Boundary", "Output encoding must match the context: HTML entity encoding in markup, JavaScript escaping in script, URL encoding in parameters, CSS escaping in styles, and correctly parameterised SQL. Encode on output, not on input, and always at the final boundary. Storing encoded data is a mistake because the same value may be needed in several contexts."),
  ("Errors And Logging", "Users get generic messages; logs get detail. Stack traces, database errors and internal paths in a response are free reconnaissance, and they frequently leak data through the error itself. Log security-relevant events with enough context to investigate, but never log credentials, tokens or full card numbers. If in doubt about a field, log a hash or a suffix, not the value."),
 ],
 "labs": ["game-sqli-puzzle", "lab-code-review"],
 "quiz": [
  {"q": "Validation versus sanitisation:", "a": ["The same thing", "Validation rejects, sanitisation attempts to clean, and rejection is safer", "Sanitisation is always better", "Neither matters"], "c": 1, "why": "Cleaning tries to be clever and fails in corners; rejecting is unambiguous."},
  {"q": "Which approach removes SQL injection entirely?", "a": ["Escaping", "Parameterised queries", "WAF", "Input length limits"], "c": 1, "why": "Parameters separate structure from data at the protocol level."},
  {"q": "When should output encoding happen?", "a": ["On input", "On output, at the boundary, per context", "At storage", "Never"], "c": 1, "why": "The same value used in HTML and JavaScript needs different encodings."},
  {"q": "What should an error page reveal to the user?", "a": ["The stack trace", "A generic message, with detail going only to logs", "The database schema", "The framework version"], "c": 1, "why": "Verbose errors hand over reconnaissance for free."},
 ],
},
{
 "id": "code-authz", "cat": "coding", "title": "Authorisation & Session Design",
 "tier": M, "points": 150,
 "summary": "Deny by default, check per object, and design sessions that survive contact with reality.",
 "theory": [
  ("Deny By Default", "Every request is refused unless it matches an explicit allowance. This inverts the common mistake of allowing unless a specific forbidden case is matched, which fails the moment an endpoint is added. Centralise the check rather than scattering it through controllers, because scattered checks are missed exactly where nobody looked. Framework-level enforcement with explicit exceptions is the pattern that holds."),
  ("Per Object, Not Per Page", "Authenticating the user is not authorising the action. Every request that touches an object must verify that this user may touch this object, every single time, server-side. The check belongs next to the data access, not in the user interface, because the interface is a suggestion and the API is the truth. Never trust an identifier, role or user ID supplied by the client for an authorisation decision."),
  ("Session Design", "Issue a new session identifier at login to prevent fixation. Expire idle sessions and absolute sessions. Invalidate server-side on logout rather than merely clearing the cookie, and invalidate everywhere when a password changes. Store only an opaque reference in the cookie, never a serialised user object, because the client can read what you put there. Rotate secrets on privilege change."),
  ("Secrets", "Never commit them. Environment variables loaded at runtime, a managed secret store, or an encrypted configuration, and in no case a file in the repository, even a private one, even for a moment, because history is forever and repositories get cloned. Rotate on any suspicion of exposure, and audit what the application actually needs so the blast radius is small."),
 ],
 "labs": ["lab-authz-review", "game-auth-bypass"],
 "quiz": [
  {"q": "Where must authorisation be enforced?", "a": ["Client-side", "Server-side, per object, on every request", "In the database only", "In the WAF"], "c": 1, "why": "Anything the client enforces can be bypassed by the client."},
  {"q": "Why reissue the session identifier at login?", "a": ["Performance", "To prevent session fixation", "Encryption", "Caching"], "c": 1, "why": "An attacker-set identifier becomes useless once it is replaced."},
  {"q": "What should a session cookie contain?", "a": ["The serialised user object", "An opaque reference to server-side state", "The password hash", "The role"], "c": 1, "why": "The client can read and modify whatever you store, so keep decisions server-side."},
  {"q": "Correct handling of secrets in code:", "a": ["Commit and rotate later", "Load from environment or a secret store, never commit", "Base64 in the source", "In a private repo only"], "c": 1, "why": "Repository history is permanent and repositories leak."},
 ],
},
]
