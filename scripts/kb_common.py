"""Shared, dependency-free helpers for the knowledge-base tools."""

from __future__ import annotations

import os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


CATEGORIES = ("rules", "candidates", "incidents", "external-skill-imports")
CATEGORY_WEIGHT = {
    "rules": 1.45,
    "incidents": 1.20,
    "candidates": 1.00,
    "external-skill-imports": 0.80,
}


def repository_root() -> Path:
    override = os.environ.get("KB_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text).casefold()


def parse_list(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [part.strip() for part in value.split(",") if part.strip()]


def metadata_from(content: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in content.splitlines():
        if line.startswith("##"):
            break
        match = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if match:
            metadata[match.group(1)] = match.group(2).strip()
    return metadata


def first_title(content: str, fallback: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return re.sub(r"^\[[^\]]+\]\s*", "", line[2:].strip())
    return fallback


def extract_section(content: str, names: tuple[str, ...], max_chars: int = 240) -> str:
    for name in names:
        match = re.search(
            rf"^##\s*{re.escape(name)}\s*$\n(.*?)(?=^##\s|\Z)",
            content,
            re.MULTILINE | re.DOTALL,
        )
        if match:
            text = " ".join(match.group(1).split())
            return text[:max_chars] + ("…" if len(text) > max_chars else "")
    return ""


@dataclass(frozen=True)
class Entry:
    path: Path
    relative_path: str
    category: str
    title: str
    metadata: dict[str, str]
    summary: str
    resolution: str
    content: str

    @property
    def status(self) -> str:
        return self.metadata.get("status", self.category)

    @property
    def tags(self) -> list[str]:
        return parse_list(self.metadata.get("tags", ""))


def load_entries(root: Path | None = None) -> list[Entry]:
    root = root or repository_root()
    entries: list[Entry] = []
    for category in CATEGORIES:
        directory = root / category
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            content = path.read_text(encoding="utf-8")
            entries.append(
                Entry(
                    path=path,
                    relative_path=path.relative_to(root).as_posix(),
                    category=category,
                    title=first_title(content, path.name),
                    metadata=metadata_from(content),
                    summary=extract_section(content, ("何が起きたか", "問題", "ルール")),
                    resolution=extract_section(
                        content,
                        ("わかったこと・今の対応", "解決", "判断基準"),
                    ),
                    content=content,
                )
            )
    return entries


ASCII_TOKEN = re.compile(r"[a-z0-9][a-z0-9_.:/+\-]*")
CJK_SEQUENCE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]{2,}")


def query_features(query: str) -> tuple[list[str], list[str]]:
    normalized = normalize(query)
    ascii_terms = sorted(set(ASCII_TOKEN.findall(normalized)), key=len, reverse=True)
    cjk_ngrams: set[str] = set()
    for sequence in CJK_SEQUENCE.findall(normalized):
        if len(sequence) <= 4:
            cjk_ngrams.add(sequence)
        for size in (2, 3, 4):
            for index in range(0, len(sequence) - size + 1):
                cjk_ngrams.add(sequence[index:index + size])
    return ascii_terms, sorted(cjk_ngrams, key=len, reverse=True)


def score_entry(entry: Entry, query: str) -> tuple[float, list[str]]:
    query_norm = normalize(query).strip()
    title = normalize(entry.title)
    tags = normalize(" ".join(entry.tags))
    summaries = normalize(f"{entry.summary} {entry.resolution}")
    body = normalize(entry.content)
    ascii_terms, cjk_ngrams = query_features(query_norm)
    score = 0.0
    matched: list[str] = []

    if query_norm and query_norm in body:
        score += 12.0

    for term in ascii_terms:
        term_score = 0.0
        if term in title:
            term_score += 8.0
        if term in tags:
            term_score += 6.0
        if term in summaries:
            term_score += 3.0
        if term in body:
            term_score += 1.0
        if term_score:
            score += term_score
            matched.append(term)

    cjk_score = 0.0
    cjk_matches: list[str] = []
    for gram in cjk_ngrams:
        gram_score = 0.0
        if gram in title:
            gram_score += 1.6
        if gram in tags:
            gram_score += 1.2
        if gram in summaries:
            gram_score += 0.8
        elif gram in body:
            gram_score += 0.2
        if gram_score:
            cjk_score += gram_score
            if len(gram) >= 3 and len(cjk_matches) < 8:
                cjk_matches.append(gram)
    score += min(cjk_score, 24.0)
    matched.extend(cjk_matches)

    return score * CATEGORY_WEIGHT.get(entry.category, 1.0), matched[:12]


def search_entries(query: str, limit: int = 5, root: Path | None = None) -> list[dict]:
    ranked = []
    for entry in load_entries(root):
        score, matched = score_entry(entry, query)
        if score <= 0:
            continue
        ranked.append({"entry": entry, "score": round(score, 2), "matched": matched})
    ranked.sort(key=lambda item: (-item["score"], item["entry"].relative_path))
    return ranked[:limit]
