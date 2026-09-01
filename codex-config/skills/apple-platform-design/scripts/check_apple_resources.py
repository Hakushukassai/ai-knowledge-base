#!/usr/bin/env python3
"""Inventory user-provided Apple Design Resources without modifying them."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys


SUPPORTED_SUFFIXES = {
    ".fig",
    ".sketch",
    ".psd",
    ".svg",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".json",
    ".zip",
    ".dmg",
    ".pkg",
}

PLATFORM_TERMS = {
    "ios": ("ios", "iphone"),
    "ipados": ("ipados", "ipad"),
    "macos": ("macos", "mac os", "mac_"),
    "watchos": ("watchos", "watch"),
    "tvos": ("tvos", "apple tv"),
    "visionos": ("visionos", "vision pro"),
    "shared": ("sf symbols", "app icon", "color", "font", "typography"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory a licensed, user-controlled Apple Design Resources directory."
    )
    parser.add_argument(
        "--root",
        help="Explicit resource directory. Falls back to APPLE_DESIGN_RESOURCES_DIR.",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=5000,
        help="Maximum supported files to report before stopping (default: 5000).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return a nonzero exit code when no supported resource files are found.",
    )
    return parser.parse_args()


def resolve_root(raw_root: str | None) -> Path:
    value = raw_root or os.environ.get("APPLE_DESIGN_RESOURCES_DIR")
    if not value:
        raise ValueError(
            "Set --root or APPLE_DESIGN_RESOURCES_DIR to one explicit Apple resource directory."
        )
    root = Path(value).expanduser().resolve()
    if root == Path(root.anchor):
        raise ValueError("Refusing to scan a filesystem root; provide a dedicated resource directory.")
    if not root.exists():
        raise ValueError(f"Resource directory does not exist: {root}")
    if not root.is_dir():
        raise ValueError(f"Resource path is not a directory: {root}")
    return root


def classify(relative_path: str) -> list[str]:
    lowered = relative_path.lower().replace("-", " ")
    matches = [
        platform
        for platform, terms in PLATFORM_TERMS.items()
        if any(term in lowered for term in terms)
    ]
    return matches or ["unclassified"]


def inventory(root: Path, max_files: int) -> dict[str, object]:
    if max_files < 1:
        raise ValueError("--max-files must be at least 1.")

    files: list[dict[str, object]] = []
    counts: dict[str, int] = {}
    truncated = False

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        if len(files) >= max_files:
            truncated = True
            break
        relative = str(path.relative_to(root))
        platforms = classify(relative)
        files.append(
            {
                "path": relative,
                "suffix": path.suffix.lower(),
                "bytes": path.stat().st_size,
                "platforms": platforms,
            }
        )
        for platform in platforms:
            counts[platform] = counts.get(platform, 0) + 1

    return {
        "root": str(root),
        "supported_file_count": len(files),
        "platform_counts": dict(sorted(counts.items())),
        "truncated": truncated,
        "files": files,
        "notice": (
            "Inventory only. File presence does not establish license permission; "
            "consult the Apple Design Resources License for the intended use."
        ),
    }


def main() -> int:
    args = parse_args()
    try:
        root = resolve_root(args.root)
        report = inventory(root, args.max_files)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        return 2

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.strict and report["supported_file_count"] == 0:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
