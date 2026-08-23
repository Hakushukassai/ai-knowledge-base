#!/bin/bash
# knowledge-base/ の中身を数値化して docs/stats.json と docs/stats-data.js に出力する
# 使い方: bash scripts/generate_stats.sh
# Claude Code の SessionEnd hook (/clear 時) から自動実行される想定
#
# 前回実行時との差分(新しく増えたファイル)を docs/.manifest.json で
# 記憶しておき、その差分から「今回の変更」を一言サマリーとして履歴に残す。

set -e
cd "$(dirname "$0")/.."

export KB_DIR="$HOME/knowledge-base"
export OUT="docs/stats.json"
export MANIFEST="docs/.manifest.json"
export NOW="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

python3 << 'PYEOF'
import json
import os
import re
import glob
from datetime import datetime

kb_dir = os.environ['KB_DIR']
out_path = os.environ['OUT']
manifest_path = os.environ['MANIFEST']
now = os.environ['NOW']
now_dt = datetime.strptime(now, '%Y-%m-%dT%H:%M:%SZ')

CATEGORY_LABEL = {'rules': 'ルール', 'candidates': '候補', 'incidents': '事例'}
STALE_DAYS = 30  # 候補がこの日数以上動きなしなら「放置」とみなす


def files_in(category):
    return sorted(glob.glob(os.path.join(kb_dir, category, '*.md')))


def count_chars(paths):
    total = 0
    for p in paths:
        try:
            with open(p, encoding='utf-8') as f:
                total += len(f.read())
        except OSError:
            pass
    return total


def first_title(path):
    """ファイルの最初の見出し行(# で始まる行)を一言タイトルとして取り出す。
    見出しに既に [候補] 等の印が付いていれば、二重表示にならないよう外す。"""
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    title = line.lstrip('#').strip()
                    title = re.sub(r'^\[[^\]]*\]\s*', '', title)
                    return title[:60]
    except OSError:
        pass
    return os.path.basename(path)


def read_content(path):
    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except OSError:
        return ''


def find_skill_name(content):
    """本文中の `skill: <名前>` 行から、紐づいているSkill名を取り出す"""
    m = re.search(r'^skill:\s*(\S+)', content, re.MULTILINE)
    return m.group(1) if m else None


def skill_is_installed(skill_name):
    """~/.claude/skills/<名前>/SKILL.md が実在するかを確認する(全プロジェクト共通の場所のみ)"""
    if not skill_name:
        return False
    path = os.path.expanduser(f'~/.claude/skills/{skill_name}/SKILL.md')
    return os.path.exists(path)


def find_tags(content):
    """本文中の `tags: [a, b, c]` 行からタグの一覧を取り出す"""
    m = re.search(r'^tags:\s*\[(.*?)\]', content, re.MULTILINE)
    if not m:
        return []
    return [t.strip() for t in m.group(1).split(',') if t.strip()]


def find_projects(content):
    """本文中の `observed_in: [a, b]` 行からプロジェクト名の一覧を取り出す"""
    m = re.search(r'^observed_in:\s*\[(.*?)\]', content, re.MULTILINE)
    if not m:
        return []
    return [t.strip() for t in m.group(1).split(',') if t.strip()]


def find_date(content):
    """本文中の `date: YYYY-MM-DD` 行から日付を取り出す"""
    m = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    return m.group(1) if m else None


def days_since(date_str, now_dt):
    if not date_str:
        return None
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None
    return (now_dt - d).days


def extract_section(content, heading, max_len=90):
    """`## <heading>` 見出しの本文を取り出し、短く要約して返す(無ければ None)"""
    m = re.search(rf'^##\s*{re.escape(heading)}\s*\n(.*?)(?=\n##|\Z)', content, re.MULTILINE | re.DOTALL)
    if not m:
        return None
    text = ' '.join(m.group(1).split())
    if not text:
        return None
    if len(text) > max_len:
        text = text[:max_len].rstrip() + '…'
    return text


# カテゴリごとに「問題」「対応」に対応する見出し名(存在すれば要約に使う)
PROBLEM_HEADINGS = {'candidates': '何が起きたか', 'incidents': '何が起きたか'}
SOLUTION_HEADINGS = {'candidates': 'わかったこと・今の対応', 'incidents': '解決', 'rules': 'ルール'}


