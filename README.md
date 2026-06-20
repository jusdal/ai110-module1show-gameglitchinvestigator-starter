# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game's purpose.** A Streamlit number-guessing game: the player guesses a hidden secret number within a difficulty-based range and a limited number of attempts, getting "higher/lower" hints and a score after each guess. The starter version was deliberately broken so the goal was to find and fix the glitches.

**Bugs found.**
1. **Hints reversed** — a guess that was too low said "Go LOWER!" and a guess too high said "Go HIGHER!"
2. **Off-by-one attempts** — `attempts` started at `1` while the submit handler also incremented it, so "Attempts left" was wrong and the player was cut off one guess early (Normal stopped at 7 instead of 8); it also inflated the score's attempt number.
3. **Hardcoded range** — the prompt always said "between 1 and 100" and New Game regenerated the secret with `randint(1, 100)`, ignoring the selected difficulty's range.
4. **Enter didn't submit** — the guess input used a standalone button, so pressing Enter never registered a guess.
5. **New Game didn't fully reset** — it left `status`, `history`, and `score` untouched, so after a loss the "Game over" screen blocked restarting.
6. **Difficulty change didn't regenerate the secret** — switching difficulty kept the old secret (and old range).

**Fixes applied.**
1. Swapped the hint messages in `check_guess` so they point the correct direction.
2. Initialized `attempts` to `0` in all three places (init path, the session-state guard, and New Game) to match the `+= 1` in the submit handler.
3. Used `get_range_for_difficulty` for the prompt text and for the secret in New Game so the range follows the chosen difficulty.
4. Wrapped the input + submit button in `st.form` so Enter submits the guess.
5. Made New Game reset `attempts`, `secret`, `status`, `history`, and `score`.
6. Detected difficulty changes and regenerated the secret with the correct range.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Launch the app and start on **Normal** difficulty — guess a number between 1 and 100, with 8 attempts allowed.
2. Enter a guess of `40` and submit (pressing Enter now works); the game returns "📈 Go HIGHER!" because the guess is too low.
3. Enter `70` → the game returns "📉 Go LOWER!" because the guess is too high — the hints now point in the correct direction.
4. After each guess the secret number stays fixed and the score and "Attempts left" counter update correctly.
5. Enter the correct number → the game shows "🎉 Correct!", celebrates with balloons, and ends; click **New Game 🔁** to reset and play again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest tests/ -v
============================= test session starts ==============================
platform darwin -- Python 3.13.7, pytest-9.0.3, pluggy-1.6.0
collected 22 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  4%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [  9%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 13%]
tests/test_game_logic.py::test_hint_message_when_guess_too_high PASSED   [ 18%]
tests/test_game_logic.py::test_hint_message_when_guess_too_low PASSED    [ 22%]
tests/test_game_logic.py::test_easy_difficulty_range PASSED              [ 27%]
tests/test_game_logic.py::test_normal_difficulty_range PASSED            [ 31%]
tests/test_game_logic.py::test_hard_difficulty_range PASSED              [ 36%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numeric_string PASSED [ 40%]
tests/test_game_logic.py::test_parse_guess_rejects_empty_string PASSED   [ 45%]
tests/test_game_logic.py::test_parse_guess_rejects_none PASSED           [ 50%]
tests/test_game_logic.py::test_parse_guess_accepts_negative_number PASSED [ 54%]
tests/test_game_logic.py::test_parse_guess_truncates_float_string PASSED [ 59%]
tests/test_game_logic.py::test_parse_guess_rejects_whitespace PASSED     [ 63%]
tests/test_game_logic.py::test_is_in_range_accepts_value_inside_range PASSED [ 68%]
tests/test_game_logic.py::test_is_in_range_accepts_boundaries PASSED     [ 72%]
tests/test_game_logic.py::test_is_in_range_rejects_negative PASSED       [ 77%]
tests/test_game_logic.py::test_is_in_range_rejects_value_above_range PASSED [ 81%]
tests/test_game_logic.py::test_describe_guess_too_low_shows_higher_hint PASSED [ 86%]
tests/test_game_logic.py::test_describe_guess_too_high_shows_lower_hint PASSED [ 90%]
tests/test_game_logic.py::test_describe_guess_correct_shows_win_marker PASSED [ 95%]
tests/test_game_logic.py::test_describe_guess_invalid_entry_flagged PASSED [100%]

============================== 22 passed in 0.02s ===============================
```

## 🚀 Stretch Features

- **Guess History sidebar (Agent Mode, SF8):** the sidebar shows every guess made this game as a numbered list, each annotated with the hint it earned (📈 higher / 📉 lower / 🎉 correct), and flags rejected input as invalid. Implemented via `describe_guess` in `logic_utils.py` and rendered in `app.py`. See the "Agent Workflow" section of `ai_interactions.md`.
- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
