#!/bin/bash
set -Eeuo pipefail

show_help() {
    cat <<USAGE
Usage: run_scenario.sh <scenario-id>

Execute the scripted steps for a red team scenario. Available scenarios:
USAGE
    find /opt/redteam/scenarios -maxdepth 1 -mindepth 1 -type d -printf "  %f\n" | sort
}

if [[ ${1:-} == "--help" || ${1:-} == "-h" || $# -eq 0 ]]; then
    show_help
    exit 0
fi

SCENARIO="$1"
SCENARIO_DIR="/opt/redteam/scenarios/${SCENARIO}"

if [[ ! -d "$SCENARIO_DIR" ]]; then
    echo "Unknown scenario: $SCENARIO" >&2
    exit 1
fi

RUNNER="$SCENARIO_DIR/run.sh"
if [[ ! -x "$RUNNER" ]]; then
    echo "Scenario script is missing or not executable: $RUNNER" >&2
    exit 1
fi

exec "$RUNNER"
