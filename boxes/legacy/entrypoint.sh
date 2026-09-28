#!/bin/bash
# A dated multi-service host. Each service carries a realistic weakness so the
# box rewards enumeration and known-issue recognition rather than a single bug.
set -u

FLAG="${FLAG:-LEGACY_default_flag}"

# --- flag lives with the service account that the privesc path reaches ---
printf %s "$FLAG" > /root/flag.txt
chmod 600 /root/flag.txt

# --- a cron-style world-writable script root runs (local privesc path) ---
cat > /usr/local/bin/cleanup.sh <<'CRON'
#!/bin/bash
# nightly cleanup
rm -f /tmp/*.tmp 2>/dev/null
cat /root/flag.txt 2>/dev/null > /var/www/html/.cache 2>/dev/null || true
CRON
chmod 777 /usr/local/bin/cleanup.sh

# --- ftp config: anonymous read, and a leak ---
cat > /etc/vsftpd.conf <<'FTP'
listen=YES
listen_ipv6=NO
anonymous_enable=YES
anon_root=/srv/ftp
local_enable=YES
write_enable=NO
anon_upload_enable=NO
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=YES
secure_chroot_dir=/var/run/vsftpd/empty
pam_service_name=vsftpd
FTP
mkdir -p /var/run/vsftpd/empty

# --- nginx serves the portal and the diagnostics endpoint ---
cat > /etc/nginx/sites-available/default <<'NGX'
server {
  listen 80 default_server;
  root /var/www/html;
  index index.html;
  location /status { try_files /status.html =404; }
  # a debug endpoint that was never removed
  location /debug {
    default_type text/plain;
    return 200 'LEGACY_DEBUG=1\nphp_version="removed"\nbackup_user=svc_backup\nbackup_pass=B4ckup2019!\nnote=see /pub/db_backup.ini\n';
  }
}
NGX

# --- ssh: password auth, weak credential ---
cat > /etc/ssh/sshd_config <<'SSH'
Port 22
PermitRootLogin no
PasswordAuthentication yes
PermitEmptyPasswords no
UsePAM yes
Subsystem sftp /usr/lib/openssh/sftp-server
SSH

# start everything
/usr/sbin/vsftpd /etc/vsftpd.conf &
in.telnetd -debug 23 &
service ssh start 2>/dev/null || /usr/sbin/sshd &
nginx -g 'daemon off;' &

# a small loop that lets the world-writable script be triggered (the 'cron')
while true; do
  sleep 20
  # simulate the nightly cleanup running, which writes the flag where the
  # writable-script privesc can reach it
  /usr/local/bin/cleanup.sh 2>/dev/null || true
done
