#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    config_data = json.loads(Path(args.config).read_text(encoding="utf-8"))
    services = config_data.get("services", [])

    report = {
        "status": "ready",
        "service_count": len(services),
        "total_replicas": sum(s.get("replica_count", 0) for s in services),
        "images": sorted([f"{s['image']}:{s['tag']}" for s in services]),
        "manifest_size": len(Path(args.manifest).read_text(encoding="utf-8").splitlines()),
    }

    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report written to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
