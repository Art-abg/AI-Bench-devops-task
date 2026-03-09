#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    services = config.get("services", [])

    template_text = Path(args.template).read_text(encoding="utf-8")

    docs: list[str] = []
    for svc in services:
        docs.append(
            template_text.format(
                name=svc["name"],
                replicas=svc["replicas"],
                image=svc["image"],
                version=svc["tag"],
            )
        )

    rendered = "\n---\n".join(docs) + "\n"
    Path(args.output).write_text(rendered, encoding="utf-8")

    print(f"Manifest written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
