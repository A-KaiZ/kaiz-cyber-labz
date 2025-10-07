#!/bin/bash
set -Eeuo pipefail

cat /etc/motd

if [[ ${DEVCONTAINER:-false} == "true" ]]; then
    exec /bin/bash
fi

exec "$@"
