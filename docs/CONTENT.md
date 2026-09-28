# Writing content

Content is code. A module is a Python file; a game is a dictionary in a registry.
This keeps the curriculum reviewable, diffable and testable without a database.

## Categories

`content/categories.py` holds the twelve categories. Each carries a name, a
short icon key, a hex colour and a one-line blurb. The front end renders the
grid from this dictionary — adding a category is adding an entry.

## Modules

```python
MODULES = [
  {
    "id": "web-sqli",
    "cat": "web",
    "title": "SQL Injection",
    "tier": "Easy",
    "summary": "One line for the catalogue card.",
    "read": ["Paragraph one.", "Paragraph two."],
    "quiz": [
      {"q": "Which character starts a comment...", "a": ["--", "#", "/*"], "c": 0},
    ],
  },
]
```

Files in `content/modules/` are auto-discovered; a filename beginning with an
underscore is skipped, which is the way to park unfinished material without
breaking the build. The quiz `c` field is the index of the correct option and is
stripped before the module is sent to the browser.

## Games

Forty-one exercises live in `games/registry.py`. Four kinds, each with a
front-end renderer:

| kind | shape | used for |
|---|---|---|
| `quiz` | multiple choice, timed rounds | recall and interpretation |
| `input` | free-text answer, validated server-side | short exact answers, speedruns |
| `builder` | ordered list or single pick | sequencing, assembling a config |
| `simulator` | bespoke interactive component | the network simulator and terminal |

Answer banks live in `games/banks/` — JSON for hand-written material, and Python
generators where the questions should be produced rather than typed
(`networking.py`, `linux.py`). Grading rules are in `app/grader.py`:

- numeric input answers compare as floats with a tolerance
- builder answers compare an ordered list for sequence games, or a single index
  for pick-one games
- quiz answers compare the option index

## Conventions that keep grading honest

- Never send the answer to the browser: `c`, `order` and `correct` are stripped
  from the payload the API returns.
- Keep the answer derivable from the material. A quiz question whose answer is
  not in the reading is a bug, not a challenge.
- For boxes, the flag is random but the path is fixed — write hints against the
  path, never against the flag value.
