from __future__ import annotations

import argparse
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from kb_capture import new_candidate, observe_existing  # noqa: E402
from kb_common import search_entries  # noqa: E402
from migrate_claude_settings import cleaned_settings  # noqa: E402


def write_entry(root: Path, category: str, name: str, title: str, body: str) -> Path:
    directory = root / category
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(
        f"# {title}\n\nstatus: {category}\ntags: [godot, test]\n\n## 何が起きたか\n{body}\n",
        encoding="utf-8",
    )
    return path


class SearchTests(unittest.TestCase):
    def test_confirmed_rule_ranks_above_same_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entry(root, "rules", "rule.md", "Godot headless exit code", "script error")
            write_entry(root, "candidates", "candidate.md", "Godot headless exit code", "script error")
            results = search_entries("Godot headless exit code", root=root)
            self.assertEqual(results[0]["entry"].relative_path, "rules/rule.md")


class CaptureTests(unittest.TestCase):
    def test_new_candidate_is_explicitly_unverified(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "candidates").mkdir()
            args = argparse.Namespace(
                slug="godot-exit-code",
                title="Godotの終了コード",
                project="sample-game",
                tags="godot,testing",
                summary="スクリプトエラーでも終了コードが0になった。",
                resolution="ログ本文も確認する。",
                details="headless実行で確認。",
                unknown="別バージョンは未確認。",
                source="",
                confirm_new=True,
            )
            self.assertEqual(new_candidate(args, root), 0)
            created = next((root / "candidates").glob("*.md"))
            content = created.read_text(encoding="utf-8")
            self.assertIn("verification: unverified", content)

    def test_observe_increments_count_and_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "candidates" / "finding.md"
            path.parent.mkdir()
            path.write_text(
                "# [候補] 発見\n\nstatus: candidate\nobserved_count: 1\n"
                "observed_in: [alpha]\ntags: [test]\ndate: 2026-08-31\n\n"
                "## 何が起きたか\n問題\n\n## わかったこと・今の対応\n対処\n",
                encoding="utf-8",
            )
            args = argparse.Namespace(path="candidates/finding.md", project="beta", note="再現した")
            self.assertEqual(observe_existing(args, root), 0)
            content = path.read_text(encoding="utf-8")
            self.assertIn("observed_count: 2", content)
            self.assertIn("observed_in: [alpha, beta]", content)


class MigrationTests(unittest.TestCase):
    def test_only_legacy_kb_hooks_are_removed(self) -> None:
        settings = {
            "theme": "dark",
            "permissions": {"allow": ["Bash(bash ~/knowledge-base/scripts/generate_stats.sh:*)", "Bash(npm test:*)"]},
            "hooks": {
                "SessionEnd": [
                    {"hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/scan_and_push.py"}]},
                    {"hooks": [{"type": "command", "command": "notify-send done"}]},
                ]
            },
        }
        cleaned = cleaned_settings(json.loads(json.dumps(settings)))
        self.assertEqual(cleaned["permissions"]["allow"], ["Bash(npm test:*)"])
        self.assertEqual(cleaned["hooks"]["SessionEnd"][0]["hooks"][0]["command"], "notify-send done")
        self.assertEqual(cleaned["theme"], "dark")


if __name__ == "__main__":
    unittest.main()
