# Architecture and threat model

## Components

* **attacker** – Debian-based workstation with offensive tooling.
* **victim-ssh** – OpenSSH server with configurable rate limiting.
* **victim-web** – Flask application with optional risky upload functionality.
* **mitm-gateway** – Passive capture host running tcpdump/tshark.
* **defender-siem** – OpenSearch + Dashboards with preloaded visualizations.

## Data flows

1. The attacker interacts with victim services over the `labnet` bridge.
2. The MITM gateway mirrors traffic for packet capture.
3. Victim logs (auth, app) are shipped into the SIEM via filebeat-like polling
   scripts embedded in the container.
4. Analysts access Dashboards on port 5601.

## Ports

| Service | Container port | Host default |
| --- | --- | --- |
| victim-web | 5000 | 8080 |
| victim-ssh | 22 | 2222 |
| defender-siem (API) | 9200 | 9200 |
| defender-siem (Dashboards) | 5601 | 5601 |

## Threat model (STRIDE)

| Threat | Considerations | Mitigations |
| --- | --- | --- |
| Spoofing | Lab services share a bridge network. | Static hostnames and `/etc/hosts` entries in attacker container. |
| Tampering | Attack scripts could alter telemetry. | PCAPs stored on separate volume; defenders validate hashes. |
| Repudiation | Attackers may deny actions. | Logs centralized in SIEM with timestamps. |
| Information disclosure | Sensitive data exists only within lab network. | Default `ENABLE_RISKY=false`, TLS guidance in hardening docs. |
| Denial of service | Resource-heavy scans degrade hosts. | Makefiles allow quick teardown/rebuild. |
| Elevation of privilege | Attackers escalate via webshell. | Cleanup guides reset states and hardening configs reduce risk. |

See [`docs/diagrams/topology.mmd`](diagrams/topology.mmd) for the Mermaid diagram
used in presentations and README embeds.
