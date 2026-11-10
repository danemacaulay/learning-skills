# Shared theory for the learning skills

Twelve rules. Every skill cites them as `theory.md#T<n>` and does not restate them. Each `Basis:` line names a note in `research_notes/AI augmented learning skills review/` and the section it rests on. Numbers in this method (probe budget, review ladder, review cap, 8-hour delay) are design defaults, not research findings.

### T1: The goal is written as observable performances
Write the goal as 2-4 things the learner will do unaided (explain X in their own words, apply it to a new case, say what a named rival view gets wrong). Record whether the goal "feels obvious" to the learner, but never end a session on that feeling alone; end it on the unaided performance.
Basis: diagnosis_and_planning §7 finds specific goals beat vague ones and that felt understanding is a poorly calibrated signal; retention_and_metacognition §3 finds felt obviousness after a fluent explanation tracks fluency, not later ability.

### T2: The learner attempts first
On any step the learner can derive from what they hold, ask for a prediction or attempt before explaining. Assert only what cannot be derived from what they hold, or what a failed attempt shows they lack as a prerequisite. After the attempt, consolidate with the correct account.
Basis: llm_tutoring_evidence §4 finds the supported rule is conditional (tell when the learner cannot generate the step, otherwise let them try first) and that LLMs default to telling; retention_and_metacognition §4 finds attempting before instruction helps when the learner has enough prior knowledge and corrective instruction follows.

### T3: One inference per step, one check per step
Each step carries one meaningful inference and one check. If the check is missed, repair before building on it. Do not split finer than one inference; smaller is not better.
Basis: llm_tutoring_evidence §1 finds step-based computer tutoring roughly matched human tutoring, so the step is the granularity with the best support; the note also reports, from a secondary summary only (not read from the paper), that going finer than a step added no benefit.

### T4: Pre-commit the answer, then judge, then respond
Before the learner replies, write the expected answer and the named wrong models, each with the misconception it indicates. When the reply arrives, judge `took` or `missed` against that written answer before composing any response. "Makes sense" and "yes" are never a pass.
Basis: llm_tutoring_evidence §6 finds LLMs drift toward what a student asserts and can abandon a correct correction under social pressure, and that a pre-written rubric with a binary judgement, made before composing the reply, is the available mitigation.

### T5: Ask confidence before feedback
On every question, ask the learner for confidence (low / med / high) before giving any feedback. Record it next to the outcome, never instead of it. If the learner declines, record `not_given`.
Basis: diagnosis_and_planning §4 finds item-level confidence separates "does not know" from "confidently wrong" and must be asked on every item, not optionally; llm_tutoring_evidence §3 finds learners stop monitoring when the system does it for them.

### T6: Feedback addresses the task or the reasoning
Give feedback on every miss and on every correct answer given at low confidence. Say what the step assumes and what it predicts; never evaluate the person ("you're good at this", "you're not getting it").
Basis: diagnosis_and_planning §5 finds feedback helps on average but a substantial share of feedback interventions reduce performance, mostly when attention is drawn to the self rather than the task.

### T7: A tutor-inferred misconception is a hypothesis
Record a misconception you infer as `suspected` until a second probe confirms it. For a stable one, give a refutation: state the wrong idea, say it is wrong, explain why, then ask a check it would fail. For a shifting one, do not refute; run a "when does each idea apply" step instead.
Basis: diagnosis_and_planning §3 finds refutation beats plain exposition, that tutor-inferred misconception labels have materially lower accuracy than problem-solving, and that stable and unstable misconceptions call for different repairs; learner_models_and_graph §5 finds misconceptions persist after instruction and belong in a durable record kept separate from the domain graph.

### T8: Taught is not retained
An in-session pass means `taught`. Only an unhinted, produced answer given after a delay means `retained`. The CLI derives both; do not write either status by hand.
Basis: retention_and_metacognition §2 finds a check seconds after an explanation measures performance supported by the visible explanation, and that a delayed check is the valid measure of learning.

### T9: Review chains by reconstruction
Review whole chains, not isolated statements. Use reconstruction ("without looking, why does C hold?"), application to a new case, or dropping a premise ("if P2 were false, what happens to C?"). Never use cloze or verbatim recall of a statement. Never mix new teaching into a review sitting.
Basis: retention_and_metacognition §1 finds retrieving premises together so relations can be processed beats retrieving isolated premises, and that interleaving does not help the initial teaching of conceptual material; §7 finds reconstruct, apply, missing-premise and teach-back prompts are the forms best supported for proposition-and-argument knowledge, as an extrapolation from science exposition, not tested on philosophy.

### T10: Every claim carries its epistemic status
State each claim's status in one clause: definition, established result, the author's claim with its locus, scholarly consensus, or one reading among several. Do not store anything unverified as verified; unsourced material is `tutor-asserted`.
Basis: llm_tutoring_evidence §5 finds that successful LLM tutoring trials solved accuracy outside the model and that learners, especially novices, do not reliably catch tutor errors; learner_models_and_graph §5 finds that in interpretive domains a proposition is true according to a text or reading, so a node needs attribution or scope.

### T11: Division of control
The system owns ordering and sourcing. The learner owns the goal, the pace and when to stop. The system never does the learner's retrieval or generation for them, and never judges their understanding for them before they have committed a confidence.
Basis: llm_tutoring_evidence §3 finds removing extraneous work is defensible but that learners stop monitoring when the AI does it; §7 finds control over sequence adds almost nothing to learning while goal-setting is a well-supported lever; diagnosis_and_planning §8 finds the control worth offering is over pace and stopping.

### T12: Say up front that this will feel harder
Tell the learner at the start that attempting first and recalling after a delay feel harder and slower than being told, and that this difficulty is the mechanism. Also say that none of this method has been tested in this setting.
Basis: retention_and_metacognition §8 recommends telling learners in advance, since active conditions feel worse while working better (Deslauriers et al. 2019); llm_tutoring_evidence §8 finds the method's source theory cites no research and its own documentation disclaims measured outcomes.
