"""SessionEndフックの最後に呼ばれる。knowledge-baseの変更を
コミット・GitHubへpushする、一連の流れをこのスクリプト1つで担う。

重要な設計判断: 機密情報っぽい文字列のチェックは「コミットする前」に行う。
「コミットしてからpush前にチェック」だと、後で該当ファイルを直して
別のコミットを積んでも、機密情報入りの古いコミット自体はローカル履歴に
残り続け、次にpushした時に一緒に送られてしまう(直したつもりが結局
漏れる)。そのため、機密情報が見つかった場合は git add だけ取り消して、
そもそもコミットを作らない(=履歴に一切残さない)ようにしている。
"""
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
    # 既知の形式に一致しない、独自のAPIキー・パスワードらしきものも
    # 「キーワード + 値」のパターンで広めに拾う(誤検知はあり得るが、
    # 見逃すよりは安全側に倒す)
    'キー/パスワードらしき記述': re.compile(
        r'(?i)\b(api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*["\']?[A-Za-z0-9_\-]{8,}'
    ),
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
    git('add', '-A')
    findings = scan()

    if findings:
        # コミットさせない(ステージだけ取り消す。ファイルの変更自体は
        # 作業ディレクトリに残るので、直す作業はそのまま続けられる)
        git('reset')
        with open(WARNING_PATH, 'w', encoding='utf-8') as f:
            f.write('# 機密情報の可能性がある文字列が見つかりました\n\n')
            f.write('この内容はコミットされていません(pushもされていません)。\n')
            f.write('該当ファイルを修正するか削除してから、次の`/clear`で\n')
            f.write('再度コミット・pushが試みられます。\n\n')
            f.write('\n'.join(findings))
            f.write('\n')
        print('secret scan: 機密情報の疑いがあるためコミット・pushを中止しました', file=sys.stderr)
        sys.exit(1)

    if os.path.exists(WARNING_PATH):
        os.remove(WARNING_PATH)

    diff_check = git('diff', '--cached', '--quiet')
    if diff_check.returncode != 0:
        git('commit', '-m', f'auto: {subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True).stdout.strip()}', '--quiet')

    result = git('pull', '--rebase', '--quiet')
    if result.returncode != 0:
        git('rebase', '--abort')
    git('push', '--quiet')


if __name__ == '__main__':
    main()
