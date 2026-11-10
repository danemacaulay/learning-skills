# Retention and Metacognition: what the durable-learning literature says about a teach-once, "feels obviously true" LLM tutoring harness

Scope: evaluation of the `learning` repo (skills `learning-ground → learning-plan → learning-teach → learning-graph`) against the literature on retrieval practice, spacing, interleaving, desirable difficulties, and metacognitive illusions. Notes compiled 2026-11-09.

**Verification legend.** Every DOI below was resolved against the Crossref registry in this session (authors, year, title, venue, pages confirmed) unless a non-DOI URL is given. Provenance of each *number* is tagged:
- **[P]** read in the primary text or its supplement this session
- **[A]** from the paper's abstract / PubMed record as returned by search this session
- **[S]** from a secondary source this session (press release, review, blog); primary not opened
- **[R]** recalled from the paper's abstract; bibliographic record verified but the number was **not** re-read this session. Treat as "check before quoting".

---

## 1. Retrieval practice, spacing, interleaving, successive relearning: effect sizes, transfer to conceptual material, and the cost of teaching once

### Takeaway
Retrieval practice (g ≈ 0.5–0.6 vs. restudy), spacing, and their combination (successive relearning) are the two best-supported techniques in the field, and the benefits extend to inference and application questions (transfer d ≈ 0.40), though more weakly and with real boundary conditions. A system that explains once, checks seconds later, and never revisits is optimising the one condition (immediate performance after fluent exposure) that the literature shows is least predictive of what is retained a week later.

### Cited Findings

