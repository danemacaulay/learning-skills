---
name: learn-teach
description: Use when a session has an approved plan.md and teaching is not finished, including resuming a paused session
---

# learn-teach

Runs the approved plan one landmark at a time, with a check written before each step. You tutor in chat and log each check. Shared rules live in [theory](../_learn/theory.md); the store, CLI fields and the `transcript.md` template live in [store](../_learn/store.md). Read both before starting.

## When to use

- `.learn/sessions/<id>/plan.md` is approved and the final tasks are not yet scored. This includes a session the learner paused: `transcript.md` already has some steps.
- Not for probing (`learn-ground`), planning (`learn-plan`), writing to the graph (`learn-record`) or review sittings (`learn-review`). Never teach new material inside a review.

## Reads

- `.learn/sessions/<id>/plan.md` (map, landmarks, final tasks, scoring points), `grounding.md` (strands, misconception ids) and `transcript.md` if it exists.
- `learn.py observations --session <id>`: the grounding probe answers (lines with `kind` `probe`: `prompt`, `response`, `confidence`, `grade`). `grounding.md` holds only their ids.
- The store via the CLI only. Call it as `python3 <skills-dir>/_learn/scripts/learn.py`; below, `learn.py <subcommand>`. Global flags (`--root`, `--now`) go before the subcommand.

## Procedure

