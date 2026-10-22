import json
from pathlib import Path

from logscope.cli import main

SAMPLE = str(Path(__file__).parent.parent / "samples" / "asa.log")


def test_text_output(capsys):
    assert main([SAMPLE]) == 0
    out = capsys.readouterr().out
    assert "total: 14 lines" in out
    assert "ASA-4-106023" in out


def test_json_output(capsys):
    assert main([SAMPLE, "--json", "--max-severity", "4"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["parsed_lines"] == 13
    assert "informational" not in data["by_severity"]


def test_missing_file_returns_1(capsys):
    assert main(["no_such_file.log"]) == 1
    assert "file not found" in capsys.readouterr().err
