import pytest

from logscope.parser import parse_line


def test_parse_asa_line():
    line = (
        "Oct 17 10:15:05 asa01 : %ASA-4-106023: Deny tcp src outside:203.0.113.5/4444 "
        'dst inside:10.0.0.8/22 by access-group "OUTSIDE_IN"'
    )
    entry = parse_line(line)
    assert entry is not None
    assert entry.facility == "ASA"
    assert entry.severity == 4
    assert entry.severity_name == "warnings"
    assert entry.mnemonic == "106023"
    assert entry.message_id == "ASA-4-106023"
    assert entry.message.startswith("Deny tcp")


def test_parse_ios_line_with_alpha_mnemonic():
    entry = parse_line("rtr01 : %LINK-3-UPDOWN: Interface Gi0/1, changed state to down")
    assert entry is not None
    assert entry.facility == "LINK"
    assert entry.severity == 3
    assert entry.mnemonic == "UPDOWN"


@pytest.mark.parametrize(
    "line",
    [
        "",
        "plain text without tag",
        "%ASA-9-106023: severity 9 does not exist",
        "%asa-4-106023: lowercase facility",
    ],
)
def test_non_cisco_lines_return_none(line):
    assert parse_line(line) is None
