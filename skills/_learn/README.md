# Learning skills

Five skills that help an agent teach one learner over several sessions, and a small Python CLI that keeps what was learned in plain text.

## The skills

Run in this order for a new topic:

1. `learn-ground` asks diagnostic questions to find what the learner already holds and where it breaks.
2. `learn-plan` turns that into a short plan with a check and an expected answer for each step.
3. `learn-teach` teaches the plan, asking the learner to predict or attempt before it explains.
4. `learn-record` writes the verified claims to the graph and links the session's questions to them, so they come due for review. The question results and the learner's false beliefs are recorded as they happen, by `learn-ground`, `learn-teach` and `learn-review`.
5. `learn-review` runs later: it finds what is due and asks the learner to rebuild it from memory.

`learn-review` also runs when a sitting starts without a new topic and something is due. A learner who brings a new topic starts with `learn-ground`, which probes the due items on that topic and says that a review is waiting.

## Install

Copy or symlink every `skills/learn-*` directory and `skills/_learn` into your agent's skills directory. Keep the `_learn` directory name: the skills call `_learn/scripts/learn.py`. You need Python 3 and nothing else.

## The store

State lives in a `.learn/` directory at the project root: JSON Lines files for claims, questions and false beliefs, and markdown files for each session's grounding, plan and transcript. It is yours. Read it, edit the markdown, or delete it. The JSONL files are append-only, so corrections are new lines rather than edits; `skills/_learn/store.md` lists every file and record.

To see what the system thinks you know:

```
python3 skills/_learn/scripts/learn.py show
```

It prints a markdown summary of what was taught, what is retained, and the false beliefs recorded. No score is stored; statuses and due dates are worked out from the record each time.

## Limits

The method is assembled from adjacent research on retrieval practice, spacing and misconceptions. It has not been evaluated in an LLM chat tutor, and the research behind its parts does not show that it works there. The question budgets (3 to 5 per strand, 12 to 20 per session) and the review intervals (1, 3, 7, 21 and 60 days) are defaults chosen for this project, not findings; tune them. The skills tell the learner this up front, along with the warning that attempting first feels harder than being told.
