import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from logic_utils import check_guess, get_range_for_difficulty

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
