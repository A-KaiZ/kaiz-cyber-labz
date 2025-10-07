#!/bin/bash
set -Eeuo pipefail

show_help() {
    cat <<'USAGE'
Usage: import.sh

Wait for OpenSearch and Dashboards to become available, then import saved
objects located in /opt/detect/detections/elastic/.
USAGE
}

if [[ ${1:-} == "--help" || ${1:-} == "-h" ]]; then
    show_help
    exit 0
fi

API_URL=${OPENSEARCH_URL:-http://localhost:9200}
DASH_URL=${DASHBOARD_URL:-http://localhost:5601}

until curl -s "$API_URL" >/dev/null; do
    echo "Waiting for OpenSearch at $API_URL..."
    sleep 5
done

echo "OpenSearch reachable. Importing saved search and dashboards."

curl -s -X POST "$DASH_URL/api/saved_objects/_import?overwrite=true" \
    -H 'kbn-xsrf: true' \
    -F "file=@/opt/detect/detections/elastic/kibana_saved_search.ndjson" >/dev/null

curl -s -X POST "$DASH_URL/api/saved_objects/_import?overwrite=true" \
    -H 'kbn-xsrf: true' \
    -F "file=@/opt/detect/detections/elastic/dashboards.ndjson" >/dev/null

echo "Dashboards imported. Access $DASH_URL/app/dashboards#/view/cyber-lab-overview"
