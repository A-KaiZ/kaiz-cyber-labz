# Scenario playbook

## 01 – SSH Bruteforce

1. Ensure the lab is running: `make up`.
2. From the host, run `make attack NAME=01-ssh-bruteforce`.
3. Observe `/var/log/auth.log` inside `victim-ssh` or run `docker compose logs victim-ssh`.
4. Import detections with `make detect` and review the **SSH Bruteforce Candidates** saved search.
5. Capture a pcap: `make pcap` from another terminal and allow it to run during the attack.
6. Collect evidence: `telemetry/parsers/parse_authlog.py /opt/telemetry/auth.log --output ssh_events.csv`.
7. Mitigate by applying `blueteam/hardening/sshd_config.hard`.

**Flags to capture:**

* `telemetry/redteam/01-ssh-bruteforce/success.txt`
* `telemetry/redteam/01-ssh-bruteforce/session.txt`

## 02 – SQLi Webshell

1. Enable the risky feature: `ENABLE_RISKY=true docker compose up -d victim-web`.
2. Execute `make attack NAME=02-sqli-webshell`.
3. Confirm the upload in `telemetry/redteam/02-sqli-webshell/web_logs.txt`.
4. Run `make detect` to import the web dashboard objects.
5. Review the Sigma rule `blueteam/detections/sigma/web_sqli.yml` and map fields to OpenSearch.
6. Clean up by setting `ENABLE_RISKY=false` and restarting `victim-web`.

**Flags to capture:**

* `telemetry/redteam/02-sqli-webshell/probe.json`
* `telemetry/redteam/02-sqli-webshell/upload.html`
* SIEM saved object export showing SQLi indicators

> **Legal reminder:** Only exercise these techniques within Cyber Lab Foundry or
> environments where you have explicit authorization.
