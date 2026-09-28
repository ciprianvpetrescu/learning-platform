#!/bin/bash
set -e
FLAG=${FLAG:-LEARN{dev_flag}}
echo "$FLAG" > /var/www/flag.txt
# internal admin service on loopback, only reachable from the fetcher itself
python3 /app/internal.py &
sleep 1
exec python3 /app/fetcher.py
