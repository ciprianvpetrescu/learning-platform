#!/bin/bash
# Bastion - Linux privilege escalation lab. Deliberately vulnerable.
set +e

FLAG="${FLAG:-LEARN{dev_flag}}"
echo "$FLAG" > /root/flag.txt
chmod 600 /root/flag.txt

# ---- entry user ----
id analyst >/dev/null 2>&1 || useradd -m -s /bin/bash analyst
echo 'analyst:analyst123' | chpasswd

# ---- sudo rights: vim is a shell ----
mkdir -p /etc/sudoers.d
echo 'analyst ALL=(root) NOPASSWD: /usr/bin/vim' > /etc/sudoers.d/analyst-vim
chmod 440 /etc/sudoers.d/analyst-vim

# ---- root cron running a world-writable script ----
mkdir -p /opt/scripts
printf '#!/bin/bash\ncp /root/flag.txt /tmp/.flagcopy 2>/dev/null\nchmod 644 /tmp/.flagcopy 2>/dev/null\n' > /opt/scripts/cleanup.sh
chmod 777 /opt/scripts/cleanup.sh
printf '* * * * * root /opt/scripts/cleanup.sh\n' > /etc/cron.d/cleanup
chmod 644 /etc/cron.d/cleanup

# ---- setuid binary ----
mkdir -p /opt/app
printf '[database]\nuser = svc_backup\npassword = Backups_2024!\n' > /opt/app/config.ini
chmod 644 /opt/app/config.ini
id svc_backup >/dev/null 2>&1 || useradd -m -s /bin/bash svc_backup
echo 'svc_backup:Backups_2024!' | chpasswd
echo 'svc_backup ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/svc_backup
chmod 440 /etc/sudoers.d/svc_backup

echo 'Welcome to Bastion. Start with: sudo -l' > /home/analyst/readme.txt
chown analyst:analyst /home/analyst/readme.txt 2>/dev/null

sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config

# run the cleanup once so /tmp/.flagcopy appears immediately
/opt/scripts/cleanup.sh

service cron start >/dev/null 2>&1 || cron 2>/dev/null
exec /usr/sbin/sshd -D -e
