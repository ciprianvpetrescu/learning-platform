#!/bin/bash
set -e
FLAG=${FLAG:-LEARN{dev_flag}}
echo "$FLAG" > /var/www/flag.txt
chmod 644 /var/www/flag.txt
chmod -R 777 /var/www/html/uploads
apache2-foreground
