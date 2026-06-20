import random
import streamlit as st

from logic_utils import (
    check_guess,
    describe_guess,
    get_range_for_difficulty,
    is_in_range,
    parse_guess,
    update_score,
)


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

#FIX: Detect difficulty changes and regenerate secret with correct range. Previously, changing difficulty kept the old secret. Used Claude Code.
if "difficulty" not in st.session_state or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    #FIX: Start attempts at 0 (was 1). attempts is incremented at the top of the submit handler, so a starting value of 1 pre-counted a phantom guess — causing an off-by-one in "Attempts left", cutting the player off one guess early, and inflating the score's attempt_number. Now consistent with the New Game reset. Used Claude Code.
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
else:
    if "secret" not in st.session_state:
        st.session_state.secret = random.randint(low, high)

    #FIX: Start attempts at 0 (was 1), matching the init path above and the New Game reset. Used Claude Code.
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "status" not in st.session_state:
        st.session_state.status = "playing"

    if "history" not in st.session_state:
        st.session_state.history = []

st.subheader("Make a guess")

#FIX: Display the correct range for the selected difficulty instead of hardcoding 1-100. Used Claude Code.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

#FIX: Wrapped the guess input and submit button in st.form so pressing Enter submits the guess. Previously a standalone st.button was only True on a physical click, so the Enter-triggered rerun never registered a submission. Used Claude Code.
with st.form(key=f"guess_form_{difficulty}"):
    raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")
    submit = st.form_submit_button("Submit Guess 🚀")

col2, col3 = st.columns(2)
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

#FIX: New Game button now properly resets all game state including status, history, and score. Previously forgot to reset status to "playing", which blocked game restart. Used Claude Code.
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        #FIX: Invalid (non-numeric/empty) input is rejected without
        # consuming an attempt — only a legal, in-range guess costs a turn.
        st.session_state.history.append(raw_guess)
        st.error(err)
    elif not is_in_range(guess_int, low, high):
        #FIX: Out-of-range guesses (e.g. negatives or numbers above the
        # range) are rejected without consuming an attempt — a friendlier
        # UX than silently wasting a turn on an impossible guess.
        st.warning(f"Out of range — guess between {low} and {high}.")
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# Guess History sidebar (Stretch Feature SF8). Rendered after the submit
# handler so it includes the guess made on this rerun.
st.sidebar.divider()
st.sidebar.subheader("📜 Guess History")
if not st.session_state.history:
    st.sidebar.caption("No guesses yet.")
else:
    for i, past in enumerate(st.session_state.history, start=1):
        summary = describe_guess(past, st.session_state.secret)
        st.sidebar.write(f"{i}. {summary}")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
