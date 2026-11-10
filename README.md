# Learning skills

Five agent skills that help someone learn a topic over several sessions, and a small Python CLI that keeps what was learned in plain text so the next session builds on it.

A session finds what the learner already holds, plans from there, teaches one step at a time with the learner attempting first, and records what was taught. Later sessions ask the learner to rebuild it from memory, spaced out over days and weeks.

## The skills

| Skill | What it does |
|---|---|
| `learn-ground` | Sets a concrete goal and asks a short run of diagnostic questions to find where teaching should start. |
| `learn-plan` | Turns that into a short plan, with a check and an expected answer written down for each step. |
| `learn-teach` | Teaches the plan one step at a time; the learner predicts or attempts before the explanation. |
| `learn-record` | Writes the verified claims to the store and links the session's questions to them, so they come due for review. |
| `learn-review` | Finds what is due and asks the learner to reconstruct it from memory, without showing it first. |

For a new topic they run in that order. `learn-review` runs on its own in later sittings.

## Install

Copy or symlink every `skills/learn-*` directory and `skills/_learn` into your agent's skills directory. Keep the `_learn` name, because the skills call `_learn/scripts/learn.py`. You need Python 3.11 or later and nothing else.

Then ask your agent to teach you something, for example "I want to understand why binary search is O(log n)".

## The store

Everything is kept in a `.learn/` directory in the project where you run the skills: JSON Lines files for claims, question results and recorded misconceptions, and markdown files for each session. It is yours to read, edit or delete. The JSONL files are append-only, so a correction is a new line.

To see what has been recorded about you:

```
python3 skills/_learn/scripts/learn.py show
```

No score is stored. Statuses (`taught`, `retained`, `lapsed`) and review dates are worked out from the record each time.

## What is in this repo

| Path | Contents |
|---|---|
| `skills/learn-*/SKILL.md` | The five skills. |
| `skills/_learn/theory.md` | The twelve rules the skills share, each with the research it rests on. |
| `skills/_learn/store.md` | The store layout, record formats and every CLI command. |
| `skills/_learn/scripts/` | The CLI (`learn.py`) and its library. Standard library only. |
| `tests/learn/` | Tests for the CLI and a lint for the skill files. Run with `python3 -m pytest tests/learn -q`. |
| `research_notes/` | The literature review the design is based on. |
| `docs/superpowers/plans/` | The implementation plan the skills were built from. |

## Limits

The method is assembled from adjacent research on retrieval practice, spacing, diagnostic assessment and misconceptions. It has not been evaluated in an LLM chat tutor, and that research does not show that it works there. The question budgets and review intervals are defaults chosen for this project, not findings. The skills have been tried in two short role-played sessions and not with real learners over time.

Expect sessions to feel harder and slower than being told the answer; the skills say so up front.

## License

MIT. See [LICENSE](LICENSE).
