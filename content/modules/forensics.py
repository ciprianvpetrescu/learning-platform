from content.categories import F, E, M, H, I

MODULES = [
{
 "id": "for-evidence", "cat": "forensics", "title": "Evidence Handling & Imaging",
 "tier": F, "points": 75,
 "summary": "Order of volatility, chain of custody, write blockers and hashing your images.",
 "theory": [
  ("Order Of Volatility", "Collect the most perishable evidence first. Registers and cache, then memory, then network state and running processes, then disk, then archival backups. Pulling the plug destroys memory and any fileless malware evidence with it, though it also prevents a malicious shutdown routine from wiping the disk. The choice depends on the case, and knowing why you made it is the point."),
  ("Proving Integrity", "Hash the source before acquisition, hash the image after, hash again at analysis. Matching MD5 and SHA-256 values demonstrate that what you examined is what you collected. Document who handled the media, when, and where, with signatures, because an unbroken chain of custody is what makes evidence admissible. A technically perfect analysis in a broken chain is worth very little in a hearing."),
  ("Acquisition", "Use a write blocker so the source cannot change. Do a physical acquisition when you need deleted data and unallocated space, a logical one when you only need files. Check for full-disk encryption, which needs a key from the user or from memory before it is any use. On virtual machines, snapshot and copy rather than converting, which preserves everything."),
  ("Tools", "dd and dcfldd for raw imaging, EWF for a forensic format with embedded metadata, FTK Imager, Guymager, and Autopsy for analysis. Sleuthkit provides the command-line core. Learn one tool deeply and the concepts transfer, because they all expose the same filesystem structures."),
 ],
 "labs": ["game-evidence-order", "lab-image-hash"],
 "quiz": [
  {"q": "Which evidence is most volatile?", "a": ["Disk", "CPU registers and cache", "Backups", "Printed logs"], "c": 1, "why": "Registers and cache vanish fastest, then memory, then network state."},
  {"q": "Why hash an image?", "a": ["Compression", "To prove it matches the source and is unaltered", "Encryption", "Faster indexing"], "c": 1, "why": "Matching hashes establish integrity and reproducibility."},
  {"q": "What is a write blocker for?", "a": ["Speed", "Preventing modification of the source media", "Encryption", "Compression"], "c": 1, "why": "It makes acquisition non-destructive."},
  {"q": "What is chain of custody?", "a": ["Key rotation", "Documented control of evidence from collection to court", "File permissions", "Backup schedule"], "c": 1, "why": "It is the unbroken record of who held the evidence and when."},
 ],
},
{
 "id": "for-filesystems", "cat": "forensics", "title": "Filesystem Forensics & Carving",
 "tier": E, "points": 125,
 "summary": "Deleted files, NTFS and ext structures, file carving and metadata timelines.",
 "theory": [
  ("Deletion Is A Lie", "Deleting a file usually removes the pointer, not the data. The inode is marked free and the blocks become available for reuse, so until something overwrites them the content is still on disk, reachable by carving known structures out of unallocated space. Secure deletion is a separate operation, which is why forensic images are taken at the block level."),
  ("Structures Worth Knowing", "On NTFS, the master file table holds a record per file with timestamps and data run locations; the dollar-MFT, dollar-LogFile and USN journal are rich sources. On ext, inodes hold metadata and block pointers, with the journal recording recent changes. Alternate data streams on NTFS hide content normal browsing never shows. Hibernation and page files contain fragments of memory."),
  ("Timestamps As Evidence", "NTFS records four times per file: created, modified, MFT-modified and accessed. Discrepancies between them indicate tampering, because timestomping tools usually alter only the ones they know about. Build a timeline across many sources, filesystem metadata, logs, browser history, registry, and the case emerges from relationships rather than any single artefact."),
  ("Carving", "File carving recovers content by signature rather than metadata: scan for known headers such as JPEG, PNG, PDF or ZIP and extract until the footer. It works even when metadata is gone. Fragmented files reconstruct badly, and filenames and timestamps are lost, so you recover those from elsewhere. Scalpel, foremost and photorec are the standard tools."),
 ],
 "labs": ["box-forensics", "game-file-carve"],
 "quiz": [
  {"q": "When a file is deleted, what happens to its data?", "a": ["Overwritten instantly", "Remains until blocks are reused", "Encrypted", "Moved to backup"], "c": 1, "why": "Only the pointer is released; blocks persist until overwritten."},
  {"q": "Which NTFS structure is a primary forensic source?", "a": ["Master File Table", "/etc/passwd", "The swap file only", "The boot sector only"], "c": 0, "why": "The MFT holds a record per file with timestamps and data runs."},
  {"q": "What is file carving?", "a": ["Compression", "Recovering files by header and footer signatures in raw data", "Encryption", "Renaming"], "c": 1, "why": "It ignores metadata and reconstructs from content signatures."},
  {"q": "A file's created time is later than its modified time. This suggests:", "a": ["Nothing", "Possible timestomping or a copy", "Disk corruption", "Normal operation"], "c": 1, "why": "The anomaly is a classic tampering indicator, though copying is a benign explanation."},
  {"q": "What is an alternate data stream?", "a": ["A backup copy", "Hidden content attached to an NTFS file", "A compressed archive", "A log file"], "c": 1, "why": "ADS hides data alongside a file without changing apparent size."},
 ],
},
{
 "id": "for-stego", "cat": "forensics", "title": "Steganography & Hidden Data",
 "tier": E, "points": 125,
 "summary": "LSB embedding, metadata, appended archives and how to find what is hidden.",
 "theory": [
  ("Least Significant Bits", "An image's colour values can be altered in their last bit with no visible change, so a message spreads across the pixels. Detection looks for statistical anomalies in those bits, which reveal structure where randomness is expected. Stegsolve cycles through colour and bit planes for exactly this."),
  ("Metadata And Appended Data", "Exif holds camera, timestamps and sometimes GPS. Header comments hold arbitrary content. Data appended after an image's end marker is invisible to viewers but trivially extractable, and a ZIP concatenated onto a JPEG remains valid as both, which is a polyglot file. Check file size against expected dimensions and look for multiple signatures in one file."),
  ("Audio And Other Carriers", "Audio spectrograms sometimes contain text written into the frequency spectrum, visible when you plot it. Phase coding and echo hiding are more advanced. Video, PDFs, documents and even packet timing carry payloads. The unifying question is whether anything exists that does not need to."),
  ("Practical Method", "Run strings and look for readable fragments. Check metadata with exiftool. Look for trailing data with a hex editor or binwalk. Try common passphrases, since in a learning context the password is weak or empty. Then examine bit planes. Order tools from simplest to most exotic, because the simple answer is usually right."),
 ],
 "labs": ["game-stego-hunt", "lab-exif-recover"],
 "quiz": [
  {"q": "What does LSB steganography modify?", "a": ["File permissions", "The least significant bit of each colour value", "The filename", "Compression level"], "c": 1, "why": "Single-bit changes are imperceptible but carry the message."},
  {"q": "Data appended after a JPEG end marker is:", "a": ["Lost", "Still present and extractable", "Compressed", "Encrypted"], "c": 1, "why": "Viewers stop at the marker; trailing bytes remain in the file."},
  {"q": "Which tool shows Exif metadata?", "a": ["nmap", "exiftool", "tcpdump", "hydra"], "c": 1, "why": "exiftool reads metadata across many formats."},
  {"q": "How might text hide in audio?", "a": ["Changing bitrate", "Written into the spectrogram", "Renaming", "Cover art"], "c": 1, "why": "Plotting the spectrum can reveal letters drawn into it."},
 ],
},
{
 "id": "for-memory", "cat": "forensics", "title": "Memory Forensics",
 "tier": M, "points": 150,
 "summary": "Analysing RAM dumps: process lists, network connections, injected code and credentials.",
 "theory": [
  ("Why Memory", "Fileless malware lives only in RAM. Decrypted documents, plaintext credentials, encryption keys and clipboard contents exist there and nowhere else. A disk image of a filelessly compromised machine can look entirely clean. Capturing memory is often the difference between a case and no case."),
  ("Process Analysis", "Compare the process list against what should be running. Look for unusual parent-child relationships, a document reader spawning a shell, a service running from a temporary directory, or a process whose executable is deleted from disk. Cross-reference the network connection table to see what is talking out. A process with no on-disk binary is a strong signal."),
  ("Injection And Hiding", "Attackers inject code into legitimate processes and unlink their own from the linked list, so the process list lies. Comparing a list derived from pool tags against a linked-list traversal exposes hidden entries. Look inside process memory for executable regions that should be private, and dump those regions."),
  ("Volatility Workflow", "Identify the profile, then work through imageinfo, pslist, pstree, netscan, cmdline, dlllist, malfind and hashdump. The order matters: establish what should be there, then find what should not. Timeline the artefacts afterwards. Practising on known-good and known-bad images is what builds instinct."),
 ],
 "labs": ["box-memory", "game-injected-process"],
 "quiz": [
  {"q": "Why capture memory when a disk image exists?", "a": ["It is faster", "Fileless malware and plaintext secrets live only in RAM", "Disk images are unreliable", "It is legally required"], "c": 1, "why": "Memory holds artefacts that never touch disk."},
  {"q": "Which Volatility plugin lists network connections?", "a": ["pslist", "netscan", "dlllist", "hashdump"], "c": 1, "why": "netscan recovers connection structures from memory."},
  {"q": "A process running from a temp directory with a deleted binary suggests:", "a": ["Normal operation", "Malicious execution and cleanup", "A system update", "Disk failure"], "c": 1, "why": "Running from temp with the executable removed is a classic hiding technique."},
  {"q": "Why can the process list be incomplete?", "a": ["Memory limits", "Attackers can unlink processes from the kernel list", "Antivirus interference", "Paging"], "c": 1, "why": "Direct kernel object manipulation removes entries from the traversal."},
 ],
},
]
