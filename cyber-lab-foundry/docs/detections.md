# Detections

## MITRE ATT&CK mapping

| Technique | Description | Coverage |
| --- | --- | --- |
| T1110.001 | Brute Force: Password Guessing | `blueteam/detections/sigma/ssh_bruteforce.yml`, saved search `ssh-bruteforce-search` |
| T1190 | Exploit Public-Facing Application | `blueteam/detections/sigma/web_sqli.yml` |
| T1505.003 | Web Shell | OpenSearch dashboard `cyber-lab-overview` panels |

## Import procedure

Run `make detect` to execute `/opt/detect/import.sh` inside the SIEM container.
This performs the following steps:

1. Waits for OpenSearch to accept connections on port 9200.
2. Imports saved searches and dashboards from `blueteam/detections/elastic`.
3. Prints the URLs to access in OpenSearch Dashboards.

## Customizing rules

Sigma files live in `blueteam/detections/sigma/`. Use
[`sigmac`](https://github.com/SigmaHQ/sigma) to convert them into query
languages supported by your tooling.

## Alert response

* Investigate offending IP addresses using `telemetry/parsers/parse_authlog.py`.
* Contain via `blueteam/response/blocklist_updater.py --block <ip>`.
* Document findings in your incident log.
