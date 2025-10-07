# Example topology

```
attacker (10.20.0.10)
   │
   ├──> mitm-gateway (10.20.0.5)
   │        └── captures mirrored traffic
   ├──> victim-ssh (10.20.0.20)
   └──> victim-web (10.20.0.30)

victim services forward logs to defender-siem (10.20.0.40)
```

All services reside on the `labnet` bridge. Traffic can be mirrored through the
MITM gateway to observe activity without interfering with lab exercises.
