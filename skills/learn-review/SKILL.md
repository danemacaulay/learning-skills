---
name: learn-review
description: Use when the learner wants to review or practise earlier material, or starts a sitting without a new topic and learn.py due returns items
---

# learn-review

Runs a delayed, spaced retrieval sitting over what earlier sessions taught. You tutor in chat and log each question. Shared rules live in [theory](../_learn/theory.md); the store, CLI fields and the `review.md` template live in [store](../_learn/store.md). Read both before starting.

## When to use

- The learner asks to review or practise earlier material.
- A sitting starts without a new topic and `learn.py due` returns items. A learner who brings a new topic goes to `learn-ground` first; its step 4 probes the due items on that topic and tells them the rest of the review is waiting.
- Not for new material. Grounding a new topic is `learn-ground`, teaching is `learn-teach`, recording is `learn-record`.

## Reads

- The store via the CLI only. Call it as `python3 <skills-dir>/_learn/scripts/learn.py`; below, `learn.py <subcommand>`. Global flags (`--root`, `--now`) go before the subcommand.
- `learn.py due --limit 8` for the queue, `learn.py graph` for the content of each target (active nodes, and chains with their premises and conclusion), `learn.py misconceptions` for recorded wrong ideas, `learn.py state` for each target's `status`, `events` and `due_at`, and `learn.py observations --target <id>` for the questions already asked on a target. You read these; the learner does not see them before answering.
- Observations in this sitting use `session` = `<YYYYMMDD>-review` (for example `20261116-review`). Its directory `.learn/sessions/<YYYYMMDD>-review/` holds only `review.md`, the pre-commitment file.

## Procedure

