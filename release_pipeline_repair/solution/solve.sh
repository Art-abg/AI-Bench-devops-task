#!/usr/bin/env bash
set -euo pipefail

python /solution/fix_pipeline.py
bash /app/ci/run_pipeline.sh
