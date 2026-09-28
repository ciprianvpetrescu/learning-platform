#!/bin/bash
set +e
FLAG="${FLAG:-LEARN{dev_flag}}"
echo "$FLAG" > /root/flag.txt
chmod 600 /root/flag.txt
id dev >/dev/null 2>&1 || useradd -m -s /bin/bash dev
echo 'dev:dev123' | chpasswd
# Grant a capability the lab expects you to notice
apt-get install -y -qq libcap2-bin >/dev/null 2>&1
setcap cap_setuid+ep /usr/bin/python3.11 2>/dev/null || setcap cap_setuid+ep /usr/bin/python3 2>/dev/null
echo 'Check your environment. Something here is stronger than it should be.' > /home/dev/hint.txt
chown dev:dev /home/dev/hint.txt
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
exec /usr/sbin/sshd -D -e
