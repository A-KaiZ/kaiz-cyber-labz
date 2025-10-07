# Scenario 01: SSH Bruteforce

## Learning goals

* Craft targeted password lists and tune concurrency for noisy authentication attacks.
* Observe how bruteforce activity surfaces in `/var/log/auth.log` and the SIEM dashboard.
* Capture artifacts (pcap, logs) and perform credential rotation.

## MITRE ATT&CK techniques

* T1110.001 – Brute Force: Password Guessing
* T1078 – Valid Accounts

## Estimated time

~15 minutes including review of logs and mitigations.

## Cleanup steps

1. Rotate the `victim` user password using `passwd victim` on `victim-ssh`.
2. Set `ENABLE_FAIL2BAN=true` via `docker compose` overrides if continuing exercises.
3. Archive or remove `telemetry/redteam/01-ssh-bruteforce` artifacts when done.
