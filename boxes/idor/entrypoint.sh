#!/bin/bash
set -e
FLAG=${FLAG:-LEARN{dev_flag}}
echo "$FLAG" > /var/www/flag.txt
mkdir -p /var/www/invoices && chown -R www-data:www-data /var/www
apache2-foreground
