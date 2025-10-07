#!/bin/bash
set -Eeuo pipefail

export DISABLE_SECURITY_PLUGIN=${DISABLE_SECURITY_PLUGIN:-true}
export OPENSEARCH_INITIAL_ADMIN_PASSWORD=${OPENSEARCH_INITIAL_ADMIN_PASSWORD:-admin123}

/usr/local/bin/docker-entrypoint.sh &
OS_PID=$!

/opt/opensearch-dashboards/bin/opensearch-dashboards --host 0.0.0.0 --port 5601 &
DASH_PID=$!

python /logshipper.py &
SHIP_PID=$!

cleanup() {
    kill "$OS_PID" "$DASH_PID" "$SHIP_PID" 2>/dev/null || true
}

trap cleanup INT TERM

wait -n "$OS_PID" "$DASH_PID" "$SHIP_PID"
cleanup