1. Run `learn.py due --limit 8` (at most 8 targets; the cap is a design default, not a research finding). If it returns `[]`, run `learn.py state`, take the smallest `due_at` among targets that have one (status `taught`, `retained` or `lapsed`), tell the learner that date, log nothing, and go to step 8. If it returns targets, create `.learn/sessions/<YYYYMMDD>-review/` if needed and append to its `review.md` a `# Review <timestamp>` section whose `## Before` holds the output of `learn.py state` unchanged (the before-snapshot for step 7). Show no transcript or statement beforehand: the learner sees only the questions.
2. Per target, look up its content in `learn.py graph` and choose a form ([theory](../_learn/theory.md#T9), theory.md#T9). `learn.py state --target <id>` gives its `status`: `taught` means this is its first review, `retained` or `lapsed` a later one. A chain gets `reconstruct` on its first review ("Without looking, why does C hold? Give the premises and how they combine"), then on later visits `apply` to a new case or `counterfactual` ("If this premise were false, what happens to the conclusion?"). Two easily confused nodes from different sessions get `discriminate` ("When does each idea apply?"). A bare node target gets `apply` to a new case, or `discriminate` when `learn.py graph` shows a confusable node from another session. Check `learn.py observations --target <id>` (it lists the earlier review questions on that id) so you do not repeat one. Never cloze, never verbatim recall of a statement.
3. Before asking, append the question's block to `review.md`: `## Q<n>: <target id>`, `Prompt:`, `Expected:` and `Wrong models:` ([theory](../_learn/theory.md#T4), theory.md#T4). For a chain, `Expected:` lists its premises and the linking inference as scoring points; for `apply` or `counterfactual`, the answer each premise set implies. `Wrong models:` names the likely wrong answers, including any recorded misconception whose `contradicts` lists this target. Write the block before the question is sent and never quote it in a message, so the judgement cannot drift toward the learner's answer.
4. Ask the question and ask confidence (low / med / high) in ONE message, then stop until the learner answers ([theory](../_learn/theory.md#T5), theory.md#T5). Judge `took` only if every premise and the link are produced; otherwise `missed`. "I don't know" is `dont_know`: log it as such and handle it like a miss. Agreement without content is a miss with `produced: false`. Judge before composing any reply, then log with `observe` (`kind: review`), copying the answer verbatim into `response`; `target` is the chain or node id. Write the printed `o-` id as `Observation:` under the question's block in `review.md`.

   ```
   python3 <skills-dir>/_learn/scripts/learn.py observe --json '{"session":"20261116-review","kind":"review","form":"reconstruct","target":{"type":"chain","id":"c-679b5833"},"prompt":"Without looking, why does a broken tool become conspicuous as an object? Give the premises and how they combine.","expected":"Premise: equipment is encountered first through use. Link: when use fails, the thing can only show up as an object we notice.","response":"We mostly use it without noticing, so once it breaks we notice it as a thing","confidence":"med","grade":"took","produced":true}'
   ```
5. Give task-level feedback on every miss and on every correct answer given at low confidence ([theory](../_learn/theory.md#T6), theory.md#T6): what the answer skipped or rested on, what the chain assumes and predicts. On a miss, re-teach that chain briefly from its premises, then continue with the other targets. After them, re-ask the missed target once more in the same sitting, in a different wording (its own block in `review.md` first), and log it as its own `observe` with `hinted: true`, because the re-teaching is a hint. A hinted answer never counts toward `retained` ([theory](../_learn/theory.md#T8), theory.md#T8).

   ```
   python3 <skills-dir>/_learn/scripts/learn.py observe --json '{"session":"20261116-review","kind":"review","form":"reconstruct","target":{"type":"chain","id":"c-679b5833"},"prompt":"Put it in your own words again: what has to be true of a tool before it breaks for it to become conspicuous?","expected":"Premise: equipment is encountered first through use. Link: when use fails, the thing can only show up as an object we notice.","response":"It has to be in use first, unnoticed, then breaking makes it stand out","confidence":"high","grade":"took","produced":true,"hinted":true}'
   ```
6. Misconceptions ([theory](../_learn/theory.md#T7), theory.md#T7). Read the current records with `learn.py misconceptions`.
   - A miss shows a recorded misconception: put its `m-` id in the observation's `misconception` field when logging in step 4. Then add the `o-` id to `evidence`, set `status` `confirmed` (from `suspected` this is the second independent observation; from `addressed` or `resolved` it has shown again), and update `stability` if it showed in a changed form (`shifting`).
   - A miss reveals a new wrong idea: log the observation first, with no `misconception` field, then record the idea with `learn.py misconception` as `suspected`, `one-off`, with that `o-` id as its one evidence id.
   - An unhinted pass (`took`, produced, `hinted` false) on a target listed in the `contradicts` of an `addressed` misconception, or on a chain whose conclusion is listed there: set it `resolved` and add the pass's `o-` id to `evidence`. A review is always a later sitting than the teaching that addressed it.

   To update, take the record from `learn.py misconceptions`, change those fields, and resubmit the whole record with the same `id` (every status except `suspected` needs two distinct evidence ids).

   ```
   python3 <skills-dir>/_learn/scripts/learn.py misconception --json '{"id":"m-1a2b3c4d","statement":"A tool is first an object with properties","counterpart":"Equipment is encountered through use","contradicts":["n-4f60bcde"],"evidence":["o-16a30b1a","o-f510948e","o-9c0d1e2f"],"stability":"stable","kind":"category-error","status":"confirmed","session":"20261116-review"}'
   ```
7. Run `learn.py state` again and compare with the before-snapshot. Tell the learner which targets changed `status` (moved to retained, lapsed) and the next due date, the smallest `due_at` among targets that have one, in task terms. Then run `learn.py show` for the learner-facing summary (misconceptions, calibration). State no score. No new material in a review sitting: if the learner asks for it, offer `learn-ground` for another session.
8. Only after the review, look for unrecorded sessions. If `learn.py show` lists a session under "Not yet recorded", tell the learner its material is not reviewable until it is recorded. Then hand off: stop following this skill, open [`learn-record/SKILL.md`](../learn-record/SKILL.md) now for that session and follow it from its first step before sending the learner anything else. Nothing recorded in this sitting is reviewed in this sitting.

## Hard rules

- Review chains by reconstruction, application or dropping a premise; never cloze or verbatim recall; never teach new material (theory.md#T9).
- Write the expected answer in `review.md` before the question is sent, never show it, and judge before responding (theory.md#T4).
- Ask confidence on every question, before any feedback (theory.md#T5).
- Only an unhinted, produced answer after a delay counts as retained; never write a status by hand (theory.md#T8).
- At most 8 targets per sitting; the learner never sees a target's content before answering.
- Review what is already due first; record an unrecorded session only afterwards, and never review it in the same sitting.

## Writes

- One `review` observation per question asked, including each hinted re-ask, through `observe`.
- `misconception` lines (new `suspected`, or an updated record with the same `id`) through the CLI only.
- `.learn/sessions/<YYYYMMDD>-review/review.md`: the before-snapshot and one block per question.
- Nothing in `graph/`.
