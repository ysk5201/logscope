"""パース済みログを集計するモジュール."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass, field

from logscope.parser import SEVERITY_NAMES, LogEntry, parse_line


@dataclass
class Summary:
    total_lines: int = 0
    parsed_lines: int = 0
    by_severity: Counter[int] = field(default_factory=Counter)
    by_message_id: Counter[str] = field(default_factory=Counter)

    @property
    def unparsed_lines(self) -> int:
        return self.total_lines - self.parsed_lines

    def to_dict(self, top: int = 10) -> dict:
        return {
            "total_lines": self.total_lines,
            "parsed_lines": self.parsed_lines,
            "unparsed_lines": self.unparsed_lines,
            "by_severity": {
                SEVERITY_NAMES[sev]: count for sev, count in sorted(self.by_severity.items())
            },
            "top_message_ids": [
                {"message_id": mid, "count": count}
                for mid, count in self.by_message_id.most_common(top)
            ],
        }


def summarize(lines: Iterable[str], max_severity: int = 7) -> Summary:
    """ログ行を集計する.

    max_severity: この値以下(=より重要)のseverityだけを数える.
                  例: 3 を指定すると emergencies〜errors だけになる.
    """
    if not 0 <= max_severity <= 7:
        raise ValueError(f"max_severity must be 0-7, got {max_severity}")

    result = Summary()
    for line in lines:
        result.total_lines += 1
        entry: LogEntry | None = parse_line(line)
        if entry is None:
            continue
        result.parsed_lines += 1
        if entry.severity > max_severity:
            continue
        result.by_severity[entry.severity] += 1
        result.by_message_id[entry.message_id] += 1
    return result
