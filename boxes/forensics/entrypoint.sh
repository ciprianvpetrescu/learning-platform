#!/bin/bash
set +e
mkdir -p /home/analyst
FLAG="${FLAG:-LEARN{dev_flag}}"
python3 /make_evidence.py "$FLAG"
cat > /home/analyst/BRIEF.txt <<'BRIEF'
CASE FILE: Coldcase

You have /home/analyst/case.dd, a raw disk image from a seized workstation.
The suspect deleted files before the machine was taken.

Your objectives:
 1. Identify the filesystem and mount or examine the image.
 2. Carve the deleted content out of unallocated space.
 3. Examine metadata on anything you recover. Timestamps do not lie, but people do.
 4. One recovered archive is password protected. The password appears in a document on the image.
 5. The flag is inside that archive.

Tools available: foremost, fls/icat (sleuthkit), file, xxd, strings, python3.

Hints:
 - foremost -t all -i case.dd -o out/
 - exiftool or strings on recovered images
BRIEF
chown -R analyst:analyst /home/analyst 2>/dev/null
id analyst >/dev/null 2>&1 || useradd -m -s /bin/bash analyst
echo 'analyst:analyst123' | chpasswd
chown -R analyst:analyst /home/analyst
sleep infinity
