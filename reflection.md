# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  The game looked pretty good.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  1. The Hint should've been higher but it kept saying lower (#FIXED)
  2. New Game button doesn't work (#FIXED)
  3. Easy mode gave me 100 but it should've given me a number between 1 and 10 (#FIXED)
  4. Hard range should be 1-1000? or at least higher than 100 (normal) (#NOTABUG - 1-50 but less guesses)
  5. Hitting Enter doesn't work to submit the guess (#FIXED)
  6. Attempts starts at 1; should start at zero? (#FIXED)
  7. Are the attempts correct? I think Normal (should be 8 attempts) stops at 7 (#FIXED - same root cause as #6)

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input                         | Expected Behavior                     | Actual Behavior                      | Console Output / Error |
| ----------------------------- | ------------------------------------- | ------------------------------------ | ---------------------- |
| 35                            | Should say higher                     | says lower                           |                        |
| 29                            | Error message? # below 20 for easy    | says lower                           |                        |
| 19                            | "Go HIGHER!"                          | "Go LOWER!                           |                        |
| New game on Normal            | "Attempts left: 8" before first guess | showed "Attempts left: 7"            |                        |
| 8 guesses on Normal (limit 8) | Allowed 8 guesses                     | Cut off after 7 ("Out of attempts!") |                        |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  Claude Code (in VS Code)

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  Claude Code suggested flipping the hints associated with an incorrect guess and was correct. I accepted these edits and the game worked as expected. I also added two tests to the pytest file and made sure it passed those as well as my manual testing in the web app.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  I suspected Hard mode's range was wrong and should go up to ~1000. I checked this against the code in get_range_for_difficulty and confirmed Hard is intentionally 1–50 with fewer guesses, so my hunch was a false alarm (#NOTABUG). It reminded me to verify a suspected bug against the actual code before "fixing" it.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I tested manually in the web app looking carefully for expected behavior and also added tests into my pytest file and ran it.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  I ran pytest tests/test_game_logic.py and all 8 tests passed in about 0.01s. The two I added myself — test_hint_message_when_guess_too_high and test_hint_message_when_guess_too_low — check the exact hint text ("Go LOWER!" / "Go HIGHER!"). They mattered because the original bug wasn't that the outcome was wrong, it was that the message pointed the wrong way, so asserting on the message string is what actually caught the regression.

- Did AI help you design or understand any tests? How?
  Yes. After the hint tests were generated, I asked Claude Code to explain why each one was written and the logic behind it. The useful part was understanding why test_hint_message_when_guess_too_high asserts on the exact message string ("Go LOWER!") and not just the outcome — since the bug was a backwards message, not a wrong result, checking the outcome alone wouldn't have caught it. That explanation helped me see what a test is actually protecting against, so I could tell whether the test was meaningful rather than just passing.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Streamlit re-runs the entire script top to bottom every time you interact with the page — click a button, type in a box, anything. So normal Python variables get wiped and recreated on every interaction, like the page has amnesia. st.session_state is the workaround: it's a dictionary that survives those reruns, so that's where you keep things that must persist, like the secret number, the score, and the attempts count. A lot of the bugs in this project came from state being reset (or not reset) at the wrong time during a rerun.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    Tracing the code by hand before accepting a fix. With the attempts bug, reading how attempts was used (incremented before the guess is processed) is what told me 0 was correct and that two spots needed the change — not just guessing.

- What is one thing you would do differently next time you work with AI on a coding task?
  I'd write a failing test first to reproduce a bug before fixing it, instead of mostly testing manually in the web app and adding tests afterward. That way I'd know for sure the test actually catches the bug.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  AI code can look polished and even label itself "production-ready" while hiding real bugs, so confident-sounding code still needs to be read and tested. I trust it more as a fast teammate for spotting and explaining issues, and less as a final authority.
