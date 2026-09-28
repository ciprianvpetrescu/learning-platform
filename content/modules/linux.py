from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "nix-shell", "cat": "linux", "title": "The Shell & Command Line",
 "tier": F, "points": 50,
 "summary": "Navigation, files, pipes, redirection and the tools you will live in.",
 "theory": [
  ("Finding Your Way", "pwd tells you where you are, ls -la shows everything including hidden files with permissions, cd moves you, and ~ is home. Absolute paths start at root; relative paths start from where you stand. Tab completion and history search with Ctrl-R are not luxuries, they are how you work at speed."),
  ("Reading Files", "cat dumps a file, less pages through it, head and tail show the ends and tail -f follows a log live. grep searches, and with -r it recurses, with -i it ignores case, with -n it shows line numbers. find locates files by name, type, size or permission, and it is the tool you will reach for most during privilege escalation."),
  ("Pipes And Redirection", "The vertical bar sends one command's output into the next. Sort, uniq, cut, awk, sed and grep chain together into ad-hoc data processing. A single greater-than writes to a file and destroys what was there; two greater-thans append. Two is stderr, so two greater-than ampersand-one merges errors into standard output. This is how you capture command output into a file to review."),
  ("Permissions", "Every file has an owner, a group, and three triads of read, write and execute. Numerically, read is four, write is two, execute is one, so seven-five-five gives the owner everything and everyone else read and execute. Directories need execute to be entered. A setuid binary runs as its owner, which is why a root-owned setuid program is a privilege escalation target."),
  ("Processes", "ps aux lists processes, top and htop show them live, kill terminates by PID. Background a job with ampersand, suspend with Ctrl-Z, resume with bg or fg. Cron schedules jobs; systemd timers do it better. Anything running as root that you can influence is a path upward."),
 ],
 "labs": ["lab-shell-basics", "game-cmdline-gauntlet"],
 "quiz": [
  {"q": "What does chmod 644 give the owner?", "a": ["Read only", "Read and write", "Read, write and execute", "Execute only"], "c": 1, "why": "6 is 4 plus 2, read and write, with no execute."},
  {"q": "Which redirects standard error into standard output?", "a": [">", ">>", "2>&1", "&>"], "c": 2, "why": "2>&1 points file descriptor 2 at wherever descriptor 1 currently points."},
  {"q": "What does a setuid bit on a root-owned binary mean?", "a": ["It cannot be run", "It runs with root privileges whoever executes it", "Only root may run it", "It is encrypted"], "c": 1, "why": "Setuid makes the process run as the file owner, so a vulnerable setuid-root binary is a direct escalation path."},
  {"q": "Which command follows a log file as it grows?", "a": ["head -f", "tail -f", "cat -w", "less -r"], "c": 1, "why": "tail -f keeps the file open and prints new lines as they arrive."},
  {"q": "To find all files owned by user bob under the current directory:", "a": ["find . -user bob", "ls -user bob", "grep bob .", "locate bob"], "c": 0, "why": "find with -user filters by owner."},
 ],
},
{
 "id": "nix-perms", "cat": "linux", "title": "Users, Permissions & Services",
 "tier": E, "points": 100,
 "summary": "Accounts, sudo, file permissions, systemd units and the files that decide who can do what.",
 "theory": [
  ("Accounts", "The passwd file lists users, shadow holds password hashes and is readable only by root, and group lists memberships. Every user has a numeric UID; zero is root. Adding a user to the sudo or wheel group grants administrative rights. Service accounts exist to run daemons with fewer privileges, and a service running as root is a finding in itself."),
  ("sudo And su", "sudo runs a command as another user, governed by the sudoers file. Run sudo -l the moment you land on a box: it lists what you may run, and a wildcard or a runnable editor or interpreter in that list is usually the whole game. su switches user entirely, and su without a username assumes root."),
  ("Special Bits And Capabilities", "Setuid runs as the file owner; setgid does the same for the group or makes a directory inherit its group; the sticky bit on a directory restricts deletion to owners. Capabilities split root's powers into finer pieces, so a binary with cap_setuid can change UIDs without being fully setuid. Check them with getcap, and check for interesting entries system-wide."),
  ("systemd Units", "Services are defined by unit files in the system directory, with local overrides in etc slash systemd slash system. A writable unit file, or a service that runs a script you can modify, is a direct path to root. systemctl status, cat and list-timers are the commands to know. Timers replace cron elegantly and are just as abusable."),
 ],
 "labs": ["lab-suid-privesc", "lab-systemd-abuse"],
 "quiz": [
  {"q": "Where are password hashes stored?", "a": ["/etc/passwd", "/etc/shadow", "/etc/group", "/etc/security"], "c": 1, "why": "The shadow file holds the hashes and is root-readable only."},
  {"q": "Which command lists your permitted sudo commands?", "a": ["sudo --show", "sudo -l", "sudo -v", "sudoers -p"], "c": 1, "why": "sudo -l prints your sudo rights, and it is the first thing to check after gaining a shell."},
  {"q": "What does the sticky bit do on a directory?", "a": ["Prevents writes entirely", "Lets only file owners delete their files", "Encrypts contents", "Makes files executable"], "c": 1, "why": "In shared directories like slash tmp, it stops users deleting each other's files."},
  {"q": "A binary with cap_setuid can do what?", "a": ["Read any file", "Change user IDs, potentially to root", "Open raw sockets", "Mount filesystems"], "c": 1, "why": "cap_setuid allows changing process UIDs, which is enough to become root from a vulnerable binary."},
  {"q": "Where do local systemd override units live?", "a": ["/etc/systemd/system", "/var/systemd", "/etc/init.d", "/usr/lib/units"], "c": 0, "why": "Local overrides go in slash etc slash systemd slash system and take precedence."},
 ],
},
{
 "id": "nix-privesc", "cat": "linux", "title": "Linux Privilege Escalation",
 "tier": M, "points": 150,
 "summary": "From a user shell to root: enumeration, SUID abuse, cron, PATH, credentials and kernel bugs.",
 "theory": [
  ("Enumeration First", "Privilege escalation is mostly reading. What kernel, what OS, who am I, what groups, what can sudo do, what is setuid, what cron jobs exist, what is writable, what credentials sit in config files or history. Automated scripts help, but a tool that finds a path you do not understand leaves you stuck the moment the target deviates. Learn to do the manual checks, then let the tool confirm."),
  ("SUID And Capabilities", "Find setuid binaries with a find across the filesystem. Compare the list against known-good packages; anything custom stands out. A setuid copy of a shell, editor, interpreter or archive tool is usually game over, because it can read or execute as root. Check capability sets too, since cap_setuid or cap_dac_read_search on the wrong binary is just as good."),
  ("Scheduled Tasks", "Cron jobs and systemd timers running as root are a favourite. Look for scripts in writable directories, relative paths without a leading slash, wildcards a filename can hijack, or scripts whose output you can influence. If a root job runs a program by bare name, and you can write earlier in the PATH, you own root."),
  ("Credentials And Misconfiguration", "Hunt the filesystem for passwords: config files, environment files, database configs, backups, history files, SSH keys without passphrases. Then look for misconfiguration: world-writable service files, root-owned scripts you can edit, NFS exports with no squashing, mounted docker sockets. The human error is nearly always easier than the kernel exploit."),
  ("Kernel Exploits, Last", "A kernel exploit is the fallback, not the plan. They are version-specific, can panic the machine, and a crash on a shared host is a bad day. Use them when enumeration has genuinely been exhausted and the box is yours to break."),
 ],
 "labs": ["box-linux-privesc", "game-privesc-path"],
 "quiz": [
  {"q": "What is the highest-value first command after getting a shell?", "a": ["whoami", "sudo -l", "uname -a", "id"], "c": 1, "why": "sudo -l is often the fastest answer to whether escalation is trivial. Run all four, but this one decides the game."},
  {"q": "A root cron job runs backup.sh with no absolute path. What is the attack?", "a": ["Kernel exploit", "PATH hijack by placing a malicious 'backup.sh' earlier in PATH", "Brute force", "ARP poisoning"], "c": 1, "why": "Without an absolute path, which program runs depends on PATH order, and you may control an earlier directory."},
  {"q": "Which find command locates setuid binaries?", "a": ["find / -perm -4000", "find / -suid", "ls -R / +setuid", "grep -r setuid /"], "c": 0, "why": "-perm -4000 matches the setuid bit."},
  {"q": "Why is a kernel exploit usually a last resort?", "a": ["It is slow", "It is version-specific and risks crashing the host", "It needs a password", "It only works on Windows"], "c": 1, "why": "Reliability is low and a panic can take down the box or the whole host."},
  {"q": "An NFS export configured with no_root_squash allows what?", "a": ["Nothing special", "A root client to write files owned by root on the share", "Anonymous read only", "Faster transfers"], "c": 1, "why": "Without squashing, remote root keeps root ownership and can plant a setuid binary."},
 ],
},
{
 "id": "nix-logs", "cat": "linux", "title": "Logging & Process Investigation",
 "tier": E, "points": 100,
 "summary": "Where the evidence lives on a Linux host, and how to read a process like a picture.",
 "theory": [
  ("Where Logs Live", "Under var slash log you find syslog or messages, auth for authentication, and per-service directories. Modern systems pipe to the journal, queried with journalctl, filterable by unit, time or priority. Application logs often land elsewhere entirely, so check the service definition for its own path. Log rotation means you may need the compressed archives too."),
  ("The Proc Filesystem", "Every process exposes itself under slash proc slash PID. cmdline shows the exact command line, environ shows its environment, and the file descriptors in fd reveal open files and sockets. Deleted-but-open files still appear in fd, which is how you recover a binary an attacker removed. This is the kernel's view, and it does not lie."),
  ("Authentication Traces", "Failed and successful logins, sudo usage, and session opens all land in auth logs. Sudden bursts of failures from one source suggest brute force; a success immediately after a burst suggests it worked. New user creation, group changes and cron edits are all recorded too, and together they tell a story about intent."),
  ("Persistence Mechanisms", "Attackers want to survive reboot. Look in cron directories, systemd units and timers, shell profile files and rc scripts, SSH authorized_keys, and less obviously in systemd generators or LD_PRELOAD settings in environment files. Finding persistence is how you know an incident is not over."),
 ],
 "labs": ["game-log-whodunit", "lab-log-triage"],
 "quiz": [
  {"q": "Which log records authentication events on most Linux systems?", "a": ["/var/log/syslog only", "/var/log/auth.log", "/var/log/kern.log", "/var/log/dpkg.log"], "c": 1, "why": "auth.log records logins, sudo and session events on Debian-derived systems."},
  {"q": "How do you see the environment of running process 1234?", "a": ["cat /proc/1234/environ", "env -p 1234", "ps --env 1234", "ls /proc/1234/env"], "c": 0, "why": "The environ file under the process directory holds the environment it was started with."},
  {"q": "Which is NOT typical persistence?", "a": ["A cron job", "A systemd timer", "A new SSH authorized_key", "A read-only /etc/passwd"], "c": 3, "why": "A read-only passwd file is normal state, not persistence."},
  {"q": "A burst of failed logins followed by one success means what?", "a": ["Nothing", "Likely successful brute force", "Disk failure", "Kernel panic"], "c": 1, "why": "The pattern is the signature of guessing until it worked."},
 ],
},
]
