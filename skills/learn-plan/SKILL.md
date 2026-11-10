---
name: learn-plan
description: Use when a session has a grounding.md and no approved plan.md
---

# learn-plan

Turns a session's grounding into a teaching plan the learner approves. You plan; you do not teach and you write no observations. Shared rules live in [theory](../_learn/theory.md); the store, CLI fields and the `plan.md` template live in [store](../_learn/store.md). Read both before starting.

## When to use

- `.learn/sessions/<id>/grounding.md` exists and `plan.md` does not, or the learner has not yet approved it.
- Not for probing (`learn-ground`), teaching (`learn-teach`), recording to the graph (`learn-record`) or review (`learn-review`).

## Reads

- `.learn/sessions/<id>/grounding.md`: goal, success criteria, per-strand floor and ceiling, misconceptions.
- The store via the CLI only. Call it as `python3 <skills-dir>/_learn/scripts/learn.py`; below, `learn.py <subcommand>`. Global flags (`--root`, `--now`) go before the subcommand.
- `learn.py observations --session <id>`: the grounding questions. Each line's `target.id` is a probe slug (or a store id), with its `prompt`, `response`, `confidence` and `grade`.
- `learn.py misconceptions` (prints the latest record per misconception, each with `stability` and `status`; `--status confirmed` filters). The grounding file lists only ids and statements.
- Sources the learner supplies, then web or file tools if you have them.

## Procedure

1. Read `grounding.md`, and run `learn.py observations --session <id>` to see which probe slugs exist and what each question tested. Run `learn.py graph` to see the current nodes and chains. Then, for the goal and for each strand, find propositions already in the store; `candidates` takes a statement and returns up to 5 ids by word overlap, so read the returned nodes in `graph` before deciding any is the same claim. Run `learn.py state --target <id>` on each hit to see whether it is `taught`, `retained` or `lapsed`.

   ```
   python3 <skills-dir>/_learn/scripts/learn.py observations --session 20261109-heidegger
   python3 <skills-dir>/_learn/scripts/learn.py graph
   python3 <skills-dir>/_learn/scripts/learn.py candidates --statement "tools are encountered through use"
   python3 <skills-dir>/_learn/scripts/learn.py state --target n-4ef8ad36
   ```

   `candidates` prints `[{"id","score"}]`; `state` prints `[]` for a target with no observations.
2. Gather sources: texts the learner supplies first, then web or file tools if available. List them under `## Sources`, each with what it supports. With no sources, write the single line `Unverified: no sources available this session` and tell the learner that everything here is tutor-asserted ([theory](../_learn/theory.md#T10), theory.md#T10).
3. Write the goal as the simplest true version of the whole, in one paragraph (`## Goal in one paragraph`).
4. Build the prerequisite map from each strand's floor up to the success criteria: nothing below a floor, nothing above the goal, no tangents however interesting. Draw it as the mermaid graph in the template; node names are the landmark slugs. The map ends in a single sink landmark, the one every success criterion rests on; if the criteria need several end points, add one landmark that joins them. Where a landmark covers the same claim as a grounding probe slug, use that probe slug as the landmark slug, so the probe answers and the teaching later count toward the same node.
5. Choose each landmark's move ([theory](../_learn/theory.md#T2), theory.md#T2):
   - `attempt-first` when its premises are held.
   - `assert` when it cannot be derived from what is held.
   - `refute` for each misconception whose latest record has `status` `confirmed` and `stability` `stable`. Get these from `learn.py misconceptions --status confirmed`, matching the `m-` ids in `grounding.md`. Write the id with the move: `refute m-1a2b3c4d`.
   - `discriminate` for every other one: a `stability` that is not `stable` (shifting or one-off) or a `status` that is not `confirmed` (e.g. `suspected`) is planned as `discriminate m-…`, never `refute` (theory.md#T7).
   - `contrast` for each landmark a success criterion depends on: one paired contrasting case, principle stated after the comparison, not before. It is added to the landmark's primary move in the same column: `attempt-first + contrast`.
6. Where a strand's floor is low, add the connecting steps explicitly; where it is high, keep it lean. Split any landmark that needs several unheld ideas related at once.
7. For every landmark write the claim, its epistemic status and source, the check (apply, predict or explain-why, never parrot), the expected answer, and the wrong models with what each would reveal. Write them now so `learn-teach` can pre-commit them before each reply ([theory](../_learn/theory.md#T4), theory.md#T4). For an `attempt-first` landmark the check is the attempt itself: a prediction asked before any explanation, whose expected answer is the claim. For a `refute` landmark the check must be one the misconception gets wrong, and the move follows state-it, say-it-is-wrong, explain-why, then the check ([theory](../_learn/theory.md#T7), theory.md#T7).
8. Mark held landmarks. A landmark is held when grounding showed the learner holds its claim (its strand is `held-to-goal`, or the floor is at or above it) or when it reuses a store node. Write `held (retrieve, do not re-teach)` in its grounding status column, plus the `n-` id when it reuses a node. It keeps a full row (claim, check, expected answer, wrong models, and the move to use if the cold check is missed): `learn-teach` asks its check cold and teaches only on a miss, and `learn-record` writes its node from the claim column.
9. Write `## Final tasks`: a closed-transcript teach-back of the goal and one transfer question on a case not used in the plan, with scoring points taken from the landmark chain.
10. Show the map and ask exactly two things: is this the goal you meant, and do you really hold the landmarks marked held? Revise until approved. Do not ask the learner to validate the dependency structure; ordering is yours ([theory](../_learn/theory.md#T11), theory.md#T11). Write `plan.md` only once approved. Then hand off: stop following this skill, open [`learn-teach/SKILL.md`](../learn-teach/SKILL.md) now and follow it from its first step before sending the learner anything else.

## Hard rules

- Assert only what cannot be derived from what is held; everything else is `attempt-first` (theory.md#T2).
- Each landmark has one inference and one check, and a written expected answer and wrong models (theory.md#T4).
- The map ends in a single sink landmark; a landmark that matches a probe slug's claim uses that slug.
- A suspected misconception is never refuted; plan `refute` only for confirmed, stable ones (theory.md#T7).
- Every landmark states its epistemic status; with no source it is `tutor-asserted`, and the plan says `Unverified` (theory.md#T10).
- The learner owns the goal and confirms what they hold; you own sequence and sourcing (theory.md#T11).
- Store no scores or percentages. Do not edit `graph/` or `learner/`.

## Writes

- `.learn/sessions/<id>/plan.md`, using the template in [store](../_learn/store.md) with headings unchanged. The grounding status column holds the strand status or `held (retrieve, do not re-teach)`; reused store nodes also carry their `n-` id.
- Nothing else. No observations, misconceptions, nodes, chains or links.
