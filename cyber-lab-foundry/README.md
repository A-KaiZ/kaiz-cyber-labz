# Cyber Lab Foundry

[![CI](https://github.com/example/cyber-lab-foundry/actions/workflows/ci.yml/badge.svg)](https://github.com/example/cyber-lab-foundry/actions/workflows/ci.yml)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A reproducible, containerized cybersecurity range for red and blue team skill building on your own workstation.

```
   ┌──────────────┐     ┌──────────────┐      ┌──────────────┐
   │  attacker    │────▶│ mitm-gateway │─────▶│ victim-*     │
   └──────────────┘     └──────────────┘      └──────────────┘
            │                                   │
            └──────────────┬────────────────────┘
                           ▼
                    defender-siem
```

[Mermaid topology diagram](docs/diagrams/topology.mmd)

## Project vision

Cyber Lab Foundry spins up an isolated mini-network with vulnerable services, captures full telemetry, and guides you through scripted attacks and detections. It is designed for localhost or air-gapped usage only.

## Quickstart

```bash
make up
make attack NAME=01-ssh-bruteforce
make detect
```

## Safety and legality

* **Local use only.** The lab binds to localhost-scoped networks and is not meant for exposure to the public internet.
* **Authorization required.** Use the tooling only against the containers provided by this project unless you have explicit permission.
* Dangerous features (such as the vulnerable web upload) are disabled by default and must be consciously enabled per scenario guide.

## Choose your path

| Path | Description | Suggested first steps |
| --- | --- | --- |
| 🔴 Red Team | Offensive tradecraft to compromise lab targets and collect proof. | `make attack NAME=01-ssh-bruteforce`, read `redteam/scenarios/*/notes.md` |
| 🔵 Blue Team | Detection, hardening, and response with OpenSearch dashboards. | `make detect`, apply `blueteam/hardening/*`, explore `docs/detections.md` |

## Scenarios

| ID | Name | Difficulty | Learning objectives |
| --- | --- | --- | --- |
| 01 | SSH Bruteforce | Beginner | Use `brute_ssh.py`, observe auth.log noise, trigger Sigma rule, rotate SSH keys. |
| 02 | SQLi Webshell | Intermediate | Exploit SQL injection, deploy webshell under supervision, confirm SIEM alert, practice containment. |

## Telemetry & evidence

* `telemetry/capture/capture.sh` mirrors traffic from the MITM gateway, rotating pcaps using timestamped filenames.
* `telemetry/parsers/parse_authlog.py` converts SSH logs into CSV for quick triage.

## Troubleshooting FAQ

<details>
<summary>Docker complains about permissions on WSL2</summary>
Ensure Docker Desktop is running and that your user is part of the `docker` group. On first run, restart the terminal after adding the group membership.
</details>

<details>
<summary>Ports already in use</summary>
Set overrides in `compose.override.example.yml` or via `LAB_WEB_PORT`, `LAB_SIEM_PORT`, and `LAB_DASHBOARD_PORT` environment variables.
</details>

<details>
<summary>SIEM dashboards are empty</summary>
Run `make detect` to re-import saved objects, then refresh the index pattern in OpenSearch Dashboards.
</details>

## Documentation

Comprehensive docs live in [`docs/`](docs/). Start with [`docs/quickstart.md`](docs/quickstart.md) for a ten-minute tour.

## Contributing

We welcome contributions that improve safety, documentation, and learning effectiveness. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) and review our [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE).

