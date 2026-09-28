#!/bin/bash
set -e
apt-get update -qq && apt-get install -y -qq mariadb-server >/dev/null 2>&1 || true
FLAG=${FLAG:-LEARN{dev_flag}}
echo "$FLAG" > /var/www/flag.txt
chmod 644 /var/www/flag.txt
if command -v mariadbd >/dev/null 2>&1; then
  mkdir -p /run/mysqld && chown mysql:mysql /run/mysqld
  mariadbd --user=mysql --skip-grant-tables=0 >/var/log/mysql.log 2>&1 &
  for i in $(seq 1 30); do mysqladmin ping >/dev/null 2>&1 && break; sleep 1; done
  mysql -e "CREATE DATABASE IF NOT EXISTS archive;" 2>/dev/null || true
  mysql archive -e "CREATE TABLE IF NOT EXISTS documents (id INT PRIMARY KEY AUTO_INCREMENT, title VARCHAR(200), owner VARCHAR(100), body TEXT); CREATE TABLE IF NOT EXISTS admins (id INT PRIMARY KEY, username VARCHAR(100), password VARCHAR(200));" 2>/dev/null || true
  mysql archive -e "INSERT IGNORE INTO documents (id,title,owner,body) VALUES (1,'Quarterly report','jdoe','Revenue up 12 percent'),(2,'Merger memo','ceo','Confidential - pending announcement'),(3,'Staff handbook','hr','Section 4 covers leave'); INSERT IGNORE INTO admins (id,username,password) VALUES (1,'root_admin','REDACTED_BUT_EXTRACTABLE');" 2>/dev/null || true
  mysql archive -e "GRANT ALL ON archive.* TO 'app'@'localhost' IDENTIFIED BY 'apppass'; GRANT FILE ON *.* TO 'app'@'localhost';" 2>/dev/null || true
fi
apache2-foreground
