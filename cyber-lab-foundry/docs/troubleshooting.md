# Troubleshooting

## Docker permission errors (WSL2)

Add your user to the `docker` group and restart your terminal:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## SIEM takes too long to start

OpenSearch can require up to 90 seconds on first launch. Check logs with
`docker compose logs defender-siem`.

## Packet capture not writing files

Ensure `mitm-gateway` has the `NET_ADMIN` capability and run `make pcap` from the
host. Verify permissions on `telemetry/capture/pcaps/`.

## `ENABLE_RISKY` ignored on victim-web

Compose caches environment variables. Restart the container explicitly:

```bash
docker compose up -d --force-recreate victim-web
```

## Windows path issues

When using WSL2, clone the repository inside the Linux filesystem (`~/projects`).
Sharing from the Windows side can cause slow file I/O.
