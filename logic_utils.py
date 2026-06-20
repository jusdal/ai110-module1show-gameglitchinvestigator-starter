"""Pure game-logic helpers for the Game Glitch Investigator app.

These functions hold all the rules of the guessing game (ranges, input
parsing, hint direction, range checks, and scoring) with no Streamlit or
UI dependencies, so they can be unit-tested in isolation.
"""


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a difficulty level.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A ``(low, high)`` tuple of ints. Unknown values fall back to the
        Normal range ``(1, 100)``.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """Parse raw user input into an integer guess.

    Accepts integer strings and truncates float-like strings (e.g. "3.7"
    becomes 3). Empty, ``None``, and non-numeric inputs are rejected.

    Args:
        raw: The raw string entered by the player (or ``None``).

    Returns:
        A ``(ok, guess_int, error_message)`` tuple. On success ``ok`` is
        ``True``, ``guess_int`` is the parsed int, and ``error_message`` is
        ``None``. On failure ``ok`` is ``False``, ``guess_int`` is ``None``,
        and ``error_message`` describes the problem.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess to the secret and return the outcome and hint.

    The hint direction was reversed in the original starter code; it now
    correctly tells the player to go LOWER when their guess is too high and
    HIGHER when it is too low. A ``TypeError`` fallback handles the case
    where the secret has been coerced to a string elsewhere.

    Args:
        guess: The player's parsed integer guess.
        secret: The secret number (normally an int).

    Returns:
        A ``(outcome, message)`` tuple where ``outcome`` is one of "Win",
        "Too High", or "Too Low" and ``message`` is the player-facing hint.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def is_in_range(value: int, low: int, high: int):
    """Return True if value lies within the inclusive ``[low, high]`` range.

    Args:
        value: The integer guess to check.
        low: The inclusive lower bound.
        high: The inclusive upper bound.

    Returns:
        ``True`` if ``low <= value <= high``, otherwise ``False``.
    """
    return low <= value <= high


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Compute the player's new score after a guess.

    A win awards more points the earlier it happens (floored at 10). A
    wrong guess generally costs 5 points.

    Args:
        current_score: The score before this guess.
        outcome: The outcome from :func:`check_guess`.
        attempt_number: The 1-based number of the current attempt.

    Returns:
        The updated score as an int.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
