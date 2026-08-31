#!/usr/bin/env python3
"""Search the Markdown knowledge base without embeddings or external services."""

from __future__ import annotations

import argparse
import json

from kb_common import search_entries


def as_json(result: dict) -> dict:
    entry = result["entry"]
    return {
        "path": entry.relative_path,
        "category": entry.category,
        "status": entry.status,
        "title": entry.title,
        "tags": entry.tags,
        "score": result["score"],
        "matched": result["matched"],
        "summary": entry.summary,
        "resolution": entry.resolution,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="KBをタイトル・タグ・本文から検索する")
    parser.add_argument("query", help="調べたい問題、エラー、技術用語")
    parser.add_argument("--limit", type=int, default=5, help="最大表示件数 (default: 5)")
    parser.add_argument("--json", action="store_true", help="JSONで出力する")
    args = parser.parse_args()

    if args.limit < 1 or args.limit > 20:
        parser.error("--limit は1〜20にしてください")

    results = search_entries(args.query, args.limit)
    if args.json:
        print(json.dumps([as_json(item) for item in results], ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("関連する記録は見つかりませんでした")
        return 1

    for index, result in enumerate(results, 1):
        entry = result["entry"]
        print(f"{index}. [{entry.status}] {entry.title}")
        print(f"   path: {entry.relative_path}")
        print(f"   score: {result['score']}")
        if entry.tags:
            print(f"   tags: {', '.join(entry.tags)}")
        if entry.summary:
            print(f"   概要: {entry.summary}")
        if entry.resolution:
            print(f"   対応: {entry.resolution}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
