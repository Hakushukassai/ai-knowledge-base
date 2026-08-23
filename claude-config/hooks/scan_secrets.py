"""機密情報っぽい文字列(メールアドレス・APIキーの形をした文字列等)を
knowledge-base内から探す、再利用可能なスキャナ。

呼び出し元は2箇所:
1. knowledge-base/.githooks/pre-commit (本物のgit hook。コミット経路を
   問わず、手動のgit commitでも必ず通る)
2. ~/.claude/hooks/scan_and_push.py (Claude CodeのSessionEndフック。
   pushの実行そのものを担当)

見つかった場合は SECURITY-WARNING.md に詳細を書き出し、exit code 1 で
終了する(git hookとして使うと、これがコミットを拒否する合図になる)。
"""
import os
import re
import sys

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
    # 既知の形式に一致しない独自のAPIキー・パスワードらしきものも
    # 「キーワード に続けて 値」というパターンで広めに拾う。
    # 注意: ドキュメント中の説明用の書き方によっては誤検知しうるので、
    # ドキュメントを書く時は日本語の山括弧で囲んだ言い回しのような
    # 紛れない書き方をすること。
    'キー/パスワードらしき記述': re.compile(
        r'(?i)\b(api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*["\']?[A-Za-z0-9_\-]{8,}'
    ),
}


def scan(kb_dir):
    findings = []
    for root, dirs, files in os.walk(kb_dir):
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
                    rel = os.path.relpath(path, kb_dir)
                    snippet = m.group(0)[:40]
                    findings.append(f'- `{rel}`: {label}らしき文字列 (`{snippet}...`)')
    return findings


def main():
    kb_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/knowledge-base')
    warning_path = os.path.join(kb_dir, 'SECURITY-WARNING.md')
    findings = scan(kb_dir)

    if findings:
        with open(warning_path, 'w', encoding='utf-8') as f:
            f.write('# 機密情報の可能性がある文字列が見つかりました\n\n')
            f.write('コミットを拒否しました。該当ファイルを修正するか削除してから\n')
            f.write('もう一度コミットしてください。\n\n')
            f.write('\n'.join(findings))
            f.write('\n')
        print('機密情報の疑いがあるためコミットを拒否しました。詳細: SECURITY-WARNING.md', file=sys.stderr)
        for line in findings:
            print(line, file=sys.stderr)
        sys.exit(1)

    if os.path.exists(warning_path):
        os.remove(warning_path)
    sys.exit(0)


if __name__ == '__main__':
    main()
