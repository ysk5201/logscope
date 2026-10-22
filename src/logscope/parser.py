"""Cisco形式のsyslog行をパースするモジュール.

Cisco製品(ASA, IOS, FTDなど)のsyslogには次のような共通部分がある:

    %ASA-4-106023: Deny tcp src outside:203.0.113.5/4444 ...
     ^^^ ^ ^^^^^^
     |   | +-- mnemonic (メッセージID)
     |   +---- severity (0=emergencies ... 7=debugging)
     +-------- facility

この部分を正規表現で取り出す。
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# %FACILITY-SEVERITY-MNEMONIC: message
_CISCO_TAG = re.compile(
    r"%(?P<facility>[A-Z0-9_]+)-(?P<severity>[0-7])-(?P<mnemonic>[A-Z0-9_]+):\s*(?P<message>.*)$"
)

SEVERITY_NAMES: dict[int, str] = {
    0: "emergencies",
    1: "alerts",
    2: "critical",
    3: "errors",
    4: "warnings",
    5: "notifications",
    6: "informational",
    7: "debugging",
}


@dataclass(frozen=True)
class LogEntry:
    facility: str
    severity: int
    mnemonic: str
    message: str

    @property
    def severity_name(self) -> str:
        return SEVERITY_NAMES[self.severity]

    @property
    def message_id(self) -> str:
        """例: 'ASA-4-106023'"""
        return f"{self.facility}-{self.severity}-{self.mnemonic}"


def parse_line(line: str) -> LogEntry | None:
    """1行をパースする. Cisco形式でなければ None を返す."""
    match = _CISCO_TAG.search(line.rstrip("\n"))
    if match is None:
        return None
    return LogEntry(
        facility=match["facility"],
        severity=int(match["severity"]),
        mnemonic=match["mnemonic"],
        message=match["message"],
    )
