"""SessionEndフックから呼ばれる。90日以上動きのない候補(candidates/*.md)を
candidates/archive/ に移動する。

ただし「実績のある」候補は年月が経っていても対象外にする(使うほど強くなる、を
アーカイブ側でも実装する部分):
- endorsed: true が付いている(人が確認済み)
- observed_count が2以上(複数回観測されている)
- observed_in に2つ以上のプロジェクトが入っている(昇格目前)
- .reference_usage.log に、直近90日以内の参照記録がある

ダッシュボード側の「30日で警告」表示とは別の仕組み: 警告は目に入れて
もらうためのもの、アーカイブは一覧から静かに外して散らからないように
するための片付け。削除ではなく移動なので、中身はアーカイブ画面や
Gitの履歴からいつでも見られる。
"""
import glob
import os
import re
from datetime import datetime, timezone
import shutil

KB_DIR = os.path.expanduser('~/knowledge-base')
ARCHIVE_DAYS = 90


def find_date(content):
    m = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    return m.group(1) if m else None


def find_observed_count(content):
    m = re.search(r'^observed_count:\s*(\d+)', content, re.MULTILINE)
    return int(m.group(1)) if m else 1


def find_observed_in(content):
    m = re.search(r'^observed_in:\s*\[(.*?)\]', content, re.MULTILINE)
    if not m:
        return []
    return [t.strip() for t in m.group(1).split(',') if t.strip()]


def is_endorsed(content):
    return bool(re.search(r'^endorsed:\s*true\s*$', content, re.MULTILINE | re.IGNORECASE))


def load_recent_referenced_filenames(now):
    """.reference_usage.log から、直近90日以内に参照されたファイル名の集合を作る。
    フォーマット: 日時<TAB>カテゴリ<TAB>ファイル名<TAB>判定<TAB>理由"""
    log_path = os.path.join(KB_DIR, '.reference_usage.log')
    referenced = set()
    if not os.path.isfile(log_path):
        return referenced
    try:
        with open(log_path, encoding='utf-8') as f:
            for line in f:
                parts = line.rstrip('\n').split('\t')
                if len(parts) < 3:
                    continue
                ts_str, _cat, filename = parts[0], parts[1], parts[2]
                try:
                    ts = datetime.strptime(ts_str[:19], '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    continue
                if (now - ts).days < 90:
                    referenced.add(filename)
    except OSError:
        pass
    return referenced


def has_track_record(content, filename, recent_referenced):
    if is_endorsed(content):
        return True
    if find_observed_count(content) >= 2:
        return True
    if len(find_observed_in(content)) >= 2:
        return True
    if filename in recent_referenced:
        return True
    return False


def main():
    candidates_dir = os.path.join(KB_DIR, 'candidates')
    archive_dir = os.path.join(candidates_dir, 'archive')
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    recent_referenced = load_recent_referenced_filenames(now)

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

        if (now - d).days < ARCHIVE_DAYS:
            continue

        filename = os.path.basename(path)
        if has_track_record(content, filename, recent_referenced):
            continue

        os.makedirs(archive_dir, exist_ok=True)
        shutil.move(path, os.path.join(archive_dir, filename))


if __name__ == '__main__':
    main()
