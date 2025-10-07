#!/bin/bash
set -Eeuo pipefail

show_help() {
    cat <<'USAGE'
Usage: capture.sh [interface]

Start tcpdump on the given interface (default: eth0) and rotate PCAP files every
5 minutes. Files are stored in /opt/capture/pcaps/ with the format
YYYYmmdd-HHMMSS.pcap.
USAGE
}

if [[ ${1:-} == "--help" || ${1:-} == "-h" ]]; then
    show_help
    exit 0
fi

INTERFACE=${1:-eth0}
PCAP_DIR=/opt/capture/pcaps
ROTATE_SECONDS=${ROTATE_SECONDS:-300}
mkdir -p "$PCAP_DIR"

/opt/capture/rotate_pcap.sh &
ROTATE_PID=$!

trap 'kill $ROTATE_PID 2>/dev/null || true' EXIT

tcpdump -i "$INTERFACE" -s 0 -G "$ROTATE_SECONDS" -w "$PCAP_DIR/%Y%m%d-%H%M%S.pcap"
