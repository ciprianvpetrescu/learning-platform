from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "cloud-containers", "cat": "cloud", "title": "Container Security & Escapes",
 "tier": E, "points": 125,
 "summary": "Namespaces, cgroups, privileged containers, mounted sockets and how a container becomes a host.",
 "theory": [
  ("What A Container Is", "A container is a process with namespaces giving it an isolated view of the filesystem, process tree, network and hostnames, plus cgroup limits on resources. It is not a virtual machine and there is no hypervisor between it and the host kernel. Every kernel vulnerability is a container escape candidate, and every misconfiguration is a shortcut."),
  ("Common Misconfigurations", "Running as root inside the container is the default in most images and is unnecessary. Privileged mode disables the isolation entirely, granting every capability and device access. A mounted Docker socket is an immediate host compromise: the Docker API lets you start a container that mounts the host filesystem. Mounted sensitive paths like the host root, the proc directory, or device nodes all provide paths out. Capabilities beyond the default set, particularly cap_sys_admin, are powerful."),
  ("Escaping", "Check the environment first: are you privileged, what is mounted, what capabilities do you hold, is the socket present. From there, mounting the host filesystem read-write and modifying the passwd file or planting a setuid binary is straightforward. Abusing a writable cgroup release agent, exploiting a kernel bug, or attaching to the host namespaces through the proc filesystem are the alternatives. The escape is usually easier than the bug."),
  ("Hardening", "Run as a non-root user with a read-only root filesystem. Drop all capabilities and add back only what is needed. Do not mount the socket. Use user namespaces to map container root to an unprivileged host user. Apply seccomp profiles to limit syscalls and AppArmor or SELinux profiles for mandatory access control. Scan images, and rebuild from minimal base images rather than patching large ones."),
 ],
 "labs": ["box-docker-escape", "game-container-config"],
 "quiz": [
  {"q": "Why is a mounted Docker socket dangerous?", "a": ["It is slow", "The Docker API allows starting a container that mounts the host filesystem", "It uses memory", "It blocks networking"], "c": 1, "why": "Full API access is effectively root on the host."},
  {"q": "What does a privileged container grant?", "a": ["Faster CPU", "All capabilities and device access, effectively disabling isolation", "More storage", "Better networking"], "c": 1, "why": "It removes essentially every containment boundary."},
  {"q": "Which is a container, not a VM?", "a": ["A hypervisor-isolated guest", "A namespaced process on the host kernel", "A separate machine", "A virtual disk"], "c": 1, "why": "Containers share the host kernel; that is the entire security model and the entire risk."},
  {"q": "Best hardening step for a web container?", "a": ["Privileged mode", "Non-root user with dropped capabilities and a read-only root", "Mount the socket", "Bigger image"], "c": 1, "why": "Least privilege inside the container limits what an escape is even worth."},
 ],
},
{
 "id": "cloud-kubernetes", "cat": "cloud", "title": "Kubernetes Attack Paths",
 "tier": M, "points": 175,
 "summary": "Exposed APIs, anonymous access, service account tokens, RBAC abuse and secrets.",
 "theory": [
  ("The API Server Is The Target", "Everything in Kubernetes is an API object, and kubectl is just a client. An exposed API server with anonymous access enabled, or with a weak credential, gives the entire cluster. Check whether you can list namespaces before anything else; that tells you whether authentication exists at all. The cloud control plane for the cluster's provider is a second front, since compromising it often yields the cluster."),
  ("Service Account Tokens", "Every pod gets a token mounted at a known path, and depending on the version and configuration it may be a long-lived credential. Steal the token and you inherit the pod's permissions. In cloud-hosted clusters with workload identity, that token may be exchanged for cloud credentials, so the pod's identity is a cloud identity. This is how a vulnerable web application becomes a cloud account compromise."),
  ("RBAC Abuse", "Permissions are composable and the dangerous combinations are not obvious. The ability to create pods lets you mount the host filesystem. The ability to create a role binding lets you grant yourself more. The ability to read secrets, or to impersonate another service account, or to exec into a privileged pod, each escalates. Read your permissions carefully with can-i, and look for what is permitted that should not be."),
  ("Secrets And Configuration", "Secrets are base64-encoded by default, not encrypted, and readable by anyone with get on secrets in that namespace. They sit in etcd, in backups, in CI variables and in repository history. Misconfigured dashboards, exposed metrics endpoints, and debug ports on pods all leak information. The fix is encryption at rest, tight RBAC, short-lived projected tokens and frequent credential rotation."),
 ],
 "labs": ["box-k8s", "game-rbac-path"],
 "quiz": [
  {"q": "Where do pods get their service account token?", "a": ["From the network", "A file mounted into the pod filesystem", "Environment only", "The cloud provider"], "c": 1, "why": "It is projected into the pod at a well-known path, readable by the process."},
  {"q": "Which RBAC permission most directly enables host compromise?", "a": ["get pods", "create pods", "list namespaces", "read logs"], "c": 1, "why": "Creating a pod lets you mount host paths, run privileged, or use the host network."},
  {"q": "Kubernetes secrets are stored how by default?", "a": ["Encrypted at rest", "Base64-encoded, meaning readable by anyone permitted to get them", "Hashed", "In a hardware module"], "c": 1, "why": "Base64 is encoding, not encryption, and RBAC is the only barrier."},
  {"q": "Anonymous access to the API server means:", "a": ["Nothing", "Unauthenticated users can perform whatever RBAC grants", "The cluster is encrypted", "Safe by default"], "c": 1, "why": "If anonymous is bound to any role, that role is available to the internet."},
 ],
},
{
 "id": "cloud-iam", "cat": "cloud", "title": "Cloud IAM & Metadata Attacks",
 "tier": M, "points": 175,
 "summary": "Identity as the perimeter, over-permissive roles, and stealing credentials from instance metadata.",
 "theory": [
  ("Identity Is The Perimeter", "In cloud, the network boundary is largely irrelevant. What matters is which identity can call which API on which resource. Compromising an access key or a role's temporary credentials is the objective, because with valid credentials there is very little to stop you. Look for keys in code repositories, CI systems, environment variables, container images, and instance metadata."),
  ("Metadata Services", "The link-local metadata address exposes instance information and, depending on configuration and provider, temporary credentials for the attached role. Requiring a token header before returning credentials defeats the simplest SSRF exploitation, but not an SSRF that can set arbitrary headers or that reaches a service capable of requesting the token itself. Chained impersonation and metadata endpoints on container platforms are the same story with different addresses."),
  ("Over-Permission", "Wildcard actions and wildcard resources are common and turn a small foothold into account-wide capability. Roles that can create new identities, attach policies to themselves or assume other roles allow escalation from within. Read your own permissions, enumerate what you can reach, and look specifically for the permission that lets you grant yourself more. Very often it exists."),
  ("Exfiltration And Impact", "With credentials you read storage buckets, snapshots and backups; you run compute for crypto mining; you modify logging settings to blind the defenders; you create persistence through a new access key or a modified function. Defence is least privilege with regular review, short-lived credentials over static keys, monitoring of identity events specifically, and treating credential exposure as the highest-severity incident class in cloud."),
 ],
 "labs": ["game-iam-escalate", "lab-metadata-hunt"],
 "quiz": [
  {"q": "What does the cloud instance metadata service provide?", "a": ["DNS", "Instance information and often temporary role credentials", "Storage", "Firewall rules"], "c": 1, "why": "It is the standard path from SSRF to cloud credentials."},
  {"q": "Which policy pattern is most dangerous?", "a": ["Specific action on specific resource", "Wildcard action on all resources", "Deny with conditions", "Read-only on one bucket"], "c": 1, "why": "It grants everything the identity can reach."},
  {"q": "Why prefer short-lived credentials?", "a": ["Cheaper", "Exposure is bounded in time", "Faster", "More compatible"], "c": 1, "why": "A leaked static key is valid until someone notices; a temporary one expires."},
  {"q": "What is the primary cloud recommendation for access keys?", "a": ["Rotate yearly", "Avoid static keys and use roles with temporary credentials", "Share within teams", "Store in the repo encrypted"], "c": 1, "why": "Roles remove the long-lived secret entirely."},
 ],
},
]