**Retrieval practice / testing effect**
- Roediger & Karpicke (2006), *Psychological Science* 17(3), 249–255. Prose passages. On a 5-minute test repeated study beat repeated testing; at one week the order reversed: STTT 61%, SSST 56%, SSSS 40% recall [S, WashU release]. Repeated study produced higher confidence despite worse delayed retention [R]. — [DOI 10.1111/j.1467-9280.2006.01693.x](https://doi.org/10.1111/j.1467-9280.2006.01693.x); numbers: [WashU Source](https://source.washu.edu/?p=55770)
- Karpicke & Roediger (2008), *Science* 319, 966–968. Repeated retrieval (not repeated study) drove one-week retention, roughly 80% vs. ~35% [R]; learners' own predictions did not distinguish the conditions [R]. — [DOI 10.1126/science.1152408](https://doi.org/10.1126/science.1152408)
- Karpicke & Blunt (2011), *Science* 331, 772–775. Science texts; final test one week later with verbatim **and inference** short-answer questions. Retrieval practice beat elaborative concept mapping, d = 1.50 (Exp. 1) [P]; Exp. 2, d = 1.07 on short-answer (M = .73 vs .54) and d = 1.01 even when the final test was itself building a concept map (M = .44 vs .28) [P]. Judgments of learning were highest in the *repeated study* condition (M = .79) [P], i.e. learners' metacognition ran opposite to outcomes. — [DOI 10.1126/science.1199327](https://doi.org/10.1126/science.1199327); [Supporting Online Material](https://learninglab.psych.purdue.edu/downloads/2011/2011_Karpicke_Blunt_ScienceSupportingMaterial.pdf)
- Rowland (2014), *Psychological Bulletin* 140(6), 1432–1463. Meta-analysis of testing vs. restudy: g = 0.50 (159 effect sizes, 61 studies) [S]; larger at retention intervals ≥ 1 day (g = 0.69) than same-day (g = 0.41) [S]. — [DOI 10.1037/a0037559](https://doi.org/10.1037/a0037559); [PubMed](https://pubmed.ncbi.nlm.nih.gov/25150680/)
- Adesope, Trevisan & Sundararajan (2017), *Review of Educational Research* 87(3), 659–701. 272 effect sizes; overall g = 0.61 for practice testing vs. all comparison conditions [S]. **Conflict:** one later review cites this meta-analysis as g = 0.70; I could not open the full text to settle which headline figure is correct. — [DOI 10.3102/0034654316689306](https://doi.org/10.3102/0034654316689306); [Learning Scientists summary](https://www.learningscientists.org/blog/2017/2/9-1)
- Yang, Luo, Vadillo, Yu & Shanks (2021), *Psychological Bulletin* 147(4), 399–435. Classroom quizzing: g = 0.499, 222 independent studies, 48,478 students [A]. — [DOI 10.1037/bul0000309](https://doi.org/10.1037/bul0000309)
- Agarwal, Nunes & Blunt (2021), *Educational Psychology Review* 33, 1409–1453. Systematic review of applied school/classroom research; title-level conclusion "retrieval practice consistently benefits student learning"; a majority of effects medium or large [R]. — [DOI 10.1007/s10648-021-09595-9](https://doi.org/10.1007/s10648-021-09595-9)

**Does it transfer to inference / conceptual understanding?**
- Pan & Rickard (2018), *Psychological Bulletin* 144(7), 710–756. Meta-analysis of *transfer* of test-enhanced learning: overall d ≈ 0.40 across 192 effect sizes [S]. Transfer is strongest across test formats and to application and inference questions; weakest to *untested* material seen during initial study and to rearranged stimulus–response items; moderators that produce transfer are response congruency, elaborated retrieval practice, and high initial test performance [R, abstract]. — [DOI 10.1037/bul0000151](https://doi.org/10.1037/bul0000151); [author manuscript](https://sc-pan.github.io/pdf/PR_2018W.pdf)
- Butler (2010), *JEP: Learning, Memory, and Cognition* 36(5), 1118–1133. Repeated testing produced better transfer than repeated studying, including to new inferential questions in different knowledge domains (title-level claim; details [R]). — [DOI 10.1037/a0019902](https://doi.org/10.1037/a0019902)
- **Boundary condition / dispute.** van Gog & Sweller (2015), *Educational Psychology Review* 27, 247–264, argue the testing effect "decreases or even disappears as the complexity of learning materials increases" (high element interactivity, worked examples). Karpicke & Aue (2015), same issue, 317–326, reply that element interactivity is not quantitatively defined and that the cited data still show a small positive effect. — [DOI 10.1007/s10648-015-9310-x](https://doi.org/10.1007/s10648-015-9310-x); [DOI 10.1007/s10648-015-9309-3](https://doi.org/10.1007/s10648-015-9309-3)
- **Null result and its repair.** Tran, Rohrer & Pashler (2015) found retrieval practice improved memory for premises but not deductive inferences from them; Eglington & Kang (*Educational Psychology Review* 30, 215–228) showed the benefit to deductive inference appears when the related premises are presented *together* so relational processing is possible (fill-in-blank in Exps 1–2, free recall in Exp 3) [A]. — [Tran et al. DOI 10.3758/s13423-014-0646-x](https://www.doi.org/10.3758/S13423-014-0646-X); [Eglington & Kang DOI 10.1007/s10648-016-9386-y](https://doi.org/10.1007/s10648-016-9386-y)

**Spacing**
- Cepeda, Pashler, Vul, Wixted & Rohrer (2006), *Psychological Bulletin* 132(3), 354–380. 839 assessments, 317 experiments, 184 articles. Inter-study interval (ISI) and retention interval act jointly: "the ISI producing maximal retention increased as retention interval increased" [P]. Expanding vs. fixed intervals: expanding was better overall across 22 comparisons, but the authors call the conclusion "necessarily tentative" due to large between-study variability [P]. — [DOI 10.1037/0033-2909.132.3.354](https://doi.org/10.1037/0033-2909.132.3.354); [PDF](https://www.evullab.org/pdf/CepedaPashlerVulWixtedRohrer-PB-2006.pdf)
- Cepeda, Vul, Rohrer, Wixted & Pashler (2008), *Psychological Science* 19(11), 1095–1102. >1,350 participants, gaps up to 3.5 months, tests up to 1 year later. Optimal gap ≈ 20–40% of a 1-week test delay, falling to ≈ 5–10% of a 1-year delay; too-short gaps are far more costly than too-long ones (inverted-U, "ridgeline") [A]. — [DOI 10.1111/j.1467-9280.2008.02209.x](https://doi.org/10.1111/j.1467-9280.2008.02209.x); [PubMed](https://pubmed.ncbi.nlm.nih.gov/19076480/)
- Latimier, Peyre & Ramus (2021; online 2020), *Educational Psychology Review* 33, 959–987. Meta-analysis of 29 studies: spaced retrieval practice beats massed retrieval practice, g = 0.74 [A]; no reliable advantage of expanding over uniform schedules [R]. — [DOI 10.1007/s10648-020-09572-8](https://doi.org/10.1007/s10648-020-09572-8)
- Kapler, Weston & Wiseheart (2015), *Learning and Instruction* 36, 38–45. N = 169, simulated lecture, a single review either 1 or 8 days later, final test 5 weeks after review. The 8-day review produced better performance on **both factual and higher-level (application) questions** [P, abstract]. — [DOI 10.1016/j.learninstruc.2014.11.001](https://doi.org/10.1016/j.learninstruc.2014.11.001); [PDF](https://www.yorku.ca/ncepeda/publications/KWW2015.pdf)

**Successive relearning (retrieval to criterion × spaced sessions)**
- Rawson & Dunlosky (2011), *JEP: General* 140(3), 283–302. Prescriptive conclusion, as summarised in secondary sources: recall to a criterion of ~3 correct in initial learning, then relearn in ~3 widely spaced sessions [S]. — [DOI 10.1037/a0023956](https://doi.org/10.1037/a0023956)
- Rawson, Dunlosky & Sciartelli (2013), *Educational Psychology Review* 25(4), 523–548. Successive relearning of key-concept definitions in a real course improved exam performance and long-term retention over business-as-usual study. — [DOI 10.1007/s10648-013-9240-4](https://doi.org/10.1007/s10648-013-9240-4)
- Rawson & Dunlosky (2022), *Current Directions in Psychological Science* 31(4), 362–368. Review: one correct recall in each of three spaced sessions yielded 68% one-week retention vs. 26% for three correct recalls in a single session (citing Rawson et al., 2018) [A]. Same number of successful retrievals, 2.6× the retention — the spacing of *successful* retrievals is what matters. — [DOI 10.1177/09637214221100484](https://doi.org/10.1177/09637214221100484)

**Interleaving**
- Brunmair & Richter (2019), *Psychological Bulletin* 145(11), 1029–1052. 59 studies, 238 effect sizes: overall g = 0.42; **negative for word-based/expository materials (g = −0.39, blocking better)**; larger when categories are similar to one another and for more complex material [A]. — [DOI 10.1037/bul0000209](https://doi.org/10.1037/bul0000209); [PubMed](https://pubmed.ncbi.nlm.nih.gov/31556629/)
- Rohrer, Dedrick, Hartwig & Cheung (2020), *Journal of Educational Psychology* 112(1), 40–52. Preregistered classroom RCT, interleaved vs. blocked maths practice; delayed test 61% vs. 38%, d = 0.83 [R]. — [DOI 10.1037/edu0000367](https://doi.org/10.1037/edu0000367); earlier study: [Rohrer, Dedrick & Stershic 2015, DOI 10.1037/edu0000001](https://doi.org/10.1037/edu0000001)
- Kornell & Bjork (2008), *Psychological Science* 19(6), 585–592. Interleaving exemplars improved category induction, yet most participants judged massing more effective even after their own test showed the opposite [R]. — [DOI 10.1111/j.1467-9280.2008.02127.x](https://doi.org/10.1111/j.1467-9280.2008.02127.x)

**Utility reviews**
- Dunlosky, Rawson, Marsh, Nathan & Willingham (2013), *Psychological Science in the Public Interest* 14(1), 4–58. Of ten techniques, only **practice testing** and **distributed practice** rated *high* utility; **interleaved practice, elaborative interrogation, self-explanation** rated *moderate*; rereading, highlighting, summarization, keyword mnemonic, imagery rated *low* [S, APS release]. — [DOI 10.1177/1529100612453266](https://doi.org/10.1177/1529100612453266); [APS summary](https://www.psychologicalscience.org/news/releases/which-study-strategies-make-the-grade.html)
- Carpenter, Pan & Butler (2022), *Nature Reviews Psychology* 1, 496–511 — recent integrative review of spacing + retrieval. — [DOI 10.1038/s44159-022-00089-1](https://doi.org/10.1038/s44159-022-00089-1)
- Donoghue & Hattie (2021), *Frontiers in Education* 6 — meta-analytic re-examination of the ten Dunlosky techniques. — [DOI 10.3389/feduc.2021.581216](https://doi.org/10.3389/feduc.2021.581216)

### Inferences
- The repo's nearest lab analogue is the "study once + immediate test" cell. In Roediger & Karpicke that kind of condition looks as good or better at 5 minutes and loses roughly a third of the retrievable content relative to repeated retrieval at one week. The repo has no instrument that could detect this loss: `theory.md` already concedes "Presence of a proposition in the graph does not prove the learner still holds it."
- The per-step check *is* a retrieval event, so the design is not retrieval-free. But it is one massed retrieval at near-zero lag. The Rawson (68% vs 26%) result says the same retrieval count yields very different retention depending on whether retrievals are spaced across sessions.
- The transfer literature (Pan & Rickard) says untested material adjacent to tested material gets little benefit. So review prompts must target the propositions and chains themselves — not a sample of them — and should be *elaborated* (explain/apply), which is the moderator associated with transfer.
- The van Gog & Sweller / Tran et al. disputes are directly relevant to a proposition-and-chain model: retrieval of isolated premises does not automatically improve inference. Eglington & Kang's fix (retrieve premises *together* so relations can be processed) maps exactly onto retrieving a whole `chain` (premises → conclusion) rather than individual nodes.
- Interleaving is the weakest fit. The g = −0.39 for expository/word materials means there is no warrant to interleave *teaching* of conceptual propositions. The defensible use is in *review*: mix chains from different sessions, especially confusable ones (the moderator is between-category similarity).

### Gaps
- Exact exam-score and retention numbers from Rawson, Dunlosky & Sciartelli (2013) were not retrieved; only direction is reported above.
- Adesope et al. (2017) headline g (0.61 vs. 0.70) unresolved; full text was paywalled (HTTP 403).
- No meta-analysis was found that isolates retrieval/spacing effects for *one-to-one dialogue tutoring of adults in argumentative domains*; the evidence base is overwhelmingly text passages, key-term definitions, maths, and classroom quizzes.
- Almost no study tracks conceptual retention beyond ~5 weeks to 1 year for explanatory material; Cepeda (2008) used facts.

---

## 2. Immediate vs. delayed checks: learning vs. performance

### Takeaway
A check asked seconds after an explanation measures *performance* supported by working memory and the still-visible explanation; the literature treats it as an unreliable, often misleading index of learning. A delayed check at the start of the next session is both a far more valid measurement and itself a potent learning event.

### Cited Findings
- Soderstrom & Bjork (2015), *Perspectives on Psychological Science* 10(2), 176–199. Learning (durable change supporting retention and transfer) must be inferred and is dissociable from performance observed during acquisition; performance gains can occur without learning, learning without performance gains, and some manipulations move the two in *opposite* directions; people routinely misread acquisition performance as learning [A]. — [DOI 10.1177/1745691615569000](https://doi.org/10.1177/1745691615569000); [PubMed](https://pubmed.ncbi.nlm.nih.gov/25910388/)
- Bjork & Bjork (2020), *Journal of Applied Research in Memory and Cognition* 9(4), 475–479. Desirable difficulties (spacing, interleaving, retrieval, generation) slow apparent acquisition while improving retention and transfer; difficulties are only "desirable" when the learner can succeed with effort. — [DOI 10.1016/j.jarmac.2020.09.003](https://doi.org/10.1016/j.jarmac.2020.09.003)
- Bjork, Dunlosky & Kornell (2013), *Annual Review of Psychology* 64, 417–444. Review of how learners' beliefs and monitoring are systematically biased toward conditions that boost current performance. — [DOI 10.1146/annurev-psych-113011-143823](https://doi.org/10.1146/annurev-psych-113011-143823)
- Rowland (2014): the testing advantage is larger when the criterial test is ≥ 1 day later (g = 0.69) than same-day (g = 0.41) [S] — immediate measurement understates what retrieval does and overstates what restudy/explanation does. — [DOI 10.1037/a0037559](https://doi.org/10.1037/a0037559)
- Roediger & Karpicke (2006): the crossover (study wins at 5 min, testing wins at 1 week) is the canonical demonstration that an immediate check can rank conditions in the wrong order. — [DOI 10.1111/j.1467-9280.2006.01693.x](https://doi.org/10.1111/j.1467-9280.2006.01693.x)
- Nelson & Dunlosky (1991), *Psychological Science* 2(4), 267–271: judgments of learning become "extremely accurate" when delayed rather than made immediately after study (the delayed-JOL effect). Rhodes & Tauber (2011), *Psychological Bulletin* 137(1), 131–148, confirm the accuracy benefit meta-analytically while finding only a modest effect on memory itself [A]. — [DOI 10.1111/j.1467-9280.1991.tb00147.x](https://doi.org/10.1111/j.1467-9280.1991.tb00147.x); [DOI 10.1037/a0021705](https://doi.org/10.1037/a0021705)
- Kapler et al. (2015): a single delayed review at 8 days (vs. 1 day) improved 5-week performance on factual *and* application questions [P]. — [DOI 10.1016/j.learninstruc.2014.11.001](https://doi.org/10.1016/j.learninstruc.2014.11.001)
- Cepeda et al. (2008): for a ~1-week target the optimal gap is roughly 1–3 days; for months-to-a-year targets, weeks [A]. — [DOI 10.1111/j.1467-9280.2008.02209.x](https://doi.org/10.1111/j.1467-9280.2008.02209.x)

### Inferences
- The repo's immediate check is still worth keeping, but for what it actually does: it is a *comprehension gate* (did the step parse; which wrong model is active) and a first low-lag retrieval. The existing rules "prefer apply over parrot" and "design misses to name the wrong model" are well aimed at that job. It should stop being treated as evidence that the proposition is *held*.
- A delayed check at the start of the next session buys three things at once: (1) the first valid measurement of learning the system ever takes; (2) a spaced retrieval, the highest-utility intervention available; (3) calibration feedback for the learner — a delayed attempt is exactly the condition under which self-judgment becomes accurate (delayed-JOL effect).
- Within a session, checks could also be *lagged*: after step N, ask about step N−2 or ask a cumulative question that requires an earlier step. This introduces spacing inside the session at zero schedule cost.
- `learning-ground` already "probes what you hold" at session start. That probe is structurally a delayed retrieval test but is currently framed as measurement for planning only, is not targeted at previously taught nodes, and its outcome is not written back anywhere durable.

### Gaps
- No study found that directly compares "immediate per-step check only" against "immediate + next-session check" inside conversational LLM tutoring.
- Rhodes & Tauber's numeric effect size for delayed-JOL accuracy was not retrieved.

---

## 3. "Feels obviously true" as the terminal criterion: fluency, JOLs, illusion of explanatory depth, and AI explanations

### Takeaway
Felt obviousness immediately after a clear, well-sequenced explanation is the textbook condition for a metacognitive illusion: the feeling tracks processing fluency and the presence of the answer, not future ability to reproduce or use the idea. Emerging (still thin) evidence suggests LLM explanations amplify this. The literature's remedy is to make the learner *generate* before judging — explain, reconstruct, apply — and preferably after a delay.

### Cited Findings

**Why the feeling is unreliable**
- Koriat (1997), *JEP: General* 126(4), 349–370. Cue-utilization account: JOLs are inferences from cues (intrinsic, extrinsic, mnemonic such as ease of processing), not readouts of memory strength. — [DOI 10.1037/0096-3445.126.4.349](https://doi.org/10.1037/0096-3445.126.4.349)
- Koriat & Bjork (2005), *JEP: LMC* 31(2), 187–194. "Foresight bias": judgments made while the answer is present are inflated because conditions at study differ from conditions at test. — [DOI 10.1037/0278-7393.31.2.187](https://doi.org/10.1037/0278-7393.31.2.187)
- Rozenblit & Keil (2002), *Cognitive Science* 26(5), 521–562. Illusion of explanatory depth (IOED): people rate their understanding of causal mechanisms highly, then lower the rating after being asked to write out the explanation; the drop is specific to explanatory knowledge rather than facts or procedures [S for the specificity claim]. — [DOI 10.1207/s15516709cog2605_1](https://doi.org/10.1207/s15516709cog2605_1)
- Fisher, Goddu & Keil (2015), *JEP: General* 144(3), 674–687. Searching the internet for explanations inflates self-assessed knowledge, even in unrelated domains — access to an external explainer is misattributed to one's own understanding. — [DOI 10.1037/xge0000070](https://doi.org/10.1037/xge0000070)
- Carpenter, Wilford, Kornell & Mullaney (2013), *Psychonomic Bulletin & Review* 20(6), 1350–1356. A fluent instructor produced significantly higher perceived learning than a disfluent one delivering the same content, with **no difference in actual learning** [A]. — [DOI 10.3758/s13423-013-0442-z](https://doi.org/10.3758/s13423-013-0442-z)
- Deslauriers, McCarty, Miller, Callaghan & Kestin (2019), *PNAS* 116(39), 19251–19257. In randomized physics classes, students in active-learning sessions learned more but reported a *lower* feeling of learning than those given polished lectures; the authors warn that evaluating instruction by felt learning promotes inferior methods [A]. — [DOI 10.1073/pnas.1821936116](https://doi.org/10.1073/pnas.1821936116)
- Karpicke & Blunt (2011): JOLs were highest for repeated study (M = .79), the worst-performing repeated condition [P]. — [SOM](https://learninglab.psych.purdue.edu/downloads/2011/2011_Karpicke_Blunt_ScienceSupportingMaterial.pdf)
- Dunlosky & Rawson (2012), *Learning and Instruction* 22(4), 271–280. Overconfident self-evaluations of recalled key-concept definitions lead learners to stop early and retain less (title: "Overconfidence produces underachievement"); follow-up work shows judging one's answer against explicit *idea-unit* standards reduces overconfidence [S]. — [DOI 10.1016/j.learninstruc.2011.08.003](https://doi.org/10.1016/j.learninstruc.2011.08.003)
- Kruger & Dunning (1999), *JPSP* 77(6), 1121–1134: least-skilled performers overestimate most. **Caveat:** Gignac & Zajenkowski (2020), *Intelligence* 80, 101449, argue the classic pattern is "(mostly) a statistical artefact" (regression to the mean + better-than-average effect). Use Dunning–Kruger as illustration, not as load-bearing evidence. — [DOI 10.1037/0022-3514.77.6.1121](https://doi.org/10.1037/0022-3514.77.6.1121); [DOI 10.1016/j.intell.2020.101449](https://doi.org/10.1016/j.intell.2020.101449)

**AI / LLM-specific evidence (2024–2026; thin, mostly single studies)**
- Aslanov, Felmer & Guerra (2026), "Overconfidence without Understanding? Evidence for an Illusion of Understanding in AI-Assisted Explanations," *Proceedings of the Annual Meeting of the Cognitive Science Society* 48. Between-subjects: one group consulted ChatGPT on four topics, another read texts identical to the AI answers. The AI group showed the greatest overestimation of explanatory ability, and coder ratings plus automated text analyses showed *lower* explanation quality in the AI group [A, via search summary; the eScholarship page did not render for direct reading]. — [eScholarship](https://escholarship.org/uc/item/8cr599sr)
- Fernandes, Villa, Nicholls, Haavisto, Buschek, Schmidt, Kosch, Shen & Welsch, "AI makes you smarter but none the wiser: The disconnect between performance and metacognition," *Computers in Human Behavior* (DOI 10.1016/j.chb.2025.108779; arXiv Sept 2024). ~500 participants on LSAT-style reasoning with an LLM: performance rose but participants overestimated their scores by about 4 points; the usual Dunning–Kruger gradient flattened and higher AI literacy went with *more* overconfidence [S]. The authors suggest having the AI ask users to explain their reasoning. — [arXiv 2409.16708](https://arxiv.org/abs/2409.16708v1); [Aalto record](https://research.aalto.fi/en/publications/ai-makes-you-smarter-but-none-the-wiser-the-disconnect-between-pe/)
- Stadler, Bannert & Sailer (2024), *Computers in Human Behavior* 160, 108386. Title-level finding: LLMs "reduce mental effort but compromise depth in student scientific inquiry." — [DOI 10.1016/j.chb.2024.108386](https://doi.org/10.1016/j.chb.2024.108386)
- Bastani, Bastani, Sungu, Ge, Kabakcı & Mariman (2025), *PNAS* 122(26). ~1,000 Turkish high-school maths students. Unrestricted GPT-4 improved practice performance by 48% but exam performance *without* AI was 17% **lower** than never-access controls; a guard-railed tutor (hints, no answers) improved practice by 127% and largely eliminated the harm, without producing an exam gain [A]. Performance-during-assistance and learning dissociate sharply. — [DOI 10.1073/pnas.2422633122](https://doi.org/10.1073/pnas.2422633122)
- Kestin, Miller, Klales, Milbourne & Ponti (2025), *Scientific Reports* 15. Harvard physics crossover RCT (N = 194): a carefully engineered AI tutor (one step at a time, scaffolded, active engagement) beat in-class active learning, reported effect 0.73–1.3 SD, in less time [S]. **Note:** outcome was an immediate post-test, not delayed retention. — [DOI 10.1038/s41598-025-97652-6](https://doi.org/10.1038/s41598-025-97652-6)
- Messeri & Crockett (2024), *Nature* 627, 49–58 — conceptual argument that AI tools create "illusions of understanding" in science (not a learning experiment). — [DOI 10.1038/s41586-024-07146-0](https://doi.org/10.1038/s41586-024-07146-0)

**Objective criteria the literature supports instead / in addition**
- *Explain-then-rate.* The IOED manipulation itself: asking for a written step-by-step explanation deflates inflated ratings (Rozenblit & Keil 2002). — [DOI 10.1207/s15516709cog2605_1](https://doi.org/10.1207/s15516709cog2605_1)
- *Delayed judgment after a retrieval attempt* (Nelson & Dunlosky 1991; Rhodes & Tauber 2011). — [DOI 10.1037/a0021705](https://doi.org/10.1037/a0021705)
- *Free recall / recitation.* McDaniel, Howard & Einstein (2009), *Psychological Science* 20(4), 516–522: read–recite–review outperforms rereading and matches or beats note-taking with less time [R]. — [DOI 10.1111/j.1467-9280.2009.02325.x](https://doi.org/10.1111/j.1467-9280.2009.02325.x)
- *Teach-back.* Fiorella & Mayer (2013), *Contemporary Educational Psychology* 38(4), 281–288: actually teaching (not merely expecting to) improves delayed comprehension. Koh, Lee & Lim (2018), *Applied Cognitive Psychology* 32(3), 401–410: the benefit of teaching depends on retrieving the material (teaching without notes), i.e. teach-back works *because* it is retrieval. — [DOI 10.1016/j.cedpsych.2013.06.001](https://doi.org/10.1016/j.cedpsych.2013.06.001); [DOI 10.1002/acp.3410](https://doi.org/10.1002/acp.3410)
- *Idea-unit scoring against a standard* (Dunlosky & Rawson 2012 line of work) to keep self-scoring honest. — [DOI 10.1016/j.learninstruc.2011.08.003](https://doi.org/10.1016/j.learninstruc.2011.08.003)
- *Transfer / application items* (Pan & Rickard 2018; Butler 2010). — [DOI 10.1037/bul0000151](https://doi.org/10.1037/bul0000151)

### Inferences
- The repo's terminal condition is a subjective judgment, made (a) immediately, (b) with the explanation still on screen, (c) after a maximally fluent, logistics-free, one-step-at-a-time presentation, (d) from an AI explainer, and (e) confirmed by the same learner. Each of (a)–(d) is an independently documented inflator of felt understanding; (e) adds no independent evidence.
- The design's own distinction — "memorized-but-not-self-evident is not held" — is pedagogically sound (it targets generative structure, the "click"), but the *measurement* of self-evidence is the weak link. The same goal can be operationalised objectively: can the learner regenerate the chain from the base premises with the transcript closed? That *is* a test of "generated by a few base facts".
- The repo already has the ideal scoring standard for idea-unit-style grading: each `chain` lists its premises and conclusion. A reconstruction can be scored as premises-recalled / premises-total plus whether the inferential link was stated.
- "Feels obviously true" need not be discarded. It is cheap, and recording it *alongside* an objective result yields a calibration signal (confidence vs. outcome) the learner can be shown — which the IOED and delayed-JOL literatures suggest is itself corrective.
- Kestin et al. suggests the repo's core moves (one step at a time, wait for the learner, engineered prompts) are the kind of design that makes AI tutoring work; Bastani et al. suggests the risk lies in what happens when the tutor carries the cognitive work. Neither study measured retention, which is exactly this repo's blind spot too.

### Gaps
- The AI-specific IOED evidence is one conference paper (Aslanov et al. 2026) plus adjacent studies; sample sizes and effect sizes for Aslanov et al. were not retrievable. Treat "LLM explanations inflate felt understanding" as *probable and mechanistically expected*, not established.
- Fernandes et al.'s journal year (2025 vs. 2026) is inconsistent across records.
- No study found testing whether *step-wise Socratic* LLM tutoring (as opposed to answer-giving) inflates felt understanding less.
- No direct study of expert-human one-to-one explanation and IOED was located; the instructor-fluency studies are video lectures.

---

## 4. Pretesting, productive failure, and generation: should "predict before reveal" be the default?

### Takeaway
Yes, with conditions. Attempting an answer before instruction reliably improves learning of the targeted content (g ≈ 0.54 when learners actually generate; ≈ 0.22 when they merely read the question), and problem-solving-before-instruction shows g ≈ 0.36 for conceptual understanding and transfer. The benefit is specific to what was pre-asked, depends on the learner having enough prior knowledge to make a meaningful attempt, and requires corrective instruction afterwards.

### Cited Findings
- Richland, Kornell & Kao (2009), *JEP: Applied* 15(3), 243–257. Unsuccessful pretest attempts improved later learning of the tested content relative to extra study time. — [DOI 10.1037/a0016496](https://doi.org/10.1037/a0016496)
- Kornell, Hays & Bjork (2009), *JEP: LMC* 35(4), 989–998. "Unsuccessful retrieval attempts enhance subsequent learning" (with feedback). — [DOI 10.1037/a0015729](https://doi.org/10.1037/a0015729)
- St. Hilaire, Chan & Ahn (2024; online 2023), *Psychonomic Bulletin & Review* 31(2), 411–441. Preregistered meta-analysis of the prequestion effect: **specific effect g = 0.54 (k = 97); general effect on non-prequestioned material near zero**; g = 0.65 when learners had to generate an answer vs. 0.22 when they only read the questions [S, via citing paper]. — [DOI 10.3758/s13423-023-02353-8](https://doi.org/10.3758/s13423-023-02353-8)
- Pan & Carpenter (2023), *Educational Psychology Review* 35(4). Review: prequestioning/pretesting often enhances memory and transfer, with magnitude depending on procedure and how learning is assessed. — [DOI 10.1007/s10648-023-09814-5](https://doi.org/10.1007/s10648-023-09814-5)
- Sinha & Kapur (2021), *Review of Educational Research* 91(5), 761–798. 53 studies, 166 comparisons: problem-solving-before-instruction beats instruction-first on conceptual knowledge/transfer, g = 0.36 [95% CI 0.20, 0.51]; g up to 0.58 with high fidelity to Productive Failure design; **effects favour instruction-first for younger learners (grades 2–5) and for domain-general skills** [A]. — [DOI 10.3102/00346543211019105](https://doi.org/10.3102/00346543211019105)
- Kapur (2014), *Cognitive Science* 38(5), 1008–1022. Productive failure in maths: generating solutions first yielded better conceptual understanding and transfer than direct instruction first, without loss of procedural fluency [R]. — [DOI 10.1111/cogs.12107](https://doi.org/10.1111/cogs.12107)
- Slamecka & Graf (1978), *JEP: Human Learning and Memory* 4(6), 592–604; Bertsch, Pesta, Wiscott & McDaniel (2007), *Memory & Cognition* 35(2), 201–210. Generation effect meta-analysis: 86 studies, 445 effect sizes, d ≈ 0.40 for generated over read items [A]. — [DOI 10.1037/0278-7393.4.6.592](https://doi.org/10.1037/0278-7393.4.6.592); [DOI 10.3758/BF03193441](https://doi.org/10.3758/BF03193441); [PubMed](https://pubmed.ncbi.nlm.nih.gov/17645161/)
- Chi & Wylie (2014), *Educational Psychologist* 49(4), 219–243. ICAP: learning outcomes order as Interactive > Constructive > Active > Passive; receiving an explanation is passive/active, generating a prediction or explanation is constructive. — [DOI 10.1080/00461520.2014.965823](https://doi.org/10.1080/00461520.2014.965823)
- Bjork & Bjork (2020): a difficulty is desirable only if the learner is equipped to respond to it successfully with effort. — [DOI 10.1016/j.jarmac.2020.09.003](https://doi.org/10.1016/j.jarmac.2020.09.003)

### Inferences
- The repo's two "placement moves" give a principled switch. For **motivated derivations** ("how could I have discovered this?") the learner by construction holds the premises, so a prediction attempt is feasible and the evidence supports making it the *default*, not optional. For **unconditional truths** (asserted because not derivable from what is held) a prediction is a blind guess; the prequestion literature still shows some benefit from guessing, but the productive-failure boundary conditions argue for keeping it optional there.
- The near-zero *general* prequestion effect means one prediction per step (which the per-step structure affords) is the right granularity; a single up-front pretest would only help the items it happened to ask about.
- "Still one check after the step lands" is consistent with the evidence that errorful generation needs corrective feedback.
- Predict-first also makes the session less fluent, which (per Section 3) should improve calibration of the terminal judgment, at some cost in learner comfort (Deslauriers et al. 2019: active conditions feel worse while working better).

### Gaps
- Productive-failure evidence is dominated by maths/science problem solving in schools; I found no meta-analytic evidence specifically for adult learners in argumentative/humanities domains.
- St. Hilaire et al. numbers come via a citing paper's summary, not the primary PDF.
- The publication-bias-adjusted g = 0.87 reported for Sinha & Kapur in search output is counter-intuitively *higher* than the raw estimate; not verified against the paper and not relied on here.

---

## 5. Self-explanation and elaborative interrogation: should checks ask "why"?

### Takeaway
Prompted self-explanation has a moderate, well-replicated benefit (g ≈ 0.55) and is more effective than receiving an instructor's explanation; Dunlosky et al. rate both self-explanation and elaborative interrogation as moderate utility. For a system whose unit of knowledge is the *reason* a proposition follows, "why does this follow?" checks are the best-matched format — and they double as the IOED debiasing manipulation.

### Cited Findings
- Chi, Bassok, Lewis, Reimann & Glaser (1989), *Cognitive Science* 13(2), 145–182. Good problem solvers spontaneously generate more self-explanations of worked examples and monitor their comprehension failures more accurately. — [DOI 10.1207/s15516709cog1302_1](https://doi.org/10.1207/s15516709cog1302_1)
- Chi, De Leeuw, Chiu & LaVancher (1994), *Cognitive Science* 18(3), 439–477. Merely *prompting* students to self-explain each sentence of an expository text improved understanding, with the largest gains on questions requiring inference/mental-model integration [R]. — [DOI 10.1207/s15516709cog1803_3](https://doi.org/10.1207/s15516709cog1803_3)
- Bisra, Liu, Nesbit, Salimi & Winne (2018), *Educational Psychology Review* 30(3), 703–725. Meta-analysis, 64 studies, ~6,000 participants: g = 0.55 for induced self-explanation; self-explanation > instructor-provided explanation > no explanation; benefit not attributable merely to extra time, though the authors flag time-on-task control as imperfect [S, BPS Research Digest]. — [DOI 10.1007/s10648-018-9434-x](https://doi.org/10.1007/s10648-018-9434-x); [BPS digest](https://www.bps.org.uk/research-digest/self-explanation-powerful-learning-technique-according-meta-analysis-64-studies)
- Dunlosky et al. (2013): elaborative interrogation ("why is this true?") and self-explanation both *moderate* utility — promising but with thinner evidence on durability and on complex materials than testing/spacing [S]. — [DOI 10.1177/1529100612453266](https://doi.org/10.1177/1529100612453266)
- Hinze, Wiley & Pellegrino (2013), *Journal of Memory and Language* 69(2), 151–164. Retrieval practice improves later *application* performance when the retrieval task induces constructive/explanatory processing; retrieval that merely reproduces does not [R]. — [DOI 10.1016/j.jml.2013.03.002](https://doi.org/10.1016/j.jml.2013.03.002)
- Pan & Rickard (2018): "elaborated retrieval practice" is one of three moderators that produce transfer [R]. — [DOI 10.1037/bul0000151](https://doi.org/10.1037/bul0000151)
- Rozenblit & Keil (2002): generating an explanation recalibrates felt understanding. — [DOI 10.1207/s15516709cog2605_1](https://doi.org/10.1207/s15516709cog2605_1)

### Inferences
- The repo's check hierarchy ("prefer apply/predict over parrot") is in the right direction but omits the format with the most direct support for inferential knowledge: *explain why the step follows from what you already held*. Apply/predict tests whether the conclusion can be used; explain-why tests whether the chain (the thing the graph stores) exists in the learner.
- Bisra's ordering (self-explanation > instructor explanation) is a mild caution about the teach skill's expository default ("Socratic when they can reason there; expository when not"): where the learner *can* reason there, the evidence favours drawing the explanation out of them.
- Explain-why answers are free text an LLM can grade against chain premises — the grading problem that limits self-explanation in classrooms is absent here.
- A sensible rotation: predict (before) → teach → explain-why or apply (after), with explain-why mandatory on the final step into the goal.

### Gaps
- Bisra et al.'s moderator values were not retrieved from the primary text.
- Self-explanation studies mostly measure immediate or short-delay outcomes; durability evidence is weaker than for retrieval/spacing (this is Dunlosky et al.'s stated reason for "moderate").

---

## 6. Scheduling algorithms and LLM-generated review prompts: what must be stored?

### Takeaway
Every scheduler from SM-2 to FSRS needs the same irreducible data: a per-item, timestamped log of review outcomes. Everything else (ease, half-life, difficulty/stability) is derivable state. The psychological literature suggests the *existence* of spaced successful retrievals matters far more than the sophistication of the schedule, so an append-only review log plus a simple expanding rule is sufficient to start and leaves the door open to fitting FSRS later.

### Cited Findings
- **SM-2 lineage.** Anki's documentation describes its legacy scheduler as derived from SuperMemo's SM-2 and describes FSRS as the alternative. — [Anki docs](https://docs.ankiweb.net/faqs/what-spaced-repetition-algorithm.md)
- **Half-Life Regression.** Settles & Meeder (2016), *Proceedings of ACL 2016*, 1848–1858. Recall probability p = 2^(−Δ/h), with half-life h predicted from a learner's history with the item (counts of times seen / correct / incorrect) and item features; trained on Duolingo logs; 45%+ error reduction vs. baselines in predicting recall [A]. Required data: per-item last-practice time and cumulative right/wrong history. — [DOI 10.18653/v1/P16-1174](https://doi.org/10.18653/v1/P16-1174)
- **MEMORIZE.** Tabibian, Upadhyay, De, Zarezade, Schölkopf & Gomez-Rodriguez (2019), *PNAS* 116(10), 3988–3993. Casts scheduling as stochastic optimal control; optimal reviewing intensity is proportional to the probability the item has been forgotten (1 − recall probability) [R]; evaluated by natural experiment on Duolingo data. A PNAS commentary (Mozer et al.) questions whether its simplified memory model captures the inverted-U spacing dynamics [S]. — [DOI 10.1073/pnas.1815156116](https://doi.org/10.1073/pnas.1815156116); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6410845)
- **DSR / FSRS family.** Ye, Su & Cao (2022), *KDD '22*, 4381–4390: memory model with the Markov property fitted to 220 million review logs; scheduler minimising review cost via stochastic shortest path; 12.6% improvement over prior methods [A]. Su, Ye, Nie, Cao & Chen (2023), *IEEE TKDE* 35(10), 10085–10097: "Optimizing spaced repetition schedule by capturing the dynamics of memory." FSRS (the open-source scheduler now in Anki) tracks per-item **difficulty, stability, retrievability** — the "memory state" — where stability is the interval at which recall probability falls to 90%, and schedules a review when predicted retrievability drops to the target (default ≈ 0.9) [S, Anki docs]. — [DOI 10.1145/3534678.3539081](https://doi.org/10.1145/3534678.3539081); [DOI 10.1109/TKDE.2023.3251721](https://doi.org/10.1109/TKDE.2023.3251721); [Anki docs](https://docs.ankiweb.net/faqs/what-spaced-repetition-algorithm.md)
- **Does algorithmic personalisation matter?** Lindsey, Shroyer, Pashler & Mozer (2014), *Psychological Science* 25(3), 639–647. Semester-long middle-school study: personalised review scheduling improved end-of-semester retention by 16.5% over massed study and 10.0% over a one-size-fits-all spaced schedule [R]. — [DOI 10.1177/0956797613504302](https://doi.org/10.1177/0956797613504302)
- **Does expanding beat uniform?** Not reliably (Latimier et al. 2021 [R]; Cepeda et al. 2006 call the expanding advantage "tentative" [P]). — [DOI 10.1007/s10648-020-09572-8](https://doi.org/10.1007/s10648-020-09572-8); [DOI 10.1037/0033-2909.132.3.354](https://doi.org/10.1037/0033-2909.132.3.354)
- **Gap sizing.** Optimal gap ≈ 10–20% of the desired retention horizon, shrinking proportionally as the horizon lengthens; erring long is cheaper than erring short (Cepeda et al. 2008) [A]. — [DOI 10.1111/j.1467-9280.2008.02209.x](https://doi.org/10.1111/j.1467-9280.2008.02209.x)
- **LLM tutoring dialogue → learner model.** Scarlatos, Baker & Lan (LAK '25; arXiv 2409.16490), "Exploring Knowledge Tracing in Tutor-Student Dialogues using LLMs": LLMs tag each dialogue turn with knowledge components and judge response correctness; the resulting LLMKT model outperforms prior KT methods at predicting correctness. They note no open tutoring-dialogue dataset links the same student *across* dialogues — i.e. there is no public evidence base for cross-session retention in LLM tutoring. — [arXiv 2409.16490](https://arxiv.org/html/2409.16490v2)
- **Forgetting-aware LLM tutors.** TASA (arXiv 2511.15163) combines knowledge tracing with a learnable forgetting curve to update per-concept mastery and adapt LLM maths tutoring; IntelliCode (arXiv 2512.18669) is a multi-agent LLM tutor with a centralised learner model that cites Settles & Meeder. Both are preprints; I read only search summaries, not the papers. — [arXiv 2511.15163](https://arxiv.org/pdf/2511.15163v1); [arXiv 2512.18669](https://arxiv.org/pdf/2512.18669)

### Inferences
- **Minimum data to schedule anything:** one append-only event per retrieval attempt with (item id, timestamp, outcome). From that log alone SM-2 state, HLR features (seen/correct/incorrect counts, lag), and FSRS difficulty/stability can all be recomputed by replay. Storing derived state (`due`, `stability`) is a cache, not a requirement.
- **Recommended event fields**, each justified above: `targetId` (node or chain — chains matter per Eglington & Kang), `ts`, `sessionId`, `promptType` (free-recall / explain-why / reconstruct-chain / apply / predict), `lagDays` since last event on this target (derivable), `grade` on a 4-point scale compatible with FSRS (again / hard / good / easy) or an idea-unit fraction, `hinted` (boolean — cued success is weaker evidence), and `confidence` *before* answering (for calibration, Section 3).
- This fits the repo's existing style: append-only JSONL with deterministic replay. It need not violate "no mastery scores on nodes" — keep `nodes.jsonl`/`chains.jsonl` pure and put events in a separate `.learning/graph/reviews.jsonl` (or a per-learner `.learning/reviews/`). The schema's current "do not store practice outcomes" rule protects the *domain* graph's shareability; it does not require that outcomes be stored nowhere.
- **Schedule choice:** the evidence does not justify starting with FSRS. With tens-to-hundreds of items and conversational review, a fixed expanding ladder (e.g. next session / ~3 d / ~1 wk / ~3 wk / ~2 mo, reset one rung on failure) captures most of the benefit; Lindsey et al. suggest personalisation adds a further ~10% — worth having later, cheap to add because the log is the same.
- A structural mismatch to design around: schedulers assume short, atomic, auto-gradable cards. This repo's items are arguments reviewed in dialogue, graded by an LLM. Review cost per item is minutes, not seconds, so the scheduler should cap per-session load and prioritise (a) chains over leaf nodes and (b) items on the path of the *next* goal (reviewing prerequisites just before building on them).
- The agent-skill form factor has no push notifications. Review can only happen when the learner opens a session, so the practical design is "review due items at the *start* of whatever skill is invoked next" plus an on-demand `learning-review` skill — an opportunistic, long-gap-tolerant schedule. Cepeda (2008) says long gaps are the cheaper error.

### Gaps
- **No peer-reviewed study was found (2023–2026) that generates spaced retrieval prompts or flashcards from LLM tutoring dialogue and evaluates delayed retention.** The closest work is dialogue knowledge tracing (prediction accuracy, not retention outcomes) and preprint system descriptions. This is a real hole in the literature, not just in my search.
- SM-2's original specification (Woźniak, SuperMemo) was not fetched this session; from memory it stores per item a repetition count, an ease factor (initially 2.5) and the current interval, updated from a 0–5 quality grade (intervals 1 day, 6 days, then previous × ease). Verify against the primary before relying on it: `https://super-memory.com/english/ol/sm2.htm`.
- FSRS's exact parameter count/version and required revlog schema were not confirmed from the project's own wiki.
- All algorithm evidence comes from vocabulary/flashcard logs (Duolingo, MaiMemo, Anki). No evidence that fitted forgetting curves for paired associates describe forgetting of multi-premise arguments.
- Matuschak & Nielsen's "mnemonic medium" (spaced prompts embedded in conceptual essays) is the best-known attempt at spaced repetition for conceptual material, but I did not verify a source this session and it is not peer-reviewed; listed as a lead only.

---

## 7. Does spacing/retrieval apply to proposition-and-argument knowledge (e.g. philosophy), and in what form?

### Takeaway
Yes, by reasonable extension: benefits are demonstrated for expository science texts, key-concept definitions, inference and application questions, and deductive inference — provided the retrieval task engages the *relations* (explain, reconstruct, apply), not isolated statements. There is no direct evidence for philosophy or argument reconstruction specifically.

### Cited Findings
- Retrieval practice improved performance on inference questions about science texts and outperformed an explicitly relational/elaborative activity (concept mapping), d = 1.07–1.50 [P]. — [Karpicke & Blunt 2011](https://doi.org/10.1126/science.1199327)
- Spaced review improved 5-week performance on higher-level application questions, not only facts [P]. — [Kapler et al. 2015](https://doi.org/10.1016/j.learninstruc.2014.11.001)
- Successive relearning was developed and validated on multi-idea *key-concept definitions* from course material scored by idea units, not on paired associates. — [Rawson, Dunlosky & Sciartelli 2013](https://doi.org/10.1007/s10648-013-9240-4); [Rawson & Dunlosky 2022](https://doi.org/10.1177/09637214221100484)
- Retrieval practice benefits deductive inference only when premises are practised in a format that permits relational processing (premises shown/retrieved together) [A]; isolated-premise retrieval produced no inference benefit in Tran et al. (2015). — [Eglington & Kang](https://doi.org/10.1007/s10648-016-9386-y); [Tran, Rohrer & Pashler 2015](https://www.doi.org/10.3758/S13423-014-0646-X)
- Explanatory/constructive retrieval is what yields application-level gains (Hinze et al. 2013 [R]); "elaborated retrieval" moderates transfer (Pan & Rickard 2018 [R]). — [DOI 10.1016/j.jml.2013.03.002](https://doi.org/10.1016/j.jml.2013.03.002); [DOI 10.1037/bul0000151](https://doi.org/10.1037/bul0000151)
- Complexity caveat: benefits may shrink for highly interactive material (van Gog & Sweller 2015), disputed (Karpicke & Aue 2015). — [DOI 10.1007/s10648-015-9310-x](https://doi.org/10.1007/s10648-015-9310-x); [DOI 10.1007/s10648-015-9309-3](https://doi.org/10.1007/s10648-015-9309-3)
- Interleaving does **not** transfer cleanly to expository material (g = −0.39 for word-based materials) [A]. — [Brunmair & Richter 2019](https://doi.org/10.1037/bul0000209)
- Mathematics (procedural + conceptual): spaced retrieval practice improved short- and long-term retention in a college precalculus course (title-level). — [Hopkins, Lyle, Hieb & Ralston 2016](https://doi.org/10.1007/s10648-015-9349-8)

### Inferences
- The repo's data model is unusually well suited to the form the literature favours. Suggested prompt types, in rough order of evidential support:
  1. **Reconstruct the chain** — "Without looking: why does *C* hold? Give the premises and how they combine." (free recall + explanation; scored against `chain.premises`). Directly implements Eglington & Kang's joint-premise condition and the IOED explain manipulation.
  2. **Apply / transfer** — a new case that the conclusion decides. (Pan & Rickard: application and inference items show transfer.)
  3. **Missing-premise / counterfactual** — "If premise *P2* were false, what happens to *C*?" Tests the joint-entailment structure the schema insists on ("all premises are used together").
  4. **Teach-back of the whole goal** — explain the session's goal to a novice from the base facts (Fiorella & Mayer; Koh et al.).
  5. **Discriminate** — contrast two easily confused propositions from different sessions (the one place interleaving's similarity moderator applies).
- Avoid cloze-deletion or verbatim-statement recall of `node.statement` as the main review format: that is the "rearranged stimulus–response / isolated premise" regime where transfer is weakest.
- For philosophy specifically (the current session in the repo is on Heidegger), the claim that these effects hold is an *extrapolation* from science exposition and definitional concepts. It is a well-motivated extrapolation — the mechanisms are not domain-specific — but should be labelled as such in any report.

### Gaps
- No experimental study located on retrieval practice or spacing for philosophical arguments, argument mapping, or proof reconstruction with delayed outcomes.
- No evidence on optimal review *granularity* (node vs. chain vs. whole-goal) for hierarchically structured knowledge.

---

## 8. Evidence-linked implications for this repo

### Takeaway
The teaching loop is largely consistent with the evidence; the system's weaknesses are (1) nothing is ever retrieved after a delay, (2) success is defined by an immediate feeling, and (3) nothing is stored that would let either be fixed. All three can be addressed without abandoning the repo's principles: add a review skill, an append-only review log, an objective-plus-subjective terminal condition, and stronger check formats.

### Cited Findings (design decision → evidence → change)

**(a) "Teaching only — no practice skill"; nothing schedules or records retrieval. — Not supported; highest-priority change.**
- Evidence: practice testing and distributed practice are the only two *high-utility* techniques ([Dunlosky et al. 2013](https://doi.org/10.1177/1529100612453266)); testing g ≈ 0.50 rising to 0.69 at ≥ 1 day ([Rowland 2014](https://doi.org/10.1037/a0037559)); spaced vs. massed retrieval g = 0.74 ([Latimier et al. 2021](https://doi.org/10.1007/s10648-020-09572-8)); 68% vs. 26% one-week retention for the same number of correct recalls when spaced across sessions ([Rawson & Dunlosky 2022](https://doi.org/10.1177/09637214221100484)); holds for application questions ([Kapler et al. 2015](https://doi.org/10.1016/j.learninstruc.2014.11.001)).
- Change 1 — **new skill `learning-review`** (successive relearning): pull due chains/nodes, ask reconstruct / explain-why / apply prompts with transcript closed, wait, grade against chain premises, re-teach on miss using the existing repair move and re-ask later in the same sitting until one correct recall, then log. Cap items per sitting.
- Change 2 — **opening retrieval in `learning-ground` and `learning-teach`**: before new material, cold-probe the due items and the prerequisite nodes the new plan builds on; when resuming a paused session, begin with free recall of the prior steps rather than a recap. (`learning-ground` already probes; make it targeted at graph nodes and write the outcome back.)
- Change 3 — **`reviews.jsonl`** (append-only, separate from the domain graph): `{targetId, targetType: node|chain, ts, sessionId, promptType, grade (again/hard/good/easy or idea-unit fraction), hinted, confidenceBefore}`; derive `lastRetrievedAt`, streak, and `dueAt` by replay. This is the minimum log every scheduler needs ([Settles & Meeder 2016](https://doi.org/10.18653/v1/P16-1174); [Ye et al. 2022](https://doi.org/10.1145/3534678.3539081)). Also log the in-lesson check outcomes there as lag-0 events.
- Change 4 — **simple schedule first**: expanding ladder (next session, ~3 d, ~1 wk, ~3 wk, ~2 mo; drop a rung on failure). Gap sizing per [Cepeda et al. 2008](https://doi.org/10.1111/j.1467-9280.2008.02209.x); no reliable expanding-vs-uniform difference, so do not over-engineer ([Latimier et al. 2021](https://doi.org/10.1007/s10648-020-09572-8)); FSRS/HLR can be fitted to the same log later, with personalisation worth roughly +10% ([Lindsey et al. 2014](https://doi.org/10.1177/0956797613504302) [R]).

**(b) Terminal condition "goal feels obviously true and the learner confirms". — Not supported as the sole criterion; keep as one input.**
- Evidence: fluent explanation raises perceived but not actual learning ([Carpenter et al. 2013](https://doi.org/10.3758/s13423-013-0442-z)); feeling of learning can be *inversely* related to learning ([Deslauriers et al. 2019](https://doi.org/10.1073/pnas.1821936116)); explanatory understanding in particular is overestimated until one tries to explain ([Rozenblit & Keil 2002](https://doi.org/10.1207/s15516709cog2605_1)); external explainers, and plausibly LLMs, inflate it further ([Fisher et al. 2015](https://doi.org/10.1037/xge0000070); [Aslanov et al. 2026](https://escholarship.org/uc/item/8cr599sr); [Fernandes et al.](https://arxiv.org/abs/2409.16708v1)); immediate judgments with the answer present are biased ([Koriat & Bjork 2005](https://doi.org/10.1037/0278-7393.31.2.187)).
- Change 5 — **two-stage status.** `taught` requires, in addition to the learner's confirmation: (i) a closed-transcript **teach-back** of the goal from the base facts, scored against the plan's chains; (ii) one **novel transfer** question. Then a new status `retained` (or `held`) is set only after a successful delayed reconstruction in a later session. Record `feltObvious` and the objective score side by side and show the learner the gap (calibration).
- Change 6 — **reword `theory.md`**: keep "memorized-but-not-self-evident is not held", but define "held" operationally as *can regenerate the chain from the base facts after a delay*, with felt obviousness as necessary-not-sufficient.

**(c) One immediate check per step; apply/predict preferred; miss → repair. — Partly supported; reframe and extend.**
- Supported: checking each step with feedback and repair; preferring application over parroting ([Pan & Rickard 2018](https://doi.org/10.1037/bul0000151)); designing misses to be diagnostic.
- Not supported: treating an immediate pass as evidence of learning ([Soderstrom & Bjork 2015](https://doi.org/10.1177/1745691615569000)).
- Change 7 — add **explain-why** as a first-class check type ("why does this follow from what you already held?"), g ≈ 0.55 for prompted self-explanation, better than receiving the explanation ([Bisra et al. 2018](https://doi.org/10.1007/s10648-018-9434-x)); required at chain conclusions.
- Change 8 — add **lagged/cumulative checks** within the session (every few steps ask something that needs a step from earlier, without scroll-back) and a **closing free-recall** of the whole path before the teach-back.
- Change 9 — capture **confidence before the answer** on checks (the SKILL already mentions "optional thinking/confidence"); log it.

**(d) System owns logistics; minimal tree prunes off-path material. — Mostly supported; one caution.**
- Supported: removing extraneous planning load and teaching in small, checked steps is the design that performed well in the one strong LLM-tutor RCT ([Kestin et al. 2025](https://doi.org/10.1038/s41598-025-97652-6)); guard-railed, non-answer-giving tutoring avoids the harm seen with unrestricted chat ([Bastani et al. 2025](https://doi.org/10.1073/pnas.2422633122)). Not interleaving the *teaching* of conceptual material is consistent with g = −0.39 for expository materials ([Brunmair & Richter 2019](https://doi.org/10.1037/bul0000209)).
- Caution: "the learner's effort goes into the material" must not become "the learner expends little effort". Desirable difficulties are intrinsic to the material — retrieval, generation, spacing — and a maximally smooth path is the condition for fluency illusions ([Bjork & Bjork 2020](https://doi.org/10.1016/j.jarmac.2020.09.003)). Add a line to `theory.md`: own the logistics, but never do the learner's retrieval or generation for them.
- Change 10 — the plan's "do not re-teach what is already held" should become "do not re-*teach*, but do re-*retrieve*": prerequisite nodes from the graph get a cold probe before being built on, and a failed probe converts them into repair steps (this is already the spirit of "probe in chat to see what the learner still holds").

**(e) Optional "predict before reveal". — Evidence supports making it the default for derived steps.**
- Evidence: prequestions with generation g = 0.65 vs. 0.22 for merely reading the question; overall specific effect g = 0.54; no spill-over to un-asked content ([St. Hilaire et al. 2024](https://doi.org/10.3758/s13423-023-02353-8)); problem-solving-before-instruction g = 0.36 for conceptual/transfer outcomes, with boundary conditions ([Sinha & Kapur 2021](https://doi.org/10.3102/00346543211019105)); generation effect d ≈ 0.40 ([Bertsch et al. 2007](https://doi.org/10.3758/BF03193441)).
- Change 11 — in `learning-teach`: **default to predict-first on "motivated derivation" steps** (learner holds the premises); keep it optional on "unconditional truth" steps; always follow with the explanation and the post-step check (already specified); let the learner opt out. Log the prediction as an event.

**(f) Graph stores propositions and chains, no mastery/review data. — Keep the graph pure; add a sibling store.**
- Supported: the proposition + joint-premise chain representation is exactly the unit the inference literature says must be retrieved together ([Eglington & Kang](https://doi.org/10.1007/s10648-016-9386-y)), and it supplies ready-made idea-unit scoring standards ([Dunlosky & Rawson 2012](https://doi.org/10.1016/j.learninstruc.2011.08.003)). The schema's own caveat ("presence … does not prove the learner still holds it") is correct and is precisely what the review log would resolve.
- Change 12 — amend `graph-schema.md` "What not to store here": keep mastery off `nodes.jsonl`/`chains.jsonl`, but define the separate `reviews.jsonl` event log (Change 3). Store raw events, not a mastery score — consistent with "not a gradebook" and with how FSRS/HLR consume data.
- Change 13 — optionally have `learning-graph` emit, per chain, 1–3 **review prompts** (reconstruct / apply / counterfactual) at extraction time while the transcript context is available, stored with provenance; the review skill can also generate them on the fly.

### Inferences
- Priority order by expected effect per unit of work: (1) review log + opening retrieval of due items; (2) terminal teach-back + delayed `retained` status; (3) explain-why and lagged checks; (4) predict-first default; (5) dedicated `learning-review` skill with scheduling; (6) algorithm upgrades. Items 1–4 are edits to existing SKILL/theory files and one new JSONL file.
- The single most informative experiment the repo owner could run on themselves: at the start of the next session, before any recap, attempt a closed-transcript reconstruction of the previous session's goal chain, and compare the score with the "feels obviously true" confirmation that ended that session. The literature predicts a visible gap.
- These changes make sessions feel harder and slower. Per Deslauriers et al., the learner should be told this in advance — the discomfort is the mechanism, not a defect.

### Gaps
- None of the recommended changes has been evaluated in the specific setting of an agent-skill LLM tutor with a personal knowledge graph; they are extrapolations from classroom and laboratory evidence, strongest for (a), (b), (c) and weakest for anything about algorithm choice or philosophy-specific content.
- LLM grading of free-text reconstructions against chain premises is assumed to be adequately reliable; I did not research its accuracy.
- Numbers tagged [R] or [S] above should be checked against primary texts before being quoted in a final report; items with unresolved conflicts are Adesope et al. (2017) overall g, and Fernandes et al. publication year.
