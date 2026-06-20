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
Add professional docstrings to every function in logic_utils.py
(Args/Returns style), then run pycodestyle and fix any PEP 8
violations without changing behavior. Show me the linter output
before and after.
```

**Linting output before:**

```
$ python -m pycodestyle logic_utils.py
logic_utils.py:1:80: E501 line too long (82 > 79 characters)
logic_utils.py:38:1: E265 block comment should start with '# '
logic_utils.py:38:80: E501 line too long (128 > 79 characters)
```

**Linting output after:**

```
$ python -m pycodestyle logic_utils.py
$ echo $?
0
```

(No output and exit code 0 means zero PEP 8 violations.)

**Changes applied:**

- **Module docstring:** the AI suggested replacing the over-length top-of-file `# FIX:` comment (E501) with a proper module docstring describing the file's purpose. Applied.
- **Comment style (E265):** the inline `#FIX:` provenance comment above `check_guess` was missing the space after `#` and ran to 128 characters. The AI suggested folding that note into the function's docstring instead of keeping a long block comment. Applied.
- **Professional docstrings:** expanded every function's docstring to an Args/Returns format (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `is_in_range`, `update_score`). Applied.
- **Type hints:** the AI initially dropped the existing parameter type hints; I asked it to keep them since they pair well with the docstrings, so `: str` / `: int` annotations were restored and also added to `is_in_range`. (Manual correction.)
- Verified the refactor was behavior-preserving by re-running `pytest` — all 18 tests still pass.

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
