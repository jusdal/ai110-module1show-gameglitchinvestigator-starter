# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used:** "Write pytest cases for the `parse_guess` function in logic_utils.py that target tricky edge cases — empty input, non-numeric strings, whitespace-only input, negative numbers, and float-like strings. Assert on the exact `(ok, value, error)` tuple it returns."

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Non-numeric string (`"abc"`) | (see prompt above) | `test_parse_guess_rejects_non_numeric_string` — expects `(False, None, "That is not a number.")` | ✅ Yes | Players will mistype letters; the parser must reject them with a clear error instead of crashing the app. |
| Empty input (`""`) | (see prompt above) | `test_parse_guess_rejects_empty_string` — expects `(False, None, "Enter a guess.")` | ✅ Yes | Submitting a blank box is the most common accidental input; it should prompt for a guess, not count as a 0. |
| Missing input (`None`) | (see prompt above) | `test_parse_guess_rejects_none` — expects `(False, None, "Enter a guess.")` | ✅ Yes | Guards the `None` branch so the function degrades gracefully instead of raising on a missing value. |
| Negative number (`"-5"`) | (see prompt above) | `test_parse_guess_accepts_negative_number` — expects `(True, -5, None)` | ✅ Yes | Confirms negatives parse as valid ints — parsing and range-checking are separate concerns, and I wanted to pin that contract. |
| Float string (`"3.7"`) | (see prompt above) | `test_parse_guess_truncates_float_string` — expects `(True, 3, None)` | ✅ Yes | The code intentionally truncates floats; this test documents that behavior so a future change can't silently break it. |
| Whitespace only (`"   "`) | (see prompt above) | `test_parse_guess_rejects_whitespace` — expects `(False, None, "That is not a number.")` | ✅ Yes | Whitespace looks "empty" to a user but isn't `""`; this verifies it still gets rejected. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
