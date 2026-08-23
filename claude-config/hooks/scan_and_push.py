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
"""
import os
import subprocess

KB_DIR = os.path.expanduser('~/knowledge-base')


def git(*args):
    return subprocess.run(['git', *args], cwd=KB_DIR, capture_output=True, text=True)


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
    git('push', '--quiet')


if __name__ == '__main__':
    main()
