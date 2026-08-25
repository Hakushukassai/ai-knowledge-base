"""手動で実行する: Skillを「引退」させる。
使い方: python3 ~/.claude/hooks/retire_skill.py <skill名>

やること:
1. ~/.claude/skills/<name>/ を knowledge-base/claude-config/skills-archive/<name>/
   に移動する(削除ではなく移動。中身は残る)。これでClaude Codeは
   このSkillを二度と自動使用しなくなる。全プロジェクト共通のSkillフォルダ
   (~/.claude/skills/)のみ対象。プロジェクト専用Skillは対象外。
2. 対応する rules/*.md に `skill: <name>` の行があれば、直後に
   `skill_status: retired` を追記する。ダッシュボード側で
   「壊れて検出できない」場合と区別して表示するための印。
"""
import glob
import os
import re
import shutil
import sys

KB_DIR = os.path.expanduser('~/knowledge-base')
SKILLS_DIR = os.path.expanduser('~/.claude/skills')
ARCHIVE_DIR = os.path.join(KB_DIR, 'claude-config', 'skills-archive')


def main():
    if len(sys.argv) != 2:
        print('使い方: python3 retire_skill.py <skill名>')
        sys.exit(1)

    name = sys.argv[1]
    src = os.path.join(SKILLS_DIR, name)
    if not os.path.isdir(src):
        print(f'見つかりません: {src}')
        sys.exit(1)

    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    dest = os.path.join(ARCHIVE_DIR, name)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.move(src, dest)
    print(f'移動しました: {src} -> {dest}')

    for path in glob.glob(os.path.join(KB_DIR, 'rules', '*.md')):
        with open(path, encoding='utf-8') as f:
            content = f.read()
        if re.search(rf'^skill:\s*{re.escape(name)}\s*$', content, re.MULTILINE) \
                and 'skill_status:' not in content:
            content = re.sub(
                rf'(^skill:\s*{re.escape(name)}\s*$)',
                r'\1\nskill_status: retired',
                content,
                count=1,
                flags=re.MULTILINE,
            )
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'更新しました: {path}')


if __name__ == '__main__':
    main()
