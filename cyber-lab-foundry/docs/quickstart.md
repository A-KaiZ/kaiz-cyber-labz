# Quickstart

This walkthrough gets you from zero to first detection in under 10 minutes.

## 1. Launch the lab

```bash
make up
```

This builds the containers and creates the `labnet` network. Wait for the
`defender-siem` container to report "Green" in the logs.

## 2. Run the SSH bruteforce scenario

```bash
make attack NAME=01-ssh-bruteforce
```

The attacker container generates a password list, runs `brute_ssh.py`, and logs a
successful login. Review artifacts under `telemetry/redteam/01-ssh-bruteforce`.

## 3. Import detections

```bash
make detect
```

This loads Sigma-inspired saved searches and dashboards into OpenSearch.

## 4. Verify the alert

Open <http://localhost:5601> and load the **Cyber Lab Foundry Overview**
dashboard. You should see failed password bursts from the bruteforce run.

> **Safety reminder:** Keep the lab on localhost or an isolated host. Do not
> expose these services to production networks.
