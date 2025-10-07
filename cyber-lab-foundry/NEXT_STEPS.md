# Next steps for Cyber Lab Foundry

## 1. Ship actionable detections and dashboards
- Extend the OpenSearch shipper to enrich events with structured fields (e.g., `@timestamp`, `event.module`, `source.ip`) instead of raw message-only documents so saved searches and Sigma rules can pivot on them. The current implementation only stores the log line string, which limits correlation and breaks column displays that expect parsed fields. 【F:infra/docker/defender-siem/logshipper.py†L10-L47】
- Replace the placeholder dashboard export with visualizations that use the enriched fields (e.g., stacked area of failures over time, table of top sources). Right now the saved object payload has an empty `panelsJSON`, so the imported dashboard renders blank. 【F:blueteam/detections/elastic/dashboards.ndjson†L1-L1】

## 2. Tighten scenario guidance and automation
- Correct the SSH scenario evidence path to the actual auth log location under `telemetry/logs/victim-ssh/` so learners can run the parser without errors. 【F:docs/scenarios.md†L5-L24】
- Provide a helper (e.g., Makefile target or wrapper script) to toggle `ENABLE_RISKY` for the SQLi lab instead of requiring manual `docker compose` invocations. This would reduce user error when switching between safe and risky modes. 【F:docs/scenarios.md†L18-L31】

## 3. Add regression coverage
- Add automated tests that execute `make detect` (or its underlying import script) in a controlled environment to assert the dashboards import successfully and surface failures early. Currently no test exercises this workflow end-to-end. 【F:Makefile†L1-L36】
