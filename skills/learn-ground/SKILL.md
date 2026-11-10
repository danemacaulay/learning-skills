---
name: learn-ground
description: Use when someone wants to learn or understand a topic and no grounding exists yet for this session's goal
---

# learn-ground

Sets the goal and finds where teaching should start. You probe; you do not teach. Shared rules live in [theory](../_learn/theory.md); the store, CLI fields and the `grounding.md` and `probe.md` templates live in [store](../_learn/store.md). Read both before starting.

## When to use

- The learner names a topic to learn or understand and `.learn/sessions/<id>/grounding.md` does not exist for this goal.
- A learner who arrives with a new topic starts here even when reviews are due; step 4 deals with them.
- Not for reviewing earlier material (`learn-review`) or teaching (`learn-teach`).

## Reads

- `.learn/` via the CLI only. Call it as `python3 <skills-dir>/_learn/scripts/learn.py`; below, `learn.py <subcommand>`. Global flags (`--root`, `--now`) go before the subcommand.
- The `show` output (learner model); `learn.py candidates` and `learn.py graph` for node and chain ids relevant to this goal; `learn.py misconceptions` for wrong ideas already on record.

## Procedure

1. If there is no `.learn/`, run `learn.py init` (safe to repeat). Create the session folder `.learn/sessions/YYYYMMDD-<topic>`; its name is the `session` value in every record. Run `learn.py show` and read it, so you know what the learner already has on record.
2. Ask until the goal is specific ("learn Heidegger" is not; "explain ready-to-hand versus present-at-hand and say what a Cartesian view gets wrong" is). Then write 2-4 success criteria as unaided performances: explain X in their own words; apply it to a new case; say what a named rival view gets wrong. Show them and have the learner confirm or change them. Ask once whether the goal "feels obvious" to them and note the answer; it is not evidence ([theory](../_learn/theory.md#T1), theory.md#T1).
3. Say the purpose and the budget out loud: this finds where to start teaching; expect about 12–20 questions in all; wrong answers are the point, not a failure; the learner can stop at any strand boundary. Give the warning once, in your words: attempting first and recalling later feel harder and slower than being told, that difficulty is the mechanism, and none of this method has been tested in this setting ([theory](../_learn/theory.md#T12), theory.md#T12).
4. Find store ids that bear on this goal: run `learn.py candidates --statement "<the goal>"` and once per success criterion, and read each hit in `learn.py graph` (add any chain whose premises or conclusion is a hit). Then run `learn.py due --prefer <those ids, comma separated>`. `--prefer` only orders the queue; it does not filter. Cold-probe only the returned items whose id is in your list: one question each, free response, no recap beforehand, logged as `kind: probe` with `target` type `node` or `chain` and that id (example in step 7). If other items came back, tell the learner once that a review is waiting and that `learn-review` can run after this session or another time. Do not probe them and do not count them in the budget.

   ```
   python3 <skills-dir>/_learn/scripts/learn.py candidates --statement "tools are encountered through use"
   python3 <skills-dir>/_learn/scripts/learn.py due --prefer n-4ef8ad36,c-679b5833
   ```
5. Split the goal into strands (a few themes the criteria need). Let the learner choose the order. Within a strand ask one question at a time, each chosen from the last answer. Enter above the expected floor; after a confident correct answer make a large jump up, after a miss step down. Give no teaching and no feedback during the probe; say once that feedback comes in teaching.
6. Before sending each question, append its block to `.learn/sessions/<id>/probe.md` (template in [store](../_learn/store.md)): `## Q<n>: <slug>`, `Prompt:`, `Expected:` (the answer you will judge against) and `Wrong models:` (each likely wrong answer, or for a multiple-choice question which option embodies which named wrong idea). Write it before the question is sent and never quote it in a message ([theory](../_learn/theory.md#T4), theory.md#T4). Every question asks for confidence (low / med / high) before you respond ([theory](../_learn/theory.md#T5), theory.md#T5); if declined, record `not_given`. A multiple-choice question also asks for a one-line reason. Judge against `Expected:`, not against the learner's wording.
7. Log every answer with `learn.py observe` immediately, before the next question. `kind` is `probe`; `produced` is false for option picks and true when the learner generated the answer; `grade` is `took`, `missed` or `dont_know`. The call prints the new `o-` id: write it as `Observation: o-…` under that question in `probe.md`. For a not-yet-linked topic the target is a slug: name it for the claim the question tests, and reuse the same slug for every question on that claim (`learn-plan` reuses these slugs for its landmarks):

   ```
   python3 <skills-dir>/_learn/scripts/learn.py observe --json '{"session":"20261109-heidegger","kind":"probe","form":"free","target":{"type":"slug","id":"ready-to-hand"},"prompt":"What happens to a hammer for the carpenter mid-task?","expected":"It is used, not noticed as an object","response":"she looks at it to check it is a good hammer","confidence":"high","grade":"missed","produced":true}'
   ```

   For a prior item use `"target":{"type":"node","id":"n-4ef8ad36"}` (or `chain`/`c-`). For a multiple-choice pick, `"form":"mc"`, `"produced":false`, and put the reason after the option in `response`.
8. A strand is finished when any of these holds: it holds at the level the goal needs; floor and ceiling are adjacent questions; two consecutive questions moved neither edge; or 5 questions are spent (budget 3–5 per strand; a design default, not a research finding). A floor needs at least one produced answer; a floor resting only on option picks is `recognised-only`.
9. Effort drop. The first bare option pick (no reason, no confidence) is logged as usual. If the next answer is also a bare pick, log it with `"lowEffort":true`, and do the same for every further bare pick in a row; the first one stays as logged. Then switch to one free-response question. If that answer is also minimal (a word or two, no reasoning), log it with `"lowEffort":true`, stop probing and go to step 12 with stop reason `effort-drop`.
10. On a wrong answer that suggests a specific wrong idea (not a blank and not a slip), ask one follow-up. It must be a different question that the suspected idea would also get wrong. "Say more about why" is an elaboration of the same answer, not a second observation. Write its `probe.md` block first, with the suspected idea among the wrong models, ask confidence, and log it with `observe`. Then record the idea with `learn.py misconception`, in the learner's words ([theory](../_learn/theory.md#T7), theory.md#T7):
    - The follow-up is wrong in the way the idea predicts: `status` `confirmed`, `evidence` both `o-` ids; `stability` `stable` if the idea showed the same way both times, `shifting` if it changed form.
    - The follow-up is answered correctly: `status` `suspected`, `stability` `one-off`, `evidence` the first `o-` id.
    - If `learn.py misconceptions` already lists this idea from an earlier session, update that record instead: pass its `id` with the whole record, add the new `o-` ids to `evidence`, and set `status` `confirmed`.

    Omit `id` for a new misconception; the CLI assigns the `m-` id and prints it.

    ```
    python3 <skills-dir>/_learn/scripts/learn.py misconception --json '{"session":"20261109-heidegger","statement":"A tool is first an object whose properties you inspect","counterpart":"Equipment is encountered first through use","contradicts":[],"evidence":["o-16a30b1a","o-f510948e"],"stability":"stable","kind":"category-error","status":"confirmed"}'
    ```

    (`contradicts` is `[]` when no graph node exists yet.)
11. At each strand boundary offer "stop and plan from here" next to "next strand". Partial grounding is a valid end: mark unprobed strands `not-probed`. The learner owns when to stop ([theory](../_learn/theory.md#T11), theory.md#T11).
12. Write `.learn/sessions/<id>/grounding.md` using the template in [store](../_learn/store.md) with headings unchanged. Say what you found in two or three sentences (floors, ceilings, wrong ideas found). Then hand off: stop following this skill, open [`learn-plan/SKILL.md`](../learn-plan/SKILL.md) now and follow it from its first step before sending the learner anything else.

## Hard rules

- Success criteria are unaided performances, confirmed by the learner; felt obviousness never ends the grounding (theory.md#T1).
- `Expected:` and `Wrong models:` are in `probe.md` before each question is sent, and never shown to the learner (theory.md#T4).
- Confidence is asked on every question, before any feedback, and stored beside the grade, never instead of it (theory.md#T5).
- A wrong idea is `confirmed` only when a different follow-up question shows it a second time; otherwise it is `suspected`. Never refute it during grounding (theory.md#T7).
- Say the "this will feel harder, untested here" warning once, at the start (theory.md#T12).
- No teaching, hints or feedback while probing; do not supply an answer the learner could produce. A hint is not allowed, so `hinted` stays false.
- Never write `taught` or `retained`; the CLI derives them. Store no scores or percentages.

## Writes

- `observations.jsonl`: one `probe` line per answer, via `observe`.
- `misconceptions.jsonl`: `suspected` or `confirmed` lines, via `misconception`.
- `.learn/sessions/<id>/probe.md`: one pre-commitment block per question.
- `.learn/sessions/<id>/grounding.md`: goal, 2-4 success criteria, per-strand status/floor/ceiling/floor quality/evidence ids, misconceptions, session conditions (questions asked, stop reason `complete | budget | learner-request | effort-drop`, strands not probed).
- Does not touch `graph/` or `links.jsonl`.
