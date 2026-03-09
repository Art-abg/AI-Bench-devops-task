#!/usr/bin/env bash
set -euo pipefail

cd /app

mkdir -p artifacts reports

python tools/validate_config.py --config configs/services.json
python tools/render_manifest.py --config configs/services.json --template deploy/deployment.tmpl --output artifacts/deployment.yaml
python tools/generate_report.py --config configs/services.json --manifest artifacts/deployment.yaml --out reports/deploy_report.json

echo "Pipeline finished successfully"
