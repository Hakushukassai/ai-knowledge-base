"""SessionEndフックから呼ばれる。90日以上動きのない候補(candidates/*.md)を
candidates/archive/ に移動する。

ダッシュボード側の「30日で警告」表示とは別の仕組み: 警告は目に入れて
もらうためのもの、アーカイブは一覧から静かに外して散らからないように
するための片付け。削除ではなく移動なので、中身はアーカイブ画面や
Gitの履歴からいつでも見られる。
"""
import glob
import os
import re
import shutil
from datetime import datetime, timezone

KB_DIR = os.path.expanduser('~/knowledge-base')
ARCHIVE_DAYS = 90


def find_date(content):
    m = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    return m.group(1) if m else None


def main():
    candidates_dir = os.path.join(KB_DIR, 'candidates')
    archive_dir = os.path.join(candidates_dir, 'archive')
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    for path in glob.glob(os.path.join(candidates_dir, '*.md')):
        try:
            with open(path, encoding='utf-8') as f:
                content = f.read()
        except OSError:
            continue

        date_str = find_date(content)
        if not date_str:
            continue
        try:
            d = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            continue

        if (now - d).days >= ARCHIVE_DAYS:
            os.makedirs(archive_dir, exist_ok=True)
            shutil.move(path, os.path.join(archive_dir, os.path.basename(path)))


if __name__ == '__main__':
    main()
