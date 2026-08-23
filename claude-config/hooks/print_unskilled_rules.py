"""SessionStartフックから呼ばれる。knowledge-base/rules/ の中身を
セッション開始時に読み込ませるが、既にSkill化されている(実際に
~/.claude/skills/ にSKILL.mdが存在する)ルールは、そのSkillが必要な時に
自動で参照してくれるため、ここでは二重に読み込まない。
これにより、Skillが増えるほどセッション開始時のコンテキストが
際限なく膨らむのを防ぐ。"""
import glob
import os
import re

KB_DIR = os.path.expanduser('~/knowledge-base')


def find_skill_name(content):
    m = re.search(r'^skill:\s*(\S+)', content, re.MULTILINE)
    return m.group(1) if m else None


def skill_is_installed(skill_name):
    if not skill_name:
        return False
    return os.path.isfile(os.path.expanduser(f'~/.claude/skills/{skill_name}/SKILL.md'))


def main():
    paths = sorted(glob.glob(os.path.join(KB_DIR, 'rules', '*.md')))
    shown = 0
    for path in paths:
        try:
            with open(path, encoding='utf-8') as f:
                content = f.read()
        except OSError:
            continue
        skill_name = find_skill_name(content)
        if skill_is_installed(skill_name):
            continue  # Skillが既にあるので、ここでは読み込ませない
        print(content)
        shown += 1

    if shown == 0 and paths:
        print('(すべてのルールはSkill化済みのため、ここでは省略)')


if __name__ == '__main__':
    main()
