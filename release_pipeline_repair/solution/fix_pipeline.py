#!/usr/bin/env python3
from pathlib import Path


def replace_in_file(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        return
    path.write_text(text.replace(old, new), encoding="utf-8")


def main() -> int:
    base = Path('/app')

    validate = base / 'tools' / 'validate_config.py'
    replace_in_file(validate, '"replica_count"', '"replicas"')
    replace_in_file(validate, 'r"^\\d+\\.\\d+$"', 'r"^\\d+\\.\\d+\\.\\d+$"')

    report = base / 'tools' / 'generate_report.py'
    replace_in_file(report, 'replica_count', 'replicas')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
