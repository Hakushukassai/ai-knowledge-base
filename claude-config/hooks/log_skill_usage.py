"""PostToolUse(Skill)フックから呼ばれ、標準入力のJSONから使われたSkill名を
~/knowledge-base/.skill_usage.log に1行(日時\tSkill名)追記する。"""
import json
import os
import sys
import datetime


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return

    name = (data.get('tool_input') or {}).get('skill')
    if not name:
        return

    log_path = os.path.expanduser('~/knowledge-base/.skill_usage.log')
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f'{now}\t{name}\n')


if __name__ == '__main__':
    main()
