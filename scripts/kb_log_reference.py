#!/usr/bin/env python3
"""Record a knowledge item only after it was actually used."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

from kb_common import CATEGORIES, repository_root


def main() -> int:
    parser = argparse.ArgumentParser(description="実際に役立ったKB参照を記録する")
    parser.add_argument("path")
    parser.add_argument("--verdict", choices=("役立った", "参考程度", "不明"), required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()

    root = repository_root()
    path = (root / args.path).resolve()
    try:
        relative = path.relative_to(root)
    except ValueError:
        parser.error("KB外のパスは記録できません")
    if relative.parts[0] not in CATEGORIES or not path.is_file():
        parser.error("rules/candidates/incidents/external-skill-imports 内の実在ファイルを指定してください")

    reason = " ".join(args.reason.replace("\t", " ").split())[:80]
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"{timestamp}\t{relative.parts[0]}\t{path.name}\t{args.verdict}\t{reason}\n"
    with (root / ".reference_usage.log").open("a", encoding="utf-8") as handle:
        handle.write(line)
    print(f"参照実績を記録しました: {relative.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
