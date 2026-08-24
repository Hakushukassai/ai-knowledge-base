"""SessionEndフックの最後に呼ばれる。knowledge-baseの変更を
コミット・GitHubへpushする。

機密情報のチェック自体は、このスクリプトではなく本物の
git pre-commitフック(knowledge-base/.githooks/pre-commit、
scan_secrets.pyを呼び出す)が担当する。これにより、Claude Code経由の
コミットだけでなく、手動のgit commitなど他の経路からのコミットも
必ず同じチェックを通る(defense in depthではなく、そもそも
コミット経路を1つに絞り込む設計)。

このスクリプトは「コミットが拒否されたら、pushもせずに諦める」
だけを担当する。

`git pull --rebase` が衝突して失敗した場合、以前は黙ってabortして
push を試み、それも失敗して何も起きなかったように見えるだけだった
(複数PC間の同期が実は止まっていることに誰も気づけない)。
今は SYNC-CONFLICT.md を書き出し、SessionStart フックで次回必ず
警告が表示されるようにしている。
"""
import os
import subprocess

KB_DIR = os.path.expanduser('~/knowledge-base')
CONFLICT_WARNING_PATH = os.path.join(KB_DIR, 'SYNC-CONFLICT.md')


def git(*args):
    return subprocess.run(['git', *args], cwd=KB_DIR, capture_output=True, text=True)


def now_str():
    return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()


def write_conflict_warning(reason):
    with open(CONFLICT_WARNING_PATH, 'w', encoding='utf-8') as f:
        f.write('# 同期エラー: このPCの変更がGitHubにpushされていません\n\n')
        f.write(f'{reason}\n\n')
        f.write('このPC上の変更は消えていません(ローカルにcommit済みのまま残っています)。\n')
        f.write('以下を手動で実行して解決してください。\n\n')
        f.write('```bash\n')
        f.write('cd ~/knowledge-base\n')
        f.write('git pull --rebase\n')
        f.write('# コンフリクトが出たファイルを解決してから:\n')
        f.write('git add <解決したファイル>\n')
        f.write('git rebase --continue\n')
        f.write('git push\n')
        f.write('```\n\n')
        f.write(f'発生時刻: {now_str()}\n')


def main():
    git('add', '-A')

    diff_check = git('diff', '--cached', '--quiet')
    if diff_check.returncode != 0:
        commit_result = git(
            'commit', '-m',
            subprocess.run(['date', '-u', '+auto: %Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip(),
            '--quiet',
        )
        if commit_result.returncode != 0:
            # pre-commitフックに拒否された(機密情報の疑い)。
            # SECURITY-WARNING.md は scan_secrets.py 側が書き出し済みなので、
            # ここではpushせずに終了する。
            return

    result = git('pull', '--rebase', '--quiet')
    if result.returncode != 0:
        git('rebase', '--abort')
        write_conflict_warning(
            '`git pull --rebase` が他のPCからの変更と衝突(コンフリクト)したため、'
            '自動での取り込み・pushを中止しました。'
        )
        return

    if os.path.exists(CONFLICT_WARNING_PATH):
        os.remove(CONFLICT_WARNING_PATH)

    push_result = git('push', '--quiet')
    if push_result.returncode != 0:
        write_conflict_warning(
            'pushが失敗しました(ネットワーク不通、認証切れ、または他PCがこの直後に'
            'pushしたなどが考えられます)。'
        )


if __name__ == '__main__':
    main()
