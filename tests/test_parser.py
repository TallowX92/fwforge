import pytest
from fwforge.fw_parser import FixedWidthParser

def test_basic_parsing():
    layout = {
        "columns": [
            {"name": "a", "start": 0, "length": 3, "trim": True, "type": "string"},
            {"name": "b", "start": 3, "length": 2, "trim": True, "type": "int"}
        ]
    }
    parser = FixedWidthParser(layout)
    line = "ABC10"
    assert parser.parse_line(line) == {"a": "ABC", "b": 10}

def test_start_end_parsing():
    layout = {
        "columns": [
            {"name": "a", "start": 0, "end": 3, "trim": True, "type": "string"},
        ]
    }
    parser = FixedWidthParser(layout)
    line = "ABC10"
    assert parser.parse_line(line) == {"a": "ABC"}

def test_short_line_handling():
    layout = {
        "columns": [
            {"name": "a", "start": 0, "length": 5, "trim": False, "type": "string"},
        ]
    }
    parser = FixedWidthParser(layout)
    line = "AB"
    # Should handle end > len(line)
    assert parser.parse_line(line) == {"a": "AB"}

def test_float_casting():
    layout = {
        "columns": [
            {"name": "weight", "start": 0, "length": 5, "trim": True, "type": "float"},
        ]
    }
    parser = FixedWidthParser(layout)
    assert parser.parse_line("10.5 ") == {"weight": 10.5}
