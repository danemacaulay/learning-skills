---
name: learn-record
description: Use when a session's teaching is finished or paused and its transcript has not been written to the store, or when show lists a session as not yet recorded
---

# learn-record

Turns a session's transcript and plan into verified graph records and links the session's observations to them, so they can come due for review. Shared rules live in [theory](../_learn/theory.md); the store, CLI fields and the `extraction.md` template live in [store](../_learn/store.md). Read both before starting.

## When to use

- `learn-teach` has handed off, at the end or on a pause: `.learn/sessions/<id>/transcript.md` has judged steps.
- `learn.py show` lists the session under "Not yet recorded" (for example, `learn-review` hands off here after its sitting).
- A session recorded once was resumed and taught further.
- Not for teaching (`learn-teach`) or review sittings (`learn-review`). Do not teach new material while recording.

## Reads

- `.learn/sessions/<id>/transcript.md`, `plan.md` (Sources, Map, Landmarks table) and `extraction.md` if an earlier run wrote one.
- `learn.py observations --session <id>`: every question asked in the session, with its slug, `prompt` and `kind`.
- `learn.py state`: this session's slugs appear as `<id>/<slug>` with status `unlinked` (never linked) or `closed` (closed by an earlier run).
- The store via the CLI only. Call it as `python3 <skills-dir>/_learn/scripts/learn.py`; below, `learn.py <subcommand>`. Global flags (`--root`, `--now`) go before the subcommand.

## Procedure

1. Start a run. If `extraction.md` exists, leave its earlier sections as they are and append a new `# Run <timestamp>` section with the template's headings; never rewrite an earlier section. Run `learn.py state` and list the slugs to settle: every `<id>/<slug>` key with status `unlinked`, plus any `closed` one whose landmark now has a `## Step:` in the transcript.
2. Propose, going through the plan's landmark table row by row. Look up each row's `## Step:` in the transcript:
   - Taught (the step has an `Explanation:` and a `Judgement:`, whether its check took or missed): propose one node. A step with an `Explanation:` but no `Judgement:` was paused before its check was answered; treat it as not reached yet, since `learn-teach` redoes it on resume. Its statement comes from the tutor's `Explanation:` and `Repair:` lines, cross-checked against the plan's claim column.
   - Held and passed cold (`Explanation: none: held, passed cold`): propose one node from the plan's claim column, or reuse the `n-` id the row names.
   - No step yet (the session was paused before it): no node this run; step 7 closes its slugs.

   Then propose chains from the map's edges: for each landmark with incoming edges, one chain whose premises are the nodes of the landmarks that feed it and whose conclusion is its node. A proposal is not a write. Every node and chain still goes through steps 3–6; a chain that does not survive (its premises are not jointly needed, or the learner's restatement shows it does not hold) is dropped with the reason noted. Learner answers are never a source of graph content: a learner's wrong or right answer says what they hold, not what is true. Write the proposals under `## Proposed nodes and chains`, each with its slug and where its statement came from.
