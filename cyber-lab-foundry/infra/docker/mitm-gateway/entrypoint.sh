#!/bin/bash
set -Eeuo pipefail

if [[ $# -eq 0 ]]; then
    echo "MITM gateway ready. Use capture scripts from telemetry/capture."
    exec /bin/bash
fi
exec "$@"
