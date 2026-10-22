from pathlib import Path

import pytest

from logscope.summary import summarize

SAMPLE = Path(__file__).parent.parent / "samples" / "asa.log"


def test_summarize_sample_file():
    with SAMPLE.open() as f:
        s = summarize(f)
    assert s.total_lines == 14
    assert s.parsed_lines == 13
    assert s.unparsed_lines == 1
    assert s.by_message_id["ASA-4-106023"] == 3
    assert s.by_message_id.most_common(1)[0] == ("ASA-4-106023", 3)


def test_max_severity_filters_less_important_logs():
    with SAMPLE.open() as f:
        s = summarize(f, max_severity=3)
    # 0-3 だけが残る (1, 2, 3, 3)
    assert set(s.by_severity) <= {0, 1, 2, 3}
    assert sum(s.by_severity.values()) == 4


def test_invalid_max_severity():
    with pytest.raises(ValueError):
        summarize([], max_severity=8)


def test_to_dict_shape():
    s = summarize(["%ASA-4-106023: a", "%ASA-4-106023: b", "%ASA-6-302013: c"])
    d = s.to_dict(top=1)
    assert d["by_severity"] == {"warnings": 2, "informational": 1}
    assert d["top_message_ids"] == [{"message_id": "ASA-4-106023", "count": 2}]
