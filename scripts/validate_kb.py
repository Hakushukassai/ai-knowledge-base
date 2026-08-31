"""knowledge-base の Markdown ファイルを機械的に検証する。

これまでSessionEndの自然言語フックだけに任せていた「必須フィールドが
揃っているか」「本文中で参照しているファイルが実在するか」を、候補が
増えても劣化しないスクリプトでチェックする(LLM任せの集計だけでは
件数が増えるほど見落としが増えるため)。

使い方:
  python3 scripts/validate_kb.py        … 全件チェックして結果を表示
  終了コード: 問題が1件でもあれば1、無ければ0

kb-sync / pre-kb-sync のタイミングで実行される想定。
"""
import glob
import os
import re
import sys
from pathlib import Path

KB_DIR = os.environ.get('KB_DIR', str(Path(__file__).resolve().parents[1]))

# カテゴリごとの必須フロントマターキー
REQUIRED_FRONTMATTER = {
    'candidates': ['status', 'observed_count', 'observed_in', 'tags', 'date'],
    'external-skill-imports': ['status', 'observed_count', 'observed_in', 'tags', 'date', 'source', 'source_url'],
    'rules': ['status', 'tags'],
    'incidents': ['date', 'project'],
}

# カテゴリごとの必須見出し(本文に無いと昇格判断の材料が欠ける)
REQUIRED_HEADINGS = {
    'candidates': ['## 何が起きたか', '## わかったこと・今の対応'],
    'external-skill-imports': ['## 何が起きたか', '## わかったこと・今の対応'],
}

# 本文中でよく使われる「他ファイルへの相対参照」を検出する正規表現
LINK_PATTERN = re.compile(
    r'(?:^|[\s(`"\'])((?:rules|candidates|candidates/archive|incidents|external-skill-imports)/[A-Za-z0-9_\-./]+\.md)'
)

# HTMLコメント(<!-- ... -->)の中身は「もう存在しない参照について説明する
# 注記」等、意図的にリンクとして扱ってほしくない場合に使われるため、
# リンク切れチェックの対象から除外する
COMMENT_PATTERN = re.compile(r'<!--.*?-->', re.DOTALL)


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def parse_frontmatter_keys(content):
    """フロントマター相当の部分( `# 見出し` の次の行から、最初の `##` 見出しの
    手前まで)に出てくる `key: value` 行のキー名を集める。"""
    keys = set()
    for line in content.split('\n'):
        if line.startswith('##'):
            break
        m = re.match(r'^([a-z_]+):\s*(.*)$', line)
        if m:
            keys.add(m.group(1))
    return keys


def check_file(category, path, all_files, problems):
    content = read(path)
    rel = os.path.relpath(path, KB_DIR)

    required_keys = REQUIRED_FRONTMATTER.get(category, [])
    if required_keys:
        present = parse_frontmatter_keys(content)
        missing = [k for k in required_keys if k not in present]
        if missing:
            problems.append(f'[必須項目不足] {rel}: {", ".join(missing)} が無い')

    for heading in REQUIRED_HEADINGS.get(category, []):
        if heading not in content:
            problems.append(f'[見出し不足] {rel}: 「{heading}」が無い')

    for m in LINK_PATTERN.finditer(COMMENT_PATTERN.sub('', content)):
        ref = m.group(1)
        ref_path = os.path.join(KB_DIR, ref)
        if not os.path.isfile(ref_path):
            problems.append(f'[リンク切れ] {rel}: 「{ref}」が存在しない')


def main():
    # Windows(cp932コンソール)で日本語出力が文字化けするのを防ぐ
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    problems = []
    all_files = set()
    for category in ['rules', 'candidates', 'incidents', 'external-skill-imports']:
        for path in sorted(glob.glob(os.path.join(KB_DIR, category, '*.md'))):
            all_files.add(path)

    for category in ['rules', 'candidates', 'incidents', 'external-skill-imports']:
        for path in sorted(glob.glob(os.path.join(KB_DIR, category, '*.md'))):
            check_file(category, path, all_files, problems)

    if problems:
        print(f'{len(problems)}件の問題が見つかりました:')
        for p in problems:
            print(f'  - {p}')
        sys.exit(1)
    else:
        print('問題は見つかりませんでした')
        sys.exit(0)


if __name__ == '__main__':
    main()
