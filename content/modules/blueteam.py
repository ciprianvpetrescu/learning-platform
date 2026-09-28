from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "blue-detection", "cat": "blueteam", "title": "Detection Engineering",
 "tier": E, "points": 125,
 "summary": "Turning attacker behaviour into alerts that fire on the real thing and stay quiet otherwise.",
 "theory": [
  ("Think In Behaviours", "Indicators of compromise, a specific hash or IP, expire the moment the attacker changes them. Behaviours do not. A process spawning a shell that then makes an outbound connection is suspicious regardless of filenames. Writing detections around behaviour survives tool changes, which is why mature teams focus there and use indicators for triage and hunting rather than as the primary rule."),
  ("The Pyramid Of Pain", "At the bottom sit hash values, trivially changed. Then IP addresses, then domain names, then network and host artefacts, then tools, then tactics, techniques and procedures at the top, which are expensive to change because they reflect how the attacker works. The higher you detect, the more it costs the adversary. Getting to the top requires understanding their playbook, which requires knowing the techniques."),
  ("Writing A Rule", "Start from a real observation, not a guess. Define what must be true, then test against normal activity to see how much noise it makes. A rule that fires a hundred times a day will be ignored, and an ignored rule is worse than no rule because it creates false confidence. Tune with exclusions that are specific rather than broad, and document why each exclusion exists so it can be reviewed later."),
  ("Coverage And Gaps", "Map your detections against a technique framework and look at what is blank. Blind spots are not evenly distributed: teams over-invest in what is easy to see and neglect cloud identity events, internal lateral movement, and living-off-the-land binaries that are legitimate tools used badly. Fill gaps deliberately rather than adding another rule where coverage already exists."),
 ],
 "labs": ["game-alert-triage", "lab-rule-writing"],
 "quiz": [
  {"q": "Why are behavioural detections better than hash-based ones?", "a": ["Faster", "They survive attacker tool changes", "Simpler", "Fewer logs"], "c": 1, "why": "Changing behaviour is much harder than changing a file hash."},
  {"q": "What is at the top of the pyramid of pain?", "a": ["Hash values", "IP addresses", "Tactics, techniques and procedures", "Domain names"], "c": 2, "why": "TTPs are the most expensive for an adversary to change."},
  {"q": "A detection that fires hundreds of times daily:", "a": ["Is thorough", "Will be ignored and creates false confidence", "Should be kept", "Indicates good coverage"], "c": 1, "why": "Alert fatigue makes the rule worthless in practice."},
  {"q": "Which area is most commonly a detection blind spot?", "a": ["Perimeter scanning", "Cloud identity events", "Malware hashes", "Antivirus alerts"], "c": 1, "why": "Cloud control-plane activity is frequently unmonitored."},
 ],
},
{
 "id": "blue-ir", "cat": "blueteam", "title": "Incident Response",
 "tier": M, "points": 150,
 "summary": "Preparation, triage, containment, eradication and the report nobody wants to write.",
 "theory": [
  ("The Cycle", "Preparation, identification, containment, eradication, recovery, lessons learned. Preparation is where the outcome is decided, because playbooks, access, logging and contacts cannot be created during an incident. Lessons learned is where most organisations fail: the report is written, the recommendations are accepted verbally, and nothing changes until the next incident repeats the same failure."),
  ("Triage", "Establish scope before acting. What is affected, how many systems, is it still active, is data leaving. Preserve evidence while containing: pulling the plug destroys memory, but leaving a system running lets the attacker continue and clean up. Contain by isolating network access while keeping the machine powered where forensic value warrants it. Do not tip off the attacker before you are ready to evict."),
  ("Containment And Eradication", "Block and isolate, rotate every credential the affected system could touch, and assume the attacker has more access than you have found. Eradication means removing the mechanism, not the symptom: delete the persistence, not just the process. Rebuild rather than clean where feasible, because you cannot prove a cleaned system is clean. Then watch hard during recovery, because returning attackers are common and they will use the door they know."),
  ("Communication", "A named incident commander, a scribe, and a single channel for decisions. Legal and regulatory notification deadlines are short in many jurisdictions, and privacy regulators may need to hear within seventy-two hours in Europe. Communicate what you know, what you do not, and when you will next update. Speculation in a status update becomes a quote in a lawsuit later."),
 ],
 "labs": ["game-incident-room", "lab-ir-playbook"],
 "quiz": [
  {"q": "Which phase decides the eventual outcome?", "a": ["Eradication", "Preparation", "Recovery", "Reporting"], "c": 1, "why": "Playbooks, logging and access must exist before the incident starts."},
  {"q": "First priority in triage?", "a": ["Delete the malware", "Establish scope and determine whether it is still active", "Reboot", "Email the company"], "c": 1, "why": "Acting without scope risks tipping off the attacker and missing other systems."},
  {"q": "Why rebuild rather than clean?", "a": ["Cheaper", "You cannot prove a cleaned system is actually clean", "Faster", "Required by law"], "c": 1, "why": "Unknown persistence may remain, and rebuilding removes that doubt."},
  {"q": "Forgetting lessons learned most commonly results in:", "a": ["Nothing", "The same incident recurring with the same root cause", "Faster response next time", "Better reporting"], "c": 1, "why": "Without remediation, the vulnerability remains and will be found again."},
 ],
},
{
 "id": "blue-hunt", "cat": "blueteam", "title": "Log Analysis & Threat Hunting",
 "tier": M, "points": 150,
 "summary": "SIEM queries, correlations, baselines, and hunting for what no rule catches.",
 "theory": [
  ("Assumption Of Breach", "Hunting starts from the premise that something is already inside and the rules have not caught it. That changes the question from whether a rule fired to what looks inconsistent with normal. You are looking for the absence of expected events, the presence of unusual ones, and the relationships between them across sources that no single rule spans."),
  ("Query Technique", "Know your data before you query it. What fields exist, what they contain, what the retention is, and what normal looks like over time. Group and count to find outliers rather than reading rows. A process appearing on one host is noise; appearing on two hundred hosts on the same day is a campaign. Aggregate first, then drill into the specimens that stand out."),
  ("Baselines", "Establish what normal looks like for authentication volume, outbound destinations, process trees, scheduled task creation and service installs. Deviation from a baseline is the signal. Baselines decay: new software, new staff and seasonal patterns all shift them, so they need maintenance or they generate noise that gets ignored."),
  ("Hunting Hypothesis", "A good hunt has a hypothesis framed as a question you can query: if an attacker had moved laterally via remote services, what would the successful authentication events look like, from where, and at what hour. Then you look, and you accept that finding nothing is a result rather than a failure, because you have narrowed the space and improved the rule that covers it."),
 ],
 "labs": ["game-log-whodunit", "lab-siem-query"],
 "quiz": [
  {"q": "Threat hunting assumes:", "a": ["No breach", "A breach may already exist undetected", "Rules catch everything", "Logs are complete"], "c": 1, "why": "The premise is that detection has already failed somewhere."},
  {"q": "Why aggregate before reading rows?", "a": ["Storage", "Outliers only appear against the distribution", "Speed", "Compliance"], "c": 1, "why": "A single event means little; the count relative to normal is the signal."},
  {"q": "Finding nothing on a hunt means:", "a": ["Wasted effort", "The answer is useful and the space is now narrower", "The tool failed", "Stop hunting"], "c": 1, "why": "Negative results are results, and they inform coverage."},
  {"q": "Baselines need maintenance because:", "a": ["Storage fills", "Normal changes and stale baselines create noise", "Attackers adapt", "Rules expire"], "c": 1, "why": "New software and seasonal patterns shift what normal looks like."},
 ],
},
]
