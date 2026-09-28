#!/bin/bash
set -e
FLAG=${FLAG:-LEARN{dev_flag_replace_me}}
echo "$FLAG" > /var/www/flag.txt
chmod 644 /var/www/flag.txt
# seed the sqlite/php data: a users table with a weak admin
php -r '
$pdo = new PDO("sqlite:/var/www/data.db");
$pdo->exec("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)");
$pdo->exec("DELETE FROM users");
$pdo->exec("INSERT INTO users (username,password,role) VALUES (\"admin\",\"S3cr3tAdm1n!\",\"admin\"),(\"jdoe\",\"hunter2\",\"user\"),(\"svc_backup\",\"Backup2019!\",\"service\")");
'
chown -R www-data:www-data /var/www
apache2-foreground
