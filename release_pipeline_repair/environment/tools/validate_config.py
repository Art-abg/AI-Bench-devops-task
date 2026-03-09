#!/usr/bin/env python3
import argparse
import json
import re
import sys


def validate_service(service: dict) -> list[str]:
    errors = []
    required_fields = ["name", "image", "tag", "replica_count"]
    for field in required_fields:
        if field not in service:
            errors.append(f"Missing required field: {field}")

    if "tag" in service:
        if not re.match(r"^\d+\.\d+$", str(service["tag"])):
            errors.append(f"Invalid version tag format for {service.get('name', '<unknown>')}: {service['tag']}")

    if "replica_count" in service:
        if not isinstance(service["replica_count"], int) or service["replica_count"] <= 0:
            errors.append(f"replica_count must be a positive integer for {service.get('name', '<unknown>')}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        data = json.load(f)

    services = data.get("services", [])
    all_errors: list[str] = []

    for service in services:
        all_errors.extend(validate_service(service))

    if all_errors:
        print("Validation failed:", file=sys.stderr)
        for e in all_errors:
            print(f" - {e}", file=sys.stderr)
        return 1

    print("Configuration validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
