"""SessionEndフックの最後に呼ばれる。GitHubにpushする前に、うっかり
紛れ込んだ機密情報っぽい文字列(メールアドレス・APIキーの形をした文字列等)
が無いかを簡易チェックする。見つかった場合はpushを中止し、
SECURITY-WARNING.md に詳細を書き出す(このファイル自体はGit管理外)。
問題が無ければ git pull --rebase → git push を行う。"""
import os
import re
import subprocess
import sys

KB_DIR = os.path.expanduser('~/knowledge-base')
WARNING_PATH = os.path.join(KB_DIR, 'SECURITY-WARNING.md')
SKIP_NAMES = {'SECURITY-WARNING.md', '.skill_usage.log'}
SKIP_DIRS = {'.git'}

PATTERNS = {
    'メールアドレス': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
    'GitHubトークン': re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}'),
    'OpenAI風APIキー': re.compile(r'sk-[A-Za-z0-9]{20,}'),
    'AWSアクセスキー': re.compile(r'AKIA[0-9A-Z]{16}'),
    'Google APIキー': re.compile(r'AIza[0-9A-Za-z_-]{35}'),
    'Slackトークン': re.compile(r'xox[baprs]-[A-Za-z0-9-]{10,}'),
    '秘密鍵ブロック': re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
}


def scan():
    findings = []
    for root, dirs, files in os.walk(KB_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in SKIP_NAMES:
                continue
            path = os.path.join(root, name)
            try:
                with open(path, encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except OSError:
                continue
            for label, pattern in PATTERNS.items():
                for m in pattern.finditer(content):
                    rel = os.path.relpath(path, KB_DIR)
                    snippet = m.group(0)[:40]
                    findings.append(f'- `{rel}`: {label}らしき文字列 (`{snippet}...`)')
    return findings


def git(*args):
    return subprocess.run(['git', *args], cwd=KB_DIR, capture_output=True, text=True)


def main():
    findings = scan()

    if findings:
        with open(WARNING_PATH, 'w', encoding='utf-8') as f:
            f.write('# 機密情報の可能性がある文字列が見つかりました\n\n')
            f.write('自動pushを中止しました。内容を確認し、問題なければ該当ファイルを\n')
            f.write('修正するか削除してから、手動で `git push` してください。\n')
            f.write('このファイルは、問題が解消されると次回の`/clear`時に自動で消えます。\n\n')
            f.write('\n'.join(findings))
            f.write('\n')
        print('secret scan: 機密情報の疑いがあるためpushを中止しました', file=sys.stderr)
        sys.exit(1)

    if os.path.exists(WARNING_PATH):
        os.remove(WARNING_PATH)

    result = git('pull', '--rebase', '--quiet')
    if result.returncode != 0:
        git('rebase', '--abort')
    git('push', '--quiet')


if __name__ == '__main__':
    main()
