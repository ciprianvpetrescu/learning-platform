#!/bin/bash
set -e
FLAG=${FLAG:-LEARN{dev_flag}}
echo "$FLAG" > /var/www/flag.txt
mkdir -p /var/www/html/entries && chown -R www-data:www-data /var/www/html
# the admin bot stores its cookie here for the solver to steal
apache2-foreground
