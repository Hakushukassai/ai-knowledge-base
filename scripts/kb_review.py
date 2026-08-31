#!/usr/bin/env python3
"""Produce a small, read-only curation report for the candidate backlog."""

from __future__ import annotations

import argparse
import datetime as dt
import json

from kb_common import load_entries, parse_list


def review_data(stale_days: int) -> dict:
    today = dt.date.today()
    entries = load_entries()
    candidates = [entry for entry in entries if entry.category == "candidates"]
    ready = []
    stale = []
    unverified = []
    verification_unknown = []

    for entry in candidates:
        count = int(entry.metadata.get("observed_count", "1"))
        projects = set(parse_list(entry.metadata.get("observed_in", "")))
        endorsed = entry.metadata.get("endorsed", "").casefold() == "true"
        reasons = []
        if count >= 3:
            reasons.append(f"observed_count={count}")
        if len(projects) >= 2:
            reasons.append(f"projects={len(projects)}")
        if endorsed:
            reasons.append("endorsed")
        if reasons:
            ready.append({"path": entry.relative_path, "title": entry.title, "reasons": reasons})

        date_raw = entry.metadata.get("date")
        try:
            age = (today - dt.date.fromisoformat(date_raw)).days
        except (TypeError, ValueError):
            age = None
        if age is not None and age >= stale_days:
            stale.append({"path": entry.relative_path, "title": entry.title, "days": age})

        verification = entry.metadata.get("verification")
        if verification == "unverified":
            unverified.append({"path": entry.relative_path, "title": entry.title})
        elif not verification:
            verification_unknown.append({"path": entry.relative_path, "title": entry.title})

    return {
        "counts": {
            "rules": sum(entry.category == "rules" for entry in entries),
            "candidates": len(candidates),
            "incidents": sum(entry.category == "incidents" for entry in entries),
            "external_skill_imports": sum(
                entry.category == "external-skill-imports" for entry in entries
            ),
        },
        "promotion_ready": ready,
        "stale": stale,
        "explicitly_unverified": unverified,
        "legacy_verification_unknown": verification_unknown,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="候補の整理対象を読み取り専用で確認する")
    parser.add_argument("--stale-days", type=int, default=90)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    data = review_data(args.stale_days)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    counts = data["counts"]
    print(
        "KB: "
        f"rules={counts['rules']} candidates={counts['candidates']} "
        f"incidents={counts['incidents']} external={counts['external_skill_imports']}"
    )
    print(f"\n昇格を検討できる候補: {len(data['promotion_ready'])}件")
    for item in data["promotion_ready"]:
        print(f"- {item['path']} ({', '.join(item['reasons'])})")
    print(f"\n{args.stale_days}日以上前の候補: {len(data['stale'])}件")
    for item in data["stale"][:20]:
        print(f"- {item['path']} ({item['days']}日)")
    print(f"\n明示的に未検証: {len(data['explicitly_unverified'])}件")
    print(f"旧形式で検証状態不明: {len(data['legacy_verification_unknown'])}件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
