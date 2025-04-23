#!/bin/bash

REMOTE_HOST="127.0.0.1"
REMOTE_PORT=4444

# Prompt for password (hidden input)
read -s -p "Enter password: " password
echo

echo "[+] Connecting to $REMOTE_HOST:$REMOTE_PORT..."
exec 3<>/dev/tcp/$REMOTE_HOST/$REMOTE_PORT || { echo "Connection failed."; exit 1; }

trap "exec 3<&-; exec 3>&-; exit" INT TERM EXIT

# Send password
echo "$password" >&3

while true; do
    read -p "Enter Command: " command
    [ -z "$command" ] && continue

    echo "$command" >&3

    if [[ "$command" == "exit" ]]; then
        break
    fi

    # Read response until delimiter line
    while IFS= read -r -u 3 line; do
        [[ "$line" == "VM $" ]] && break
        echo "$line"
    done
done
