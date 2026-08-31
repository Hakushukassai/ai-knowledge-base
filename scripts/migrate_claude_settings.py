#!/usr/bin/env python3
"""Remove only the legacy knowledge-base hooks from Claude settings."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


MARKERS = (
    "knowledge-base",
    "scan_and_push.py",
    "archive_stale_candidates.py",
    "print_unskilled_rules.py",
    "log_skill_usage.py",
    "generate_stats.sh",
    ".skill_effectiveness.log",
    ".reference_usage.log",
)


def belongs_to_legacy_kb(value: object) -> bool:
    serialized = json.dumps(value, ensure_ascii=False)
    return any(marker in serialized for marker in MARKERS)


def cleaned_settings(data: dict) -> dict:
    result = json.loads(json.dumps(data))
    permissions = result.get("permissions")
    if isinstance(permissions, dict):
        allow = permissions.get("allow")
        if isinstance(allow, list):
            permissions["allow"] = [item for item in allow if not belongs_to_legacy_kb(item)]
            if not permissions["allow"]:
                permissions.pop("allow", None)
        if not permissions:
            result.pop("permissions", None)

    hooks = result.get("hooks")
    if isinstance(hooks, dict):
        cleaned_hooks = {}
        for event, groups in hooks.items():
            if not isinstance(groups, list):
                cleaned_hooks[event] = groups
                continue
            kept_groups = []
            for group in groups:
                if not isinstance(group, dict):
                    if not belongs_to_legacy_kb(group):
                        kept_groups.append(group)
                    continue
                group_copy = dict(group)
                nested = group_copy.get("hooks")
                if isinstance(nested, list):
                    group_copy["hooks"] = [hook for hook in nested if not belongs_to_legacy_kb(hook)]
                    if group_copy["hooks"]:
                        kept_groups.append(group_copy)
                elif not belongs_to_legacy_kb(group_copy):
                    kept_groups.append(group_copy)
            if kept_groups:
                cleaned_hooks[event] = kept_groups
        if cleaned_hooks:
            result["hooks"] = cleaned_hooks
        else:
            result.pop("hooks", None)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="旧KB SessionEndフックだけを安全に削除する")
    parser.add_argument(
        "--settings",
        type=Path,
        default=Path.home() / ".claude" / "settings.json",
    )
    parser.add_argument("--apply", action="store_true", help="バックアップ後に変更を保存する")
    args = parser.parse_args()

    path = args.settings.expanduser()
    if not path.exists():
        print(f"設定ファイルはありません。変更不要: {path}")
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    cleaned = cleaned_settings(data)
    if cleaned == data:
        print("旧KBフックは見つかりませんでした")
        return 0
    if not args.apply:
        print("旧KBフックが見つかりました。--apply でバックアップ後に削除できます")
        return 1

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.name}.kb-backup-{timestamp}")
    backup.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"旧KBフックを削除しました。バックアップ: {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
