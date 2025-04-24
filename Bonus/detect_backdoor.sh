#!/bin/bash

echo "[*] Running advanced backdoor detection..."

# 1. Look for hidden executable scripts in sensitive directories
echo "[*] Searching for hidden or suspicious scripts in /root, /usr/local/bin, /etc/systemd..."
find /root /usr/local/bin /etc/systemd/system -type f \( -name ".*" -o -name "*upd*" -o -name "*sys*" -o -name "*.sh" \) -exec ls -lh {} \; 2>/dev/null | grep -Ev 'bash_completion|dpkg'

# 2. Detect custom systemd services (excluding known ones)
echo "[*] Checking for unusual systemd services..."
systemctl list-unit-files --type=service | grep -vE "network|ssh|cron|dbus|getty|syslog|rsyslog|snapd|systemd" | grep enabled

# 3. Check for unknown listeners on uncommon ports
echo "[*] Scanning for uncommon open ports..."
ss -tulnp | awk '{print $5}' | grep -Eo '[0-9]+$' | sort -n | uniq | grep -Ev '^22$|^80$|^443$|^53$|^631$|^3306$|^5432$' | while read port; do
    echo "[!] Port $port is open and may be suspicious."
done

# 4. Check for persistence techniques: cron jobs, systemd, rc.local
echo "[*] Checking for suspicious persistence mechanisms..."
crontab -l 2>/dev/null | grep -v '^#' && echo "[!] Cronjob detected"
[ -f /etc/rc.local ] && grep -v '^#' /etc/rc.local | grep -v '^$' && echo "[!] rc.local contains active commands"

echo "backdoor detection complete."
