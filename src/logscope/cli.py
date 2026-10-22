"""コマンドラインのエントリポイント.

使い方:
    logscope samples/asa.log
    logscope samples/asa.log --max-severity 4 --json
    cat samples/asa.log | logscope -
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from logscope import __version__
from logscope.parser import SEVERITY_NAMES
from logscope.summary import Summary, summarize


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="logscope",
        description="Cisco形式のsyslogをseverity/メッセージID別に集計します",
    )
    p.add_argument("file", help="ログファイルのパス ('-' で標準入力)")
    p.add_argument(
        "--max-severity",
        type=int,
        default=7,
        choices=range(8),
        metavar="0-7",
        help="この値以下のseverityだけ集計する (例: 3 = errors以上)",
    )
    p.add_argument("--top", type=int, default=10, help="上位何件のメッセージIDを表示するか")
    p.add_argument("--json", action="store_true", help="JSONで出力する")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def format_text(summary: Summary, top: int) -> str:
    lines = [
        f"total: {summary.total_lines} lines "
        f"(parsed {summary.parsed_lines}, unparsed {summary.unparsed_lines})",
        "",
        "by severity:",
    ]
    for sev, count in sorted(summary.by_severity.items()):
        lines.append(f"  {sev} {SEVERITY_NAMES[sev]:<14} {count:>6}")
    lines += ["", f"top {top} message ids:"]
    for mid, count in summary.by_message_id.most_common(top):
        lines.append(f"  {mid:<24} {count:>6}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if args.file == "-":
            summary = summarize(sys.stdin, max_severity=args.max_severity)
        else:
            with open(args.file, encoding="utf-8", errors="replace") as f:
                summary = summarize(f, max_severity=args.max_severity)
    except FileNotFoundError:
        print(f"logscope: file not found: {args.file}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(summary.to_dict(top=args.top), indent=2, ensure_ascii=False))
    else:
        print(format_text(summary, top=args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
