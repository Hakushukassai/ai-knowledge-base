#!/usr/bin/env python3
"""Create a candidate or add another observation, only on explicit invocation."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

from kb_common import metadata_from, parse_list, repository_root, search_entries


SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,79}$")


def clean_line(value: str) -> str:
    return " ".join(value.replace("\t", " ").split())


def candidate_path(raw: str, root: Path) -> Path:
    path = (root / raw).resolve()
    candidates = (root / "candidates").resolve()
    if path.parent != candidates or path.suffix != ".md":
        raise ValueError("既存候補は candidates/*.md を指定してください")
    if not path.is_file():
        raise ValueError(f"候補が見つかりません: {raw}")
    return path


def show_similar(query: str) -> None:
    results = search_entries(query, limit=5)
    if not results:
        print("類似候補は見つかりませんでした")
        return
    print("類似する可能性がある記録:")
    for result in results:
        entry = result["entry"]
        print(f"- {entry.relative_path} ({entry.status}, score={result['score']})")
        print(f"  {entry.title}")


def new_candidate(args: argparse.Namespace, root: Path) -> int:
    root = root.resolve()
    if not args.confirm_new:
        show_similar(args.title)
        print("新規作成する場合は内容を確認して --confirm-new を付けて再実行してください")
        return 2
    if not SLUG_RE.fullmatch(args.slug):
        raise ValueError("--slug は3〜80文字の小文字英数字とハイフンにしてください")

    date = dt.date.today().isoformat()
    path = root / "candidates" / f"{date}-{args.slug}.md"
    if path.exists():
        raise ValueError(f"既に存在します: {path.relative_to(root)}")

    tags = [clean_line(tag) for tag in args.tags.split(",") if clean_line(tag)]
    project = clean_line(args.project)
    verification = "verified" if args.source else "unverified"
    metadata_lines = [
        "status: candidate",
        "observed_count: 1",
        f"observed_in: [{project}]",
        f"tags: [{', '.join(tags)}]",
        f"date: {date}",
        f"verification: {verification}",
    ]
    if args.source:
        metadata_lines.extend((f"source_url: {args.source}", f"verified_at: {date}"))

    content = "\n".join(
        [
            f"# [候補] {clean_line(args.title)}",
            "",
            *metadata_lines,
            "",
            "## 何が起きたか",
            clean_line(args.summary),
            "",
            "## わかったこと・今の対応",
            clean_line(args.resolution),
            "",
            "## 詳しい経緯",
            args.details.strip() or "詳細はまだ記録されていない。",
            "",
            "## まだ確認できていないこと",
            args.unknown.strip() or "他の環境・プロジェクトで再現するか未確認。",
            "",
        ]
    )
    path.write_text(content, encoding="utf-8")
    print(f"作成しました: {path.relative_to(root).as_posix()}")
    return 0


def observe_existing(args: argparse.Namespace, root: Path) -> int:
    root = root.resolve()
    path = candidate_path(args.path, root)
    content = path.read_text(encoding="utf-8")
    metadata = metadata_from(content)
    count = int(metadata.get("observed_count", "1")) + 1
    projects = parse_list(metadata.get("observed_in", ""))
    project = clean_line(args.project)
    if project not in projects:
        projects.append(project)

    content = re.sub(
        r"^observed_count:\s*\d+\s*$",
        f"observed_count: {count}",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    content = re.sub(
        r"^observed_in:\s*\[.*?\]\s*$",
        f"observed_in: [{', '.join(projects)}]",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    note = clean_line(args.note)
    content = content.rstrip() + f"\n\n({dt.date.today().isoformat()}、{project}で再確認) {note}\n"
    path.write_text(content, encoding="utf-8")
    print(f"観測を追加しました: {path.relative_to(root).as_posix()} (observed_count: {count})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="明示的な依頼時だけKB候補を記録する")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="保存前に類似記録を確認する")
    check.add_argument("query")

    new = subparsers.add_parser("new", help="新しい候補を作成する")
    new.add_argument("--slug", required=True)
    new.add_argument("--title", required=True)
    new.add_argument("--project", required=True)
    new.add_argument("--tags", required=True, help="カンマ区切り")
    new.add_argument("--summary", required=True)
    new.add_argument("--resolution", required=True)
    new.add_argument("--details", default="")
    new.add_argument("--unknown", default="")
    new.add_argument("--source", default="", help="確認に使った一次情報URL")
    new.add_argument("--confirm-new", action="store_true")

    observe = subparsers.add_parser("observe", help="既存候補の観測回数を増やす")
    observe.add_argument("path")
    observe.add_argument("--project", required=True)
    observe.add_argument("--note", required=True)

    args = parser.parse_args()
    root = repository_root()
    try:
        if args.command == "check":
            show_similar(args.query)
            return 0
        if args.command == "new":
            return new_candidate(args, root)
        return observe_existing(args, root)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
