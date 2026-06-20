import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from logic_utils import (
    check_guess,
    describe_guess,
    get_range_for_difficulty,
    is_in_range,
    parse_guess,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_hint_message_when_guess_too_high():
    # When guess is too high, the hint should tell the player to go LOWER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
    assert message == "📉 Go LOWER!"

def test_hint_message_when_guess_too_low():
    # When guess is too low, the hint should tell the player to go HIGHER
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message
    assert message == "📈 Go HIGHER!"

def test_easy_difficulty_range():
    # Easy mode should have range 1-20
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_difficulty_range():
    # Normal mode should have range 1-100
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_hard_difficulty_range():
    # Hard mode should have range 1-50
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50


# --- Edge-case tests for parse_guess (Stretch Feature SF7) ---

def test_parse_guess_rejects_non_numeric_string():
    # Letters are not a valid guess and must be rejected with an error.
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_rejects_empty_string():
    # An empty submission should be rejected, not crash or count as 0.
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_rejects_none():
    # A missing/None input should be handled gracefully, not raise.
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_accepts_negative_number():
    # Negative numbers parse to a valid int (range checking happens elsewhere).
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None


def test_parse_guess_truncates_float_string():
    # A float-like string should be accepted and truncated to an int.
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None


def test_parse_guess_rejects_whitespace():
    # Whitespace-only input is not a number and must be rejected.
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_is_in_range_accepts_value_inside_range():
    # A guess within the inclusive range is valid.
    assert is_in_range(50, 1, 100) is True


def test_is_in_range_accepts_boundaries():
    # The low and high bounds themselves are in range (inclusive).
    assert is_in_range(1, 1, 100) is True
    assert is_in_range(100, 1, 100) is True


def test_is_in_range_rejects_negative():
    # A negative guess is out of range and should be rejected.
    assert is_in_range(-5, 1, 100) is False


def test_is_in_range_rejects_value_above_range():
    # A guess above the high bound is out of range.
    assert is_in_range(200, 1, 100) is False


# --- Guess History display tests (Stretch Feature SF8) ---

def test_describe_guess_too_low_shows_higher_hint():
    # A past low guess should be annotated with the "go higher" hint.
    assert describe_guess(40, 50) == "40 — 📈 Go HIGHER!"


def test_describe_guess_too_high_shows_lower_hint():
    # A past high guess should be annotated with the "go lower" hint.
    assert describe_guess(60, 50) == "60 — 📉 Go LOWER!"


def test_describe_guess_correct_shows_win_marker():
    # A past winning guess should be annotated as correct.
    assert describe_guess(50, 50) == "50 — 🎉 Correct!"


def test_describe_guess_invalid_entry_flagged():
    # Non-integer history entries (rejected input) are flagged invalid.
    assert describe_guess("abc", 50) == "abc — ⚠️ invalid"
