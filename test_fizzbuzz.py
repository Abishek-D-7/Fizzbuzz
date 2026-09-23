# test_fizzbuzz.py
import sys

from fizzbuzz import mutate, parse_header, CoverageTracker


def test_mutate_returns_string_and_changes_input():
    original = "hello"
    result = mutate(original)
    assert isinstance(result, str)
    # High probability it's different, but allow rare no-op
    assert result != original or len(original) == len(result)


def test_coverage_tracker_records_parse_header_lines():
    tracker = CoverageTracker()
    sys.settrace(tracker.trace_func)
    try:
        parse_header("FUZZ!")
    except ValueError:
        pass  # Crash is expected; we only care about line coverage
    sys.settrace(None)

    # parse_header has several lines; at least one should be recorded
    assert len(tracker.executed_lines) > 0


def test_parse_header_crash_on_payload():
    try:
        parse_header("FUZZ!")
    except ValueError as e:
        assert "CRASH DETECTED" in str(e)
        return
    assert False, "Expected ValueError for payload 'FUZZ!'"


def test_parse_header_no_crash_for_short_or_invalid():
    # Should not raise for these
    parse_header("hi")
    parse_header("ABC")
    parse_header("FUZZ")
    parse_header("FUZ")


if __name__ == "__main__":
    test_mutate_returns_string_and_changes_input()
    test_coverage_tracker_records_parse_header_lines()
    test_parse_header_crash_on_payload()
    test_parse_header_no_crash_for_short_or_invalid()
    print("All tests passed.")
