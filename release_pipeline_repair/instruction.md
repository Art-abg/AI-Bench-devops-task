# Repair the Release Pipeline

A release pipeline for a Python microservice is broken. Your goal is to repair the pipeline so that deployment artifacts and a release report are generated correctly.

## Context
You are working inside `/app`.

The pipeline entrypoint is:

```bash
bash /app/ci/run_pipeline.sh
```

Right now this pipeline fails and/or generates invalid outputs.

## Requirements
1. Make the pipeline complete successfully (exit code 0).
2. Ensure it generates:
   - `/app/artifacts/deployment.yaml`
   - `/app/reports/deploy_report.json`
3. The generated report must reflect the actual configuration values (not hardcoded), and include accurate aggregate metadata for services in `/app/configs/services.json`.
4. Keep the existing project structure. Fix code/config/scripts as needed.

## Notes
- Do not add test-only shortcuts.
- Do not rely on external network services.
- All work must remain under `/app`.