categories = {cat: files_in(cat) for cat in CATEGORY_LABEL}
category_of = {p: cat for cat, paths in categories.items() for p in paths}

counts = {cat: len(paths) for cat, paths in categories.items()}
chars = {cat: count_chars(paths) for cat, paths in categories.items()}
total_chars = sum(chars.values())

# 中身を丸ごと見れるように、ファイルごとの本文も埋め込む(新しい順)
# ルールについては、対応するSkillが実際に作られているかもここで確認する
items = {}
for cat, paths in categories.items():
    entries = []
    for p in sorted(paths, reverse=True):
        content = read_content(p)
        file_date = find_date(content)
        age_days = days_since(file_date, now_dt)
        entry = {
            'filename': os.path.basename(p),
            'title': first_title(p),
            'content': content,
            'tags': find_tags(content),
            'projects': find_projects(content),
            'days_old': age_days,
            'stale': (cat == 'candidates' and age_days is not None and age_days >= STALE_DAYS),
            'problem_summary': extract_section(content, PROBLEM_HEADINGS[cat]) if cat in PROBLEM_HEADINGS else None,
            'solution_summary': extract_section(content, SOLUTION_HEADINGS[cat]) if cat in SOLUTION_HEADINGS else None,
        }
        if cat == 'rules':
            skill_name = find_skill_name(content)
            entry['skill_name'] = skill_name
            entry['skill_installed'] = skill_is_installed(skill_name)
            entry['skill_retired'] = bool(re.search(r'^skill_status:\s*retired\s*$', content, re.MULTILINE))
        entries.append(entry)
    items[cat] = entries

# 90日以上動きのなかった候補は archive_stale_candidates.py によって
# candidates/archive/ に移動されている。削除ではなく移動なので、
# ここで別カテゴリとして読み込み直し、ダッシュボードから引き続き見られるようにする。
archive_paths = sorted(glob.glob(os.path.join(kb_dir, 'candidates', 'archive', '*.md')), reverse=True)
archived_entries = []
for p in archive_paths:
    content = read_content(p)
    file_date = find_date(content)
    age_days = days_since(file_date, now_dt)
    archived_entries.append({
        'filename': os.path.basename(p),
        'title': first_title(p),
        'content': content,
        'tags': find_tags(content),
        'projects': find_projects(content),
        'days_old': age_days,
        'stale': True,
        'problem_summary': extract_section(content, PROBLEM_HEADINGS['candidates']),
        'solution_summary': extract_section(content, SOLUTION_HEADINGS['candidates']),
    })
items['archived'] = archived_entries

promotion_suggestions_path = os.path.join(kb_dir, 'PROMOTION-SUGGESTIONS.md')
promotion_suggestions = read_content(promotion_suggestions_path).strip() or None

stale_count = sum(1 for e in items.get('candidates', []) if e['stale'])

