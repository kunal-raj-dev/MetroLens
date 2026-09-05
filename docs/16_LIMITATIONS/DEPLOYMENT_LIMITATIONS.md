# Deployment, Hardware & Operational Limitations

## Purpose
Documents hardware minimums, thermal throttling considerations, and operational constraints for edge deployments.

## Documented Deployment Boundaries
1. **Minimum Hardware Baseline:** Devices require at least an 8-core CPU and 8 GB RAM to ensure $\le 5.0\text{ s}$ per-package inspection latency without thermal throttling.
2. **Camera Focus Limitations:** Devices lacking macro focus support or with dirty camera lenses fail the Image Quality Gate and require lens cleaning or manual re-focus.
3. **Database Concurrency on Edge:** Standalone edge installations use SQLite with Write-Ahead Logging (WAL); concurrent multi-process writes are supported up to 5 concurrent worker threads per mobile station.
