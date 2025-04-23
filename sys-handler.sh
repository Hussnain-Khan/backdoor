#!/bin/bash

read -r password

# Use SHA256 hash instead of python's hash() (non-consistent across machines)
PASSWORD_HASH="c93c0e15af7c49fcdd7ec9532416f4f16cd7a5a38545ebca1d5b2b8b57f74b08" # hash of "c0d3m@nk3y"

if [[ "$(echo -n "$password" | sha256sum | awk '{print $1}')" != "$PASSWORD_HASH" ]]; then
    echo "Authentication failed."
    exit 1
fi

echo "Authentication successful."

while true; do
    echo -n "VM $ "
    if ! read -r cmd; then break; fi
    [[ "$cmd" == "exit" ]] && break

    result=$(eval "$cmd" 2>&1)
    if [[ -z "$result" ]]; then
        echo "no stdout"
    else
        echo "$result"
    fi
    echo "VM $"  # Signal end of response
done