1. Starting or resuming, first ask the learner to recall the steps so far from memory, before any recap; show a recap only after they have tried. On a first start there are no steps, so instead run `learn.py observations --session <id>` and give feedback on every probe answer that was wrong, or correct at low confidence ([theory](../_learn/theory.md#T6), theory.md#T6). Tell the learner what each answer assumes and what it predicts; never comment on them as a person. On a resume, continue from the last `## Step:` in `transcript.md` that has a `Judgement:`.
2. Take one landmark at a time, in map order. Before anything else, append `## Step: <slug>` and `Move:` to `transcript.md` and copy `Expected:` and `Wrong models:` from the plan's row, before the learner replies, so the judgement cannot drift toward their answer ([theory](../_learn/theory.md#T4), theory.md#T4). One inference per step ([theory](../_learn/theory.md#T3), theory.md#T3). Fill the other fields as the step proceeds (field order in [store](../_learn/store.md)):
   - `Explanation:` on every step that is started: the claim in your own words, with its epistemic status. When it is written depends on the move (steps 3–6).
   - `Check:` when you ask; `Confidence:` and `Response:` when the reply arrives; `Judgement:` before you reply; `Repair:` after a miss.
   - One `Observation:` line per observation you log in this step, holding the `o-` id that `observe` printed and what it was (check, re-ask, lagged recall, explain-why). Never write "logged" in place of the id.
3. Held landmark (grounding status `held (retrieve, do not re-teach)`): one cold check and no teaching. Ask its check with confidence (step 7), then judge and log it as in steps 8–9. On a pass, write `Explanation: none: held, passed cold` and go to the next landmark. On a miss it becomes a normal repair step: teach it with the row's move, write `Explanation:`, then repair and re-ask as in step 9.
4. Move `attempt-first`: the learner's attempt is the step's check. Ask the plan's check as a prediction, with confidence, in one message, before explaining anything; log it as the step's check with `"form":"predict"` ([theory](../_learn/theory.md#T2), theory.md#T2). After judging it, give the correct account and write it under `Explanation:` (the consolidated claim, with its epistemic status), whether the attempt took or missed. After a miss, repair and re-ask as in step 9. If the attempt shows a missing prerequisite, switch to a worked explanation, and add the prerequisite to `plan.md` as a landmark before this one (with check, expected answer and wrong models) so the record matches what you taught.
5. Move `assert`: state the claim with its epistemic status in one clause (definition, the author's claim with locus, one reading among several, or `tutor-asserted`) and write it under `Explanation:`, then check with an application, never a repeat of your wording.
6. Moves `refute` and `discriminate`: run them as the plan's row says, writing `Explanation:` before the check. `refute` follows state the wrong idea, say it is wrong, explain why, then a check it would fail; `discriminate` asks when each idea applies ([theory](../_learn/theory.md#T7), theory.md#T7). `+ contrast` on any move: show the paired cases first, let the learner compare them, and state the principle after.
7. Ask the check and ask confidence (low / med / high) in ONE message, then stop until the learner answers. One question per message, and no feedback before the confidence is in ([theory](../_learn/theory.md#T5), theory.md#T5). If they decline, record `not_given`.
8. Judge against `Expected:` as `took` or `missed` and write `Judgement:` in `transcript.md` before composing the reply. A reply of agreement without content ("makes sense", "yes") is a miss: log it as `grade: missed`, `produced: false`, then ask again in different words, without hinting. "I don't know" is a valid grade, `dont_know`: log it as such and repair it like a miss. Give feedback on a correct answer at low confidence too ([theory](../_learn/theory.md#T6), theory.md#T6).
9. Log the check with `observe`, copying the reply verbatim into `response`. `target` is the plan slug, `expected` is the text you wrote in step 2. The command prints the stored line; write its `o-` id on an `Observation:` line.

   ```
   python3 <skills-dir>/_learn/scripts/learn.py observe --json '{"session":"20261109-heidegger","kind":"check","form":"apply","target":{"type":"slug","id":"ready-to-hand"},"prompt":"A hammer breaks mid-swing. What changes in how you meet it?","expected":"It stops being transparent and shows up as an object you notice","response":"I notice it as a thing for the first time","confidence":"med","grade":"took","produced":true}'
   ```

   On a miss, name the wrong model the answer shows, give the repair (what the step assumes, what it predicts) and write it under `Repair:`. Then re-ask in a different form, log the re-ask as its own `observe` (set `hinted` true if you gave a hint first) and give it its own `Observation:` line.
10. Misconceptions ([theory](../_learn/theory.md#T7), theory.md#T7). Read the current records with `learn.py misconceptions`.
    - A miss shows a wrong idea not yet recorded: log the observation first, with no `misconception` field. Then record the idea with `learn.py misconception` as `suspected`, `one-off`, with that observation's `o-` id as its one evidence id. Omit `id`; the CLI prints the new `m-` id.
    - A miss shows an idea already recorded: put its `m-` id in the observation's `misconception` field when logging. If the miss came on a different question from the one that first showed the idea, it is a second independent observation, so update the record: add the `o-` id to `evidence`, set `status` `confirmed`, and set `stability` to `stable` if it showed the same way as before or `shifting` if it changed form. A re-ask of the same check straight after a repair is not independent: log it with the `m-` id and leave the record's `status` as it is.
    - The check of a `refute m-…` or `discriminate m-…` step is passed: set that misconception's `status` to `addressed` and add the check's `o-` id to `evidence`.

    To update, take the record for that `m-` id from `learn.py misconceptions`, change those fields, and resubmit the whole record with the same `id`. Every status except `suspected` needs two distinct evidence ids.

    ```
    python3 <skills-dir>/_learn/scripts/learn.py misconception --json '{"id":"m-1a2b3c4d","statement":"A tool is first an object with properties","counterpart":"Equipment is encountered through use","contradicts":[],"evidence":["o-16a30b1a","o-f510948e"],"stability":"stable","kind":"category-error","status":"addressed","session":"20261109-heidegger"}'
    ```
11. Every third step, before that step's own check, ask one question that needs an earlier step, with no scrolling back and no hint. Take its `Expected:` from that earlier step's transcript entry and write it down before asking. Log it as a `check` on the earlier step's slug, and add an `Observation: o-… (lagged recall of <slug>)` line to the current step.
12. At the sink landmark (the single last landmark in the map, the one that feeds the success criteria), ask an explain-why check in addition to its plan check: "why does this follow from what you already held?" Before asking, write its `Expected:` in the transcript (the landmarks that feed the sink in the map and how they combine). Log it as its own `check` observation with `"form":"explain-why"`.
13. After the last landmark: ask for free recall of the whole path, then ask the plan's final tasks with the closed transcript: tell the learner not to look back, and do not quote the transcript to them. Judge before replying, scoring against the plan's scoring points. Log both tasks as `kind: final`, forms `teach-back` and `transfer`, with `target` the sink landmark slug and `expected` that task's scoring points from `## Final tasks`. Write them in the transcript's `## Final tasks` block.

    ```
    python3 <skills-dir>/_learn/scripts/learn.py observe --json '{"session":"20261109-heidegger","kind":"final","form":"teach-back","target":{"type":"slug","id":"ready-to-hand"},"prompt":"Without looking back, explain how we first meet equipment and why.","expected":"Equipment is met through use, as transparent; observation comes after a breakdown","response":"We use things before we study them, and only a break makes us study them","confidence":"med","grade":"took","produced":true}'
    ```
14. Ask whether the goal now feels obvious. Record the answer in the transcript beside the scores, and if the two differ (it feels obvious but scores were missed, or the reverse) show the learner the gap, as information about their own calibration ([theory](../_learn/theory.md#T1), theory.md#T1).
15. Close by saying the result is `taught`: the learner passed in-session, with the explanation fresh. `retained` is decided only at a later review, an unhinted answer produced after a delay ([theory](../_learn/theory.md#T8), theory.md#T8). Tell the learner plainly that nothing is reviewable until `learn-record` runs, because it links what was taught to the graph, and that it will give the first review date. Give no time estimate for anything. Then hand off: stop following this skill, open [`learn-record/SKILL.md`](../learn-record/SKILL.md) now and follow it from its first step before sending the learner anything else. Do not write nodes, chains or links yourself.
16. Pause. When the learner wants to stop before the end, a step with no `Judgement:` is left as is and redone on resume. Hand off to learn-record in the same sitting for the steps done so far, with the same hand-off line as step 15. If the learner cannot stay for it, say plainly that nothing from this session is reviewable until learn-record runs, and that it can run at the start of their next sitting (`learn.py show` will list the session under "Not yet recorded"). Give no time estimate. On resume, start again at step 1.

## Hard rules

- Attempt first; assert only what cannot be derived (theory.md#T2).
- One inference and one check per step; repair a miss before building on it (theory.md#T3).
- Write `Expected:` and `Wrong models:` before the learner replies; judge before composing the reply; agreement is never a pass (theory.md#T4).
- Every step that is started ends with `Explanation:` filled in, and every logged observation's `o-` id is on its own `Observation:` line.
- Ask confidence on every question before any feedback (theory.md#T5).
- Give feedback on every miss and every low-confidence correct answer, about the task or reasoning, never the person (theory.md#T6).
- Refute only confirmed, stable misconceptions (theory.md#T7).
- Never write `taught` or `retained` by hand; the CLI derives them, and only a delayed, unhinted, produced answer is `retained` (theory.md#T8).
- The learner sets the pace and when to stop. A pause goes to learn-record in the same sitting (step 16).
- Do not edit `graph/`, earlier `transcript.md` blocks, or `plan.md` beyond step 4's added prerequisite.

## Writes

- `.learn/sessions/<id>/transcript.md`, one block per step with the template headings unchanged, then the `## Final tasks` block with the feel-obvious answer.
- Observations (`kind: check` per step, re-ask, lagged recall and explain-why; `kind: final` for the two final tasks) and misconception records and updates, through the CLI only.
- A prerequisite landmark added to `plan.md` when step 4 requires it.
