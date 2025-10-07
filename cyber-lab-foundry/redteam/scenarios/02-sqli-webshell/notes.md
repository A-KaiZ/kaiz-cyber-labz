# Scenario 02: SQL Injection to Webshell

## Learning goals

* Identify injectable parameters and craft authentication bypass payloads.
* Abuse insecure file uploads to gain remote command execution.
* Capture forensic traces (logs, pcaps, saved dashboards) for incident reports.

## MITRE ATT&CK techniques

* T1190 – Exploit Public-Facing Application
* T1059 – Command and Scripting Interpreter
* T1505.003 – Web Shell

## Estimated time

~25 minutes including enabling risky mode and reviewing telemetry.

## Cleanup steps

1. Disable risky mode by setting `ENABLE_RISKY=false` and restarting `victim-web`.
2. Delete uploaded webshells from `/tmp/uploads` inside the container.
3. Review `blueteam/response/blocklist_updater.py` to contain suspicious IPs.