3. Make each node atomic: one claim per node. Anything containing a "because" becomes premises plus a chain; the CLI rejects a statement containing " because ", " therefore ", " hence " or " which means ". All premises of a chain are jointly needed to reach its conclusion; two routes to one conclusion are two chains, not one chain with alternative premises.
4. Verify each claim, held ones included, against the sources in `plan.md`, in a pass separate from extraction and before writing anything ([theory](../_learn/theory.md#T10), theory.md#T10). Record each result under `## Verification`. Set `status`: `source-verified` (with `source`, which must name the text and locus), `tutor-asserted` (no source checked; this is the default when the plan says "Unverified"), or `contested` (sources disagree, or the claim is one reading among several). Set `claimType`; an `interpretation` carries its `scope` (according to which text or reading), and an `attribution` always carries a `source`; for a `tutor-asserted` attribution, put the attributed text and locus as claimed, noted as unchecked (for example "Heidegger, Being and Time, section 15 (as claimed by the tutor, not checked)"). A claim a source contradicts is not written as a node: correct it in the proposal and tell the learner in step 6.
5. For each proposed node run `learn.py candidates --statement "<the statement>"`, and look up each returned id in `learn.py graph` to read its statement before deciding. A returned node is the same claim when one check would test both, whatever the wording; a narrower, broader or different-case claim is a new node. Decide link (use the returned `n-` id) or create. Write the candidates, the decision and a one-line reason under `## Link decisions`, in the template's format. Never create a near-duplicate of a returned candidate; if the existing node is wrong, that is step 9.
6. Show the learner the proposed nodes and chains and which plan slugs will be linked to them. Ask them to restate or correct each chain's premises, in their own words, one chain at a time. Record what they contest under `## Learner review`. Then either change the proposal or mark the node `contested`; do not drop the disagreement silently, and do not accept "ok" as a restatement. If a correction changes a claim, re-run steps 4 and 5 on it before writing.
7. Write with `node`, then `chain`, then `link`, in that order, because each needs the ids the previous one prints. Settle every slug listed in step 1:
   - A `## Step:` slug links to its landmark's node plus the chain that concludes at that node, when one exists.
   - A grounding probe slug that is not a landmark slug: read its questions with `learn.py observations --session <id> --target <slug>` and link it to the node whose claim they tested.
   - The slug that carries the final-task observations (the sink) links to the sink node and its chain.
   - A slug that has no node (a strand probed but never taught, a landmark not reached yet, a dropped or source-contradicted claim) is closed: `learn.py link --session <id> --slug <slug> --none --reason "<why>"`.

   Observations count toward exactly the ids in the link.

   ```
   python3 <skills-dir>/_learn/scripts/learn.py node --json '{"name":"ready-to-hand","statement":"Equipment is encountered first through use, not through observation","claimType":"attribution","status":"source-verified","source":"Heidegger, Being and Time, section 15","scope":null,"session":"20261109-heidegger"}'
   python3 <skills-dir>/_learn/scripts/learn.py node --json '{"name":"breakdown-reveals-object","statement":"A broken tool becomes conspicuous as an object of observation","claimType":"interpretation","status":"tutor-asserted","source":null,"scope":"according to the lecture reading of Being and Time, section 16","session":"20261109-heidegger"}'
   ```

   Each prints the stored line with its `n-` id (below, `n-4ef8ad36` is the first node and `n-4f60bcde` the second; in a real run, use the ids printed). Use those ids as premises and conclusion; both must be node ids:

   ```
   python3 <skills-dir>/_learn/scripts/learn.py chain --json '{"premises":["n-4ef8ad36"],"conclusion":"n-4f60bcde","session":"20261109-heidegger"}'
   ```

   `targets` takes node and chain ids, comma separated: here the node, and the chain just printed that concludes at it. The last line closes a probe slug that has no node:

   ```
   python3 <skills-dir>/_learn/scripts/learn.py link --session 20261109-heidegger --slug breakdown --targets n-4f60bcde,c-7740e6a0
   python3 <skills-dir>/_learn/scripts/learn.py link --session 20261109-heidegger --slug cartesian-subject --none --reason "probed strand, not taught this session"
   ```

   A later `link` with `--targets` reopens a closed slug.
8. Point misconceptions at their nodes. For each `refute m-…` or `discriminate m-…` landmark written in this run, run `learn.py misconceptions`, take that record, add the landmark's node id to `contradicts`, and resubmit the whole record with the same `id`. `learn-review` resolves the misconception by a later pass on those ids.
9. If the session exposed an error in an existing node, write a `supersede` or `retract` edit with the reason; never rewrite or delete a line. Use `supersede` when a corrected node (written in step 7) replaces it, `retract` when the claim should simply leave the graph. Rival readings, each a node of its own, get a `contradicts` edit, never a silent overwrite.

   ```
   python3 <skills-dir>/_learn/scripts/learn.py edit --json '{"op":"supersede","target":"n-7a1c9e02","by":"n-4ef8ad36","reason":"The earlier node said observation comes first; the corrected node says use does","session":"20261109-heidegger"}'
   python3 <skills-dir>/_learn/scripts/learn.py edit --json '{"op":"retract","target":"n-7a1c9e02","reason":"No source supports this claim and the lecture contradicts it","session":"20261109-heidegger"}'
   python3 <skills-dir>/_learn/scripts/learn.py edit --json '{"op":"contradicts","a":"n-4f60bcde","b":"n-b2d5e6f1","reason":"Two readings of section 16 (breakdown as revealing objects vs. as revealing the world) that cannot both hold","session":"20261109-heidegger"}'
   ```
10. Fill `## Written` with the ids, the links, each closed slug with its reason, and each landmark that produced nothing with why, and tell the learner about any landmark that produced nothing. Run `learn.py show` and confirm "Not yet recorded" no longer lists the session; if it does, a slug from step 1 is still unsettled. For a linked node or chain, read the next review date with `learn.py state --target <id>` (`due_at`) and tell the learner that date. Then hand off: the next sitting is `learn-review`. Do not start it now and do not offer it in this sitting, even when the date you read is already past: the learner has just restated these claims, so a review now would not be a cold retrieval. Tell the learner it is for a later sitting, and give the date.

## Hard rules

- Every taught or held landmark is proposed as a node, and every map edge as a chain; each survives only through atomicity, verification and the learner's restatement.
- Every claim carries its status; unsourced material is `tutor-asserted`, never `source-verified` (theory.md#T10).
- Verification is a separate pass from extraction, and it comes before any write.
- Learner answers, wrong ideas and learner state never go into `graph/`; misconceptions stay in `learner/`.
- One claim per node; a "because" is premises plus a chain.
- Every slug with observations ends the run linked or closed with a reason.
- Append only: correct with `supersede`, `retract` or `contradicts`, never by editing a line. A later run appends to `extraction.md`.
- Do not edit `transcript.md`, `plan.md` or `grounding.md`.

## Writes

- `.learn/sessions/<id>/extraction.md`: one `# Run` section per run, with the template headings unchanged.
- Graph lines (`nodes.jsonl`, `chains.jsonl`, and `edits.jsonl` when step 9 applies), one `links.jsonl` line per settled slug, and `contradicts` updates to misconceptions (step 8), through the CLI only.