# Skillが実際に使われた回数(PostToolUse/Skill hookが ~/knowledge-base/.skill_usage.log に記録)
usage_log_path = os.path.join(kb_dir, '.skill_usage.log')
skill_usage_counts = {}
if os.path.isfile(usage_log_path):
    with open(usage_log_path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                skill_usage_counts[parts[1]] = skill_usage_counts.get(parts[1], 0) + 1

# Skillの効果測定(SessionEndのプロンプト型フックが会話内容から判断して記録する)
effectiveness_log_path = os.path.join(kb_dir, '.skill_effectiveness.log')
skill_effectiveness = {}
if os.path.isfile(effectiveness_log_path):
    with open(effectiveness_log_path, encoding='utf-8') as f:
        for line in f:
            parts = line.rstrip('\n').split('\t')
            if len(parts) >= 3:
                ts, skill_name, verdict = parts[0], parts[1], parts[2]
                reason = parts[3] if len(parts) > 3 else ''
                skill_effectiveness.setdefault(skill_name, []).append({
                    'date': ts, 'verdict': verdict, 'reason': reason,
                })


def parse_skill_frontmatter(skill_md_path):
    """SKILL.md の --- で囲まれた部分から name / description を取り出す"""
    content = read_content(skill_md_path)
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not m:
        return None, None
    front = m.group(1)
    name_m = re.search(r'^name:\s*(.+)$', front, re.MULTILINE)
    desc_m = re.search(r'^description:\s*(.+)$', front, re.MULTILINE)
    name = name_m.group(1).strip() if name_m else None
    desc = desc_m.group(1).strip() if desc_m else None
    return name, desc


# 全プロジェクト共通のSkillフォルダを丸ごとスキャンして一覧化する
skills_dir = os.path.expanduser('~/.claude/skills')
linked_skill_names = {
    e['skill_name'] for e in items.get('rules', []) if e.get('skill_name')
}
all_skills = []
if os.path.isdir(skills_dir):
    for name in sorted(os.listdir(skills_dir)):
        skill_md = os.path.join(skills_dir, name, 'SKILL.md')
        if not os.path.isfile(skill_md):
            continue
        parsed_name, description = parse_skill_frontmatter(skill_md)
        skill_key = parsed_name or name
        records = sorted(skill_effectiveness.get(skill_key, []), key=lambda r: r['date'], reverse=True)
        summary = {}
        for r in records:
            summary[r['verdict']] = summary.get(r['verdict'], 0) + 1
        all_skills.append({
            'folder_name': name,
            'name': skill_key,
            'description': description or '(説明文なし)',
            'linked_to_rule': skill_key in linked_skill_names,
            'usage_count': skill_usage_counts.get(skill_key, 0),
            'effectiveness_summary': summary,
            'effectiveness_recent': records[:5],
        })

# 引退させたSkill(retire_skill.py で ~/.claude/skills/ から移動済み)の一覧
retired_skills_dir = os.path.join(kb_dir, 'claude-config', 'skills-archive')
retired_skills = []
if os.path.isdir(retired_skills_dir):
    for name in sorted(os.listdir(retired_skills_dir)):
        skill_md = os.path.join(retired_skills_dir, name, 'SKILL.md')
        if not os.path.isfile(skill_md):
            continue
        parsed_name, description = parse_skill_frontmatter(skill_md)
        retired_skills.append({
            'folder_name': name,
            'name': parsed_name or name,
            'description': description or '(説明文なし)',
        })

current_files = set(category_of.keys())

# 前回のファイル一覧(マニフェスト)と比較して、新規追加分を割り出す
first_run = not os.path.exists(manifest_path)
manifest_files = set()
if not first_run:
    try:
        with open(manifest_path, encoding='utf-8') as f:
            manifest_files = set(json.load(f))
    except (OSError, json.JSONDecodeError):
        manifest_files = set()

new_files = sorted(current_files - manifest_files)

if first_run:
    summary = f'記録を開始しました(既存 {len(current_files)}件)'
elif new_files:
    parts = [f'[{CATEGORY_LABEL[category_of[p]]}] {first_title(p)}' for p in new_files]
    if len(parts) > 2:
        summary = ' / '.join(parts[:2]) + f' ほか{len(parts) - 2}件'
    else:
        summary = ' / '.join(parts)
else:
    summary = '新しい記録なし(数値のみ再集計)'

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(sorted(current_files), f, ensure_ascii=False, indent=2)

history = []
if os.path.exists(out_path):
    try:
        with open(out_path, encoding='utf-8') as f:
            history = json.load(f).get('history', [])
    except (OSError, json.JSONDecodeError):
        history = []

history.append({
    'date': now,
    'summary': summary,
    'rules_count': counts['rules'],
    'candidates_count': counts['candidates'],
    'incidents_count': counts['incidents'],
    'total_chars': total_chars,
})
history = history[-100:]  # 直近100件だけ保持

data = {
    'generated_at': now,
    'rules': {'count': counts['rules'], 'chars': chars['rules']},
    'candidates': {'count': counts['candidates'], 'chars': chars['candidates']},
    'incidents': {'count': counts['incidents'], 'chars': chars['incidents']},
    'archived': {'count': len(archived_entries), 'chars': count_chars(archive_paths)},
    'total_chars': total_chars,
    'history': history,
    'items': items,
    'promotion_suggestions': promotion_suggestions,
    'skills': all_skills,
    'retired_skills': retired_skills,
    'stale_count': stale_count,
}

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# ダブルクリックでの直接閲覧(file://)でも動くよう、同じデータをJSファイルにも埋め込む
with open('docs/stats-data.js', 'w', encoding='utf-8') as f:
    f.write('window.STATS_DATA = ')
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print(f'更新しました: {out_path}')
print(f'今回の変更: {summary}')
PYEOF
