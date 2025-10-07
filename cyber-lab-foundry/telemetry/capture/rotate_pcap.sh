#!/bin/bash
set -Eeuo pipefail

show_help() {
    cat <<'USAGE'
Usage: rotate_pcap.sh

Monitors the pcaps directory and removes files older than the retention
threshold (default: 10 files).
USAGE
}

if [[ ${1:-} == "--help" || ${1:-} == "-h" ]]; then
    show_help
    exit 0
fi

PCAP_DIR=/opt/capture/pcaps
RETENTION_COUNT=${RETENTION_COUNT:-10}
mkdir -p "$PCAP_DIR"

while sleep 60; do
    mapfile -t files < <(ls -1t "$PCAP_DIR"/*.pcap 2>/dev/null || true)
    if (( ${#files[@]} > RETENTION_COUNT )); then
        for old in "${files[@]:RETENTION_COUNT}"; do
            rm -f "$old"
        done
    fi
done
