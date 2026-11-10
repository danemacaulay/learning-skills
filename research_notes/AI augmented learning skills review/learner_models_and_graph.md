# Learner modelling, knowledge tracing and knowledge-graph representations — review of how the `learning` repo stores learning material

Scope note. These notes evaluate five storage decisions in the `learning` repo: (a) append-only JSONL graph of propositions plus joint-premise chains, extracted by an LLM from teacher prose only; (b) no mastery, confidence, outcomes or review timestamps anywhere in the graph; (c) learner evidence only in per-session markdown (`grounding.md`, `plan.md`, `transcript.md`); (d) node identity by LLM judgment, first-write-wins, no revision or retraction; (e) next session pre-reads the graph and re-probes from scratch.

Verification legend, applied to every citation:
- **[V-full]** I read the paper's own page or full text in this session.
- **[V-bib]** Existence and bibliographic details confirmed against an index (Crossref, DBLP, publisher or repository page); content statements come from the abstract or from standard, widely reproduced descriptions.
- **[V-snip]** Existence confirmed, but the specific claim comes from a search-result excerpt or a secondary source. Check before quoting.
- **Preprint** and **small-N** are flagged inline.

---

## 1. Domain model vs learner model: is refusing to store any per-learner mastery state supported?

### Takeaway
Separating a domain model from a learner model is the orthodox architecture, so the repo's clean domain graph is well supported. Leaving the learner model empty between sessions is not: every major tradition (overlay/knowledge tracing, constraint-based, Knowledge Space Theory, KLI) keeps durable per-learner state keyed to domain units. The literature does support the repo's distrust of a single scalar "mastery" number.

### Cited Findings

**The mainstream position: a domain model plus a persistent, evidence-derived learner model keyed to its units**
- The KLI framework defines its central unit, the knowledge component (KC), as "an acquired unit of cognitive function or structure that can be inferred from performance on a set of related tasks". KCs are a learner-side construct grounded in observed performance, and the term deliberately generalises "concept, principle, fact, or skill". — Koedinger, Corbett & Perfetti (2012), *Cognitive Science* 36(5):757–798, DOI 10.1111/j.1551-6709.2012.01245.x. [V-bib; definition wording V-snip] [DBLP record](https://dblp.org/rec/journals/cogsci/KoedingerCP12); [LearnLab KC page](https://learnlab.org/research/wiki/index.php/Knowledge_Component)
- KLI distinguishes three classes of learning event: memory and fluency processes, induction and refinement processes, and understanding and sense-making processes. The repo's "click" targets only the third. — Koedinger et al. (2012), same paper. [V-snip, from the authors' pre-publication draft] [draft PDF](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/TopicsInCognitiveScienceFall2011/KLI-paper-v5.00.pdf)
- Bayesian Knowledge Tracing is the canonical overlay learner model: for each rule or skill in the domain model the tutor keeps a probability that the learner is in the "learned" state, updated after every opportunity, and used to decide when to stop practising. — Corbett & Anderson (1995), *User Modeling and User-Adapted Interaction* 4:253–278, DOI 10.1007/BF01099821. [V-bib via Crossref] [Crossref record](https://api.crossref.org/works/10.1007/BF01099821)
- The two standard reviews of the field treat a persistent, per-skill learner model as the object of study; neither treats "no stored learner state" as a design option. — Desmarais & Baker (2012), *UMUAI* 22(1–2):9–38, DOI 10.1007/s11257-011-9106-8 [V-bib] [BibSonomy record](https://www.bibsonomy.org/bibtex/2b4231cdd3d096833f999cb1cf4bdc606/brusilovsky); Pelánek (2017), *UMUAI* 27:313–350, DOI 10.1007/s11257-017-9193-2 [V-bib] [Springer](https://link.springer.com/10.1007/s11257-017-9193-2), [author PDF](https://www.fi.muni.cz/~xpelanek/publications/umuai-overview.pdf)

**Perturbation / bug models: misconceptions as first-class domain-side objects**
- Brown and Burton modelled student errors in arithmetic as an executable procedural network containing correct sub-procedures and "buggy" variants, used both to diagnose students and to generate diagnostic tests. This is the origin of the bug-library approach. — Brown & Burton (1978), *Cognitive Science* 2:155–192, DOI 10.1207/s15516709cog0202_4. [V-bib] [record](https://www.bohrium.com/paper-details/diagnostic-models-for-procedural-bugs-in-basic-mathematical-skills/812131785361063937-7932)

**Constraint-based modelling: the closest precedent for a deliberately thin learner model**
- Ohlsson's constraint-based modelling represents subject matter as a set of state constraints, and the student model is the set of constraints the student has violated. It was proposed to avoid the intractability of full diagnosis, with no bug library and no runnable expert model needed. — Ohlsson (1994), in Greer & McCalla (eds.), *Student Modelling: The Key to Individualized Knowledge-Based Instruction*, NATO ASI Series 125, Springer, DOI 10.1007/978-3-662-03037-0_7. [V-bib] [Springer chapter](https://link.springer.com/doi/10.1007/978-3-662-03037-0_7)
- Even this minimal approach keeps a persistent per-learner record across sessions (constraint histories in SQL-Tutor and its siblings), and fifteen years of deployed tutors were built on it. — Mitrovic (2012), "Fifteen years of constraint-based tutors: what we have achieved and where we are going", *UMUAI* 22:39–72, DOI 10.1007/s11257-011-9105-9. [V-bib via Crossref] [Crossref record](https://api.crossref.org/works/10.1007/s11257-011-9105-9)
- Adding positive feedback (confirming tentative but correct steps) to SQL-Tutor led students to learn at roughly twice the speed of the error-feedback-only version. — Mitrovic, Ohlsson & Barrow (2013), *Computers & Education* 60(1):264–272, DOI 10.1016/j.compedu.2012.07.002. [V-snip from the repository abstract] [Lancaster ePrints](https://eprints.lancs.ac.uk/id/eprint/60011)

**Knowledge Space Theory / ALEKS: the learner state is a set of items, not a score**
- KST represents a learner by a knowledge state, the subset of domain items they can do, drawn from a family of feasible states closed under union. Its assessments are adaptive and produce "a more informative outcome than a numerical score". ALEKS, built on it, has been used by millions of students. — Doignon & Falmagne (1985), *International Journal of Man-Machine Studies* 23(2):175–196 [V-bib]; Doignon & Falmagne (2015), "Knowledge Spaces and Learning Spaces", arXiv:1511.06757 [V-full for the abstract; preprint of a handbook chapter] [arXiv](https://arxiv.org/abs/1511.06757)
- The "outer fringe" of a state is what the student is ready to learn next and the "inner fringe" is what they just learned. Both are computed from the stored state plus the prerequisite structure. — [Wikipedia, "Knowledge space"](https://en.wikipedia.org/wiki/Knowledge_space) (aggregator; it cites Doignon & Falmagne 1999, *Knowledge Spaces*, Springer, and Falmagne et al. 2013, *Knowledge Spaces: Applications in Education*, Springer) [V-snip]

**Support for the repo's suspicion of a mastery number**
- DeepTutor's authors argue explicitly against "coarse latent mastery scores" and instead keep an evidence-backed inventory of recurring confusions, wrong-answer patterns and active or resolved knowledge gaps. — Zhao et al. (2026), "DeepTutor: Towards Agentic Personalized Tutoring", arXiv:2604.26962 (v3, 9 Jul 2026). **Preprint; evaluated with LLM-simulated students and LLM judges.** [V-full] [arXiv](https://arxiv.org/html/2604.26962)
- People feel they understand explanatory, causal material "with far greater precision, coherence, and depth than they really do"; the illusion is stronger for explanatory knowledge than for facts, procedures or narratives. — Rozenblit & Keil (2002), *Cognitive Science* 26(5):521–562, DOI 10.1207/s15516709cog2605_1. [V-bib; finding V-snip] [record](https://www.bohrium.com/paper-details/the-misunderstood-limits-of-folk-science-an-illusion-of-explanatory-depth/812265652449443842-7932)

### Inferences
- The repo's graph is a domain model in the classical sense, and "presence ≠ held" is the correct reading of a domain model. The contradiction with the literature is narrower than it first looks: what is missing is an *overlay* file, not a change to the graph.
- The repo already produces overlay-shaped evidence (per-strand floor, ceiling and misconceptions in `grounding.md`; per-step check outcomes in `transcript.md`) and then strands it in prose that is not keyed to node ids. No tradition surveyed here discards that evidence between sessions.
- The design is internally inconsistent on this point. `graph-schema.md` says the graph is only "encountered domain structure", but the `grounding.md` template's "Prior graph" heading asks for "what the durable graph already suggested was held". A graph with no learner evidence cannot suggest that.
- KST's knowledge state is the closest formal match to the repo's "current understanding = set of propositions held as obviously true". A set of node ids with evidence pointers would be faithful to the repo's theory without becoming a gradebook.
- The repo's terminal condition ("the goal feels obviously true") is a self-report of understanding of explanatory material, which is exactly the judgement Rozenblit & Keil found inflated. The `theory.md` preference for apply/predict checks is the right counterweight, but only if the outcome of those checks, not the feeling, is what gets recorded.
- The Mitrovic et al. (2013) result suggests recording confirmations as well as repairs: a correct check answer is information, not just the absence of a problem.

### Gaps
- I could not confirm, in this session, primary sources for the term "overlay model" (usually attributed to Carr & Goldstein, 1977) or for Self's (1990) "Bypassing the intractable problem of student modelling" beyond a reference-list entry, so neither is cited as a finding.
- The exact KC definition is quoted from secondary reproductions; I did not open the published Wiley version.
- KST "surmise systems" (an item with several alternative prerequisite sets) are relevant to section 4, but I could not retrieve readable primary text defining them, so that mapping is stated only as an inference there.
- No source found tests a no-learner-state tutor against an overlay tutor head to head in open-ended conceptual tutoring.

---

## 2. Knowledge tracing: what minimal per-proposition evidence is worth storing, and what are the pitfalls?

### Takeaway
The evidence favours storing a small observation log (which unit, when, what kind of check, outcome, optionally confidence) and deriving any estimate at read time. Timestamps and outcomes carry real predictive value; fitted mastery probabilities are unjustified at n = 1 learner, and LLM-labelled dialogue evidence is noisy, especially at assigning turns to knowledge units.

### Cited Findings

**Classical knowledge tracing**
- BKT models each skill as a two-state (learned / unlearned) hidden variable with four parameters per skill: prior knowledge, learning rate, guess and slip. — Corbett & Anderson (1995), as above. [V-bib] [Crossref record](https://api.crossref.org/works/10.1007/BF01099821)
- Deep Knowledge Tracing replaced per-skill parameters with a recurrent network over the interaction sequence. — Piech et al. (2015), *Advances in Neural Information Processing Systems 28*, pp. 505–513. [V-snip]
- DKT's advantage does not come from discovering novel representations; BKT extended with a few features performs about as well while staying interpretable. — Khajah, Lindsey & Mozer (2016), "How Deep is Knowledge Tracing?", *Proc. EDM 2016*, pp. 94–101, arXiv:1604.02416. [V-snip] [arXiv](https://arxiv.org/abs/1604.02416)
- Across nine real-world datasets, logistic regression with the right features does best on datasets of moderate size or with very many interactions per student; DKT does best on large datasets or where precise temporal information matters; Markov-process methods such as BKT lag behind. The paper also examines calibration. — Gervet, Koedinger, Schneider & Mitchell (2020), *Journal of Educational Data Mining* 12(3):31–54. [V-snip from the journal abstract] [JEDM](https://jedm.educationaldatamining.org/index.php/JEDM/article/view/451)

**Timestamps and forgetting**
- Half-life regression predicts recall from the lag since last practice plus counts of past correct and incorrect attempts. On roughly 13 million Duolingo traces it cut prediction error by more than 45% against several baselines. — Settles & Meeder (2016), *Proc. ACL 2016*, pp. 1848–1858. [V-snip from the Anthology abstract] [ACL Anthology](https://aclanthology.org/P16-1174/)
- In a semester-long eighth-grade Spanish course, personalised review driven by a memory model plus each student's history gave a 16.5% boost in retention over massed study and 10% over a one-size-fits-all spaced schedule, on a cumulative exam about a month after the semester. — Lindsey, Shroyer, Pashler & Mozer (2014), *Psychological Science* 25(3):639–647, DOI 10.1177/0956797613504302. [V-snip] [author reprint](https://home.cs.colorado.edu/~mozer/Research/Selected%20Publications/reprints/LindseyShroyerPashlerMozer2014Published.pdf)

**Confidence**
- Errors committed with high confidence are more likely to be corrected at retest than low-confidence errors (the hypercorrection effect). — Butterfield & Metcalfe (2001), *Journal of Experimental Psychology: Learning, Memory, and Cognition* 27(6):1491–1494. [V-snip] [review in PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3970786)
- Feedback roughly doubled retention of correct answers given with low confidence, relative to no feedback; high-confidence correct answers were stable. — Butler, Karpicke & Roediger (2008), *JEP:LMC* 34(4):918–928. [V-snip from the abstract] [author PDF](https://pcllab.github.io/downloads/2008/2008_Butler_Karpicke_Roediger_JEPLMC.pdf)

**LLM-based knowledge tracing in dialogue (the repo's setting)**
- Scarlatos, Baker & Lan introduced dialogue knowledge tracing: GPT-4o labels each tutor–student turn pair with knowledge components and with whether the student responded correctly, and a KT model runs over those labels. — Scarlatos, Baker & Lan (2025), "Exploring Knowledge Tracing in Tutor-Student Dialogues using LLMs", *Proc. LAK 2025*; arXiv:2409.16490. [V-full] [arXiv](https://arxiv.org/html/2409.16490v2)
- Label quality in that study, rated by three former maths teachers on 30 dialogues (166 turn pairs): correctness labels scored 0.93/1, but KC labels scored 3.28/4 with only 0.35 annotator overlap. On final-turn correctness GPT-4o reached 75.8% accuracy against 85.6% for humans. **Small validation sample.** — same paper. [V-full] [arXiv](https://arxiv.org/html/2409.16490v2)
- Their LLM-based tracer beat the best classical baseline (AUC 65.8 vs 61.8 on CoMTA; 76.7 vs 66.2 on MathDial) but topped out near 76% AUC, below the 80%+ usual for standard KT. Stated obstacles: dialogues give about four labelled turn pairs each; 164 KCs over 623 turn pairs is too sparse; many student turns are irrelevant to KT; and students were not linked across dialogues. — same paper. [V-full] [arXiv](https://arxiv.org/html/2409.16490v2)
- TutorLLM feeds a BERT-based KT model's predicted learning state into a RAG tutor. A two-week crossover study with 30 undergraduates reported a 5% quiz-score improvement and a 10% usability gain over a general LLM. **Preprint; small-N; short duration.** — Li et al. (2025), arXiv:2502.15709. [V-snip from the arXiv abstract] [arXiv](https://arxiv.org/abs/2502.15709)
- LongTutor (built from expert-annotated real-world learning logs) finds that LLMs "excel at evidence acquisition" from a long student history but "struggle to effectively leverage long-term history for accurate diagnosis and adaptive teaching". — Li, Zhang, Huang, Li, Zhan, Luo, Liu & Chen (2026), *Proc. ACL 2026 (Long Papers)*, pp. 29712–29737. [V-snip from the Anthology abstract] [ACL Anthology](https://aclanthology.org/2026.acl-long.1371/)

### Inferences
- **What to store.** A per-observation record of roughly `{nodeId or chainId, sessionId, step, at, kind, outcome, confidence?}`, where `kind` separates grounding probes from teaching checks and recall/parrot from apply/predict, and `outcome` is a small enum (for example `held`, `repaired`, `missed`, `asserted-unprobed`). Timestamps, attempt outcomes and counts are exactly the inputs the retention and KT models above consume.
- **What not to store.** A fitted `p(mastery)`. BKT, logistic and deep models are fitted on populations; one learner with a handful of observations per proposition cannot support parameter estimation, and Scarlatos et al. show sparsity already defeats KT at 623 turn pairs. Store raw observations and let a reader derive "last seen held, n days ago".
- **Raw log over summary.** LongTutor's finding implies the next session's agent can find evidence in a log but is unreliable at inferring state from long unstructured history. That argues for a small, structured, node-keyed log over asking `learning-ground` to re-read old transcripts.
- **Pitfall: attribution.** Assigning a dialogue turn to the right knowledge unit is the weak step (0.35 annotator overlap), not judging correctness. The repo is well placed to avoid this: `learning-teach` knows which step it is checking when it asks, so the link should be written at check time rather than inferred after the fact by `learning-graph`.
- **Pitfall: in-session checks overstate durable knowledge.** A check passed seconds after the explanation is the massed condition in Lindsey et al.; it is weak evidence of retention. The probe at the start of the next session is the more valuable observation, and today it is the one the repo is least likely to key to a node.
- **Confidence is cheap and useful.** A one-word confidence on check answers lets the tutor distinguish high-confidence errors (candidate misconceptions, and readily corrected) from low-confidence correct answers (which most need confirmation).
- "Re-probe from scratch" is defensible as a policy of never trusting old evidence without a fresh check. It is not defensible as a policy of not *using* old evidence to choose what to probe; with dated outcomes the probe can target stale or previously repaired nodes first.

### Gaps
- No study found estimates how many dialogue observations per proposition are needed before a per-learner estimate is useful in open-ended conceptual tutoring.
- The retention evidence above is from paired-associate and vocabulary learning. I found no comparable forgetting-curve evidence for explanatory, derivation-style understanding of the kind the repo targets.
- I could not verify primary sources in this session for BKT identifiability problems, contextual guess/slip, Learning Factors Analysis or Performance Factors Analysis, so they are not cited.
- The TASA and AgentTutor systems (forgetting curves over knowledge tracing; learner-profile lifecycles) surfaced only in a search summary of a survey; I could not confirm them in a primary source.

---

## 3. Open learner models: does inspectability help, and what does that say about plain-text, git-tracked storage?

### Takeaway
There is moderate evidence, including classroom experiments, that showing learners their own model improves self-assessment and can improve domain learning, with the benefit strongest when the learner actively engages with the model. Plain-text git storage is a good substrate for this, but the repo currently has no learner model to open: the inspectable artifact is a domain graph.

### Cited Findings
- The SMILI framework characterises an open learner model (OLM) by what is open, how it is presented, who controls it and for what purpose (purposes include promoting reflection, supporting planning and monitoring, improving the accuracy of the model, and learner control and trust). — Bull & Kay (2007), "Student Models that Invite the Learner In: The SMILI Open Learner Modelling Framework", *IJAIED* 17(2):89–120 [V-bib] [Birmingham record](https://research.birmingham.ac.uk/en/publications/student-models-that-invite-the-learner-in-the-smili-open-learner-); Bull & Kay (2016), "SMILI☺: a Framework for Interfaces to Learning Data in Open Learner Models, Learning Analytics and Related Fields", *IJAIED* 26(1):293–331, DOI 10.1007/s40593-015-0090-8 [V-bib; one repository lists the volume as 29, DBLP and Springer give 26] [Springer](https://link.springer.com/doi/10.1007/s40593-015-0090-8)
- In two constraint-based tutors (SQL-Tutor and KERMIT), even simple open student models helped learning and metacognitive skills, with less able students gaining most. — Mitrovic & Martin (2007), "Evaluating the Effect of Open Student Models on Self-Assessment", *IJAIED* 17(2):121–144. [V-snip from the repository abstract] [Canterbury repository](https://ir.canterbury.ac.nz/handle/10092/2442)
- Two in-vivo classroom experiments with a linear-equation tutor tested whether an OLM improves domain-level learning through self-regulation support; outcomes included equation-solving, self-assessment accuracy and problem-selection decisions. The authors conclude an OLM is especially effective when designed to support multiple self-regulated-learning processes (in their design, prompted self-assessment alongside the displayed model). — Long & Aleven (2017), *UMUAI* 27(1):55–88, DOI 10.1007/s11257-016-9186-6. [V-bib; conclusion V-snip] [Springer](https://link.springer.com/doi/10.1007/s11257-016-9186-6)
- A systematic review found OLMs used to support self-regulated learning in higher education. — Hooshyar, Pedaste, Saks, Leijen, Bardone & Wang (2020), *Computers & Education* 154:103878. [V-bib] [DBLP](https://dblp.org/rec/journals/ce/HooshyarPSLBW20)
- A systematic review comparing the OLM literature with learner-facing analytics dashboards reported that 37% of OLMs have complex models and just 6% involve multiple applications. — Bodily, Kay, Aleven, Jivet, Davis, Xhakaj & Verbert (2018), *Proc. LAK '18*, pp. 41–50. [V-snip; the search returned two different DOIs, 10.1145/3170358.3170409 and …3170421, so I link the repository record] [TU Delft repository](https://repository.tudelft.nl/record/uuid:6ddc2565-0cd8-42a9-b09b-6ef40ba143c3)
- Kay's lifelong learner model is framed as an independent entity controlled by the learner, with learner control and privacy handled at the learner–model interface. — Kay (2008), "Lifelong Learner Modeling for Lifelong Personalized Pervasive Learning", *IEEE Transactions on Learning Technologies* 1(4):215–228, DOI 10.1109/TLT.2009.9. [V-bib; one index dates it 2009] [BibSonomy](https://www.bibsonomy.org/bibtex/2e438d532186661c8318014562047b8d4/brusilovsky)
- OLM research is offered as a starting framework for interpretable AI in education generally. — Conati, Porayska-Pomsta & Mavrikis (2018), "AI in Education needs interpretable machine learning: Lessons from Open Learner Modelling", ICML Workshop on Human Interpretability in ML, arXiv:1807.00154. **Workshop position paper.** [V-bib] [arXiv](https://arxiv.org/abs/1807.00154v1)
- A 2026 meta-synthesis of 26 studies proposes a continuum of OLM types: inspectable, negotiable, editable and persuasive/adaptive. — *Frontiers in Education* (2026), DOI 10.3389/feduc.2025.1760183. [V-snip; authors not confirmed] [Frontiers](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1760183/full)
- In the LLM era, LOOM's learners could see their memory graph but "cannot directly manipulate or extend the structure itself"; participants asked for more consistency and control, and the authors flag that the system can overgeneralise what a learner knows from a single interaction. — Cui, Pu & Grossman (2025), "LOOM", arXiv:2511.21037, PerFM Workshop at AAAI 2026. **Workshop preprint; formative study, N = 10 convenience sample over two days.** [V-full] [arXiv](https://arxiv.org/html/2511.21037)

### Inferences
- Plain text in git gives the repo three SMILI properties for free: the model is inspectable (a text file), editable (the learner can change it) and its history is auditable (`git log`, `git blame`). That exceeds what most OLM systems in the reviews offer, and it matches Kay's learner-controlled lifelong model.
- The benefit in the experimental studies came from learners *engaging* with a model of themselves (self-assessing, comparing their estimate with the system's). A JSONL file of propositions that the learner never looks at delivers none of this. The human-readable `extraction.md` is the natural place to surface it.
- An "editable" or "negotiated" model maps directly onto the repo's workflow: before folding a session, show the learner which propositions will be marked held and let them contest it. That is also a cheap accuracy check on LLM extraction (section 4) and the control LOOM's participants asked for.
- The repo's "not a gradebook" stance is compatible with OLM practice. OLMs need not be scores: Mitrovic & Martin's models were simple, and SMILI treats the form of presentation as a design choice.

### Gaps
- I did not find a quantitative meta-analysis of OLM effects on learning; the evidence is individual experiments plus systematic reviews and a meta-synthesis. Effect sizes for Long & Aleven were not retrieved.
- No study found evaluates an OLM stored as learner-owned plain text under version control, or an OLM in a 1:1 LLM chat tutor with real learners over multiple sessions.
- Evidence for learner-*editable* (as opposed to inspectable) models was not retrieved from primary sources in this session.

---

## 4. Granularity and representation: propositions, concepts, skills, hyperedges, LLM-extracted graphs, misconception libraries

### Takeaway
Self-contained propositions are a defensible unit and joint-premise hyperedges preserve structure that pairwise prerequisite graphs lose. The weak points are the ones the repo leaves unguarded: LLM extraction and entity resolution are documented error sources, granularity is unstable across runs and models, and the repo has no way to detect, merge or correct the resulting nodes. Misconceptions are treated as first-class objects in the literature and are absent from the repo's durable store.

### Cited Findings

**Units of knowledge**
- KLI treats the knowledge component as a deliberately general unit covering facts, concepts, principles and skills, validated by whether it explains performance across related tasks. — Koedinger et al. (2012), as above. [V-snip] [LearnLab KC page](https://learnlab.org/research/wiki/index.php/Knowledge_Component)
- For retrieval, indexing a corpus by "propositions" (atomic, self-contained factual statements) outperformed passage- or sentence-level indexing for retrieval and downstream QA under a fixed token budget. — Chen et al. (2023), "Dense X Retrieval: What Retrieval Granularity Should We Use?", arXiv:2312.06648 (v3, Oct 2024). **Preprint as retrieved; an IR result, not a learning result.** [V-snip from the arXiv abstract] [arXiv](https://arxiv.org/abs/2312.06648)

**Concept maps and argument maps**
- Learning with concept and knowledge maps has a moderate positive effect (g = 0.58; 142 independent effect sizes, n = 11,814). Constructing maps (g = 0.72) helps more than studying them (g = 0.43). — Schroeder, Nesbit, Anguiano & Adesope (2018), "Studying and Constructing Concept Maps: a Meta-Analysis", *Educational Psychology Review* 30(2):431–455, DOI 10.1007/s10648-017-9403-9. [V-snip from the abstract] [SFU Summit record](https://summit.sfu.ca/item/17789)
- High-intensity argument-mapping courses are reported to raise critical-thinking scores by about 0.8 SD, roughly twice the typical critical-thinking course. — van Gelder (2015), "Using argument mapping to improve critical thinking skills", in Davies & Barnett (eds.), *The Palgrave Handbook of Critical Thinking in Higher Education*. **Handbook chapter by an argument-mapping proponent; the figure reached me via secondary quotation, and a 2025 *Frontiers in Education* paper describes robust evidence for argument-visualisation tools as scarce.** [V-snip] [author PDF](https://www.reasoninglab.com/wp-content/uploads/2013/10/TvG-Using-argument-mapping-to-improve-critical-thinking-skills-2015.pdf)

**Prerequisite structure**
- KST derives its feasible knowledge states from prerequisite structure among items, built by querying experts or mining response data; simulation work has examined how expert errors propagate into the resulting structure. — [Wikipedia, "Knowledge space"](https://en.wikipedia.org/wiki/Knowledge_space) (aggregator), citing Koppen & Doignon (1990), *Journal of Mathematical Psychology* 34(3):311–331, and Schrepp & Held (1995), *Journal of Mathematical Psychology* 39(4):376–382. [V-snip]

**LLM-extracted educational knowledge graphs: accuracy and entity resolution**
- A study of GPT-3.5, GPT-4o-mini and GPT-4o on concept generation, concept extraction and prerequisite-relation identification, scored by automated metrics plus four domain experts, concludes LLMs are viable for this but reports that the models are cautious in asserting prerequisite relations, which limits completeness. It includes a failure-type analysis over 3,318 errors. — Yang, Ren, Gu, He, Ma & Konomi (2025), *Machine Learning and Knowledge Extraction* 7(3):103, DOI 10.3390/make7030103; preprint arXiv:2504.08856. [V-bib; findings V-snip, the publisher page returned 403] [DBLP](https://dblp.org/rec/journals/make/YangRGHMK25.html)
- An LLM pipeline for course knowledge–competency graphs reached entity-extraction accuracy of up to 87.92%; the authors describe granularity as an unresolved two-way bias in which apparent over-extraction can reflect a mismatch between model interpretation and task granularity. — "LLM-Powered Construction of Course Knowledge-Competency Graphs", ACM, DOI 10.1145/3766557.3766569. [V-snip; authors and venue not confirmed] [ACM DL](https://dl.acm.org/doi/10.1145/3766557.3766569)
- Graphusion builds an educational (NLP-course) knowledge graph in three stages: seed concepts, candidate triplet extraction, then a fusion stage that performs entity merging, conflict resolution and novel triplet discovery. Removing fusion noticeably hurts performance. — Yang et al. (2024), arXiv:2407.10794. **Preprint.** [V-snip from the arXiv abstract] [arXiv](https://arxiv.org/abs/2407.10794)
- In incremental LLM graph construction, entity and relation resolution "becomes crucial" for consistency as inputs grow. — iText2KG, arXiv:2409.03284. **Preprint.** [V-snip] [arXiv](https://arxiv.org/pdf/2409.03284)
- LLM-extracted graph elements show high coverage and low accuracy; adding an LLM judging step raised precision on retained triples. — "Can LLMs be Good Graph Judge for Knowledge Graph Construction?", arXiv:2411.17388. **Preprint.** [V-snip] [arXiv](https://arxiv.org/pdf/2411.17388)
- A production agent-memory graph resolves entities in three steps (embedding similarity, full-text search over names and summaries, then an LLM judgment over the candidates) rather than by LLM judgment over the whole store. — Rasmussen, Paliychuk, Beauvais, Ryan & Chalef (2025), "Zep: A Temporal Knowledge Graph Architecture for Agent Memory", arXiv:2501.13956. **Vendor preprint.** [V-full] [arXiv](https://arxiv.org/html/2501.13956)

**Misconception libraries as first-class objects**
- Bug libraries date from Brown & Burton (1978), cited in section 1. [V-bib]
- Eedi's 2024 Kaggle competition "Mining Misconceptions in Mathematics" asked systems to rank a curated library of about 2,587 named misconceptions against each wrong answer (MAP@25). A medal-winning solution scored about 0.50–0.54. — [Eedi write-up](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions). **Company blog; library size and scores from third-party write-ups.** [V-snip]
- LLMs have been evaluated on misconception reasoning using Eedi data, including the task of answering incorrectly in the way a specific misconception predicts. — "Novice Learner and Expert Tutor: Evaluating Math Reasoning Abilities of Large Language Models with Misconceptions", arXiv:2310.02439. **Preprint.** [V-snip] [arXiv](https://arxiv.org/pdf/2310.02439)
- DeepTutor's learner profile makes "recurring confusions, wrong-answer patterns, and active or resolved knowledge gaps" an explicit, evidence-backed component. — Zhao et al. (2026), as above. **Preprint.** [V-full] [arXiv](https://arxiv.org/html/2604.26962)

### Inferences
- **Propositions.** A proposition is a legitimate KC under KLI and the unit Dense X favours for retrieval, so the choice is supported. The risk is in the repo's own example: the "Primary key" statement bundles a premise, an inference and a definition into one node, which makes link-or-create ambiguous and hides a chain inside a node. A stated atomicity rule (one claim per node; "because" belongs in a chain) would reduce the granularity instability the extraction papers report.
- **Hyperedges.** I found no direct evidence comparing joint-premise hyperedges with pairwise edges for learning. The support is structural: KST allows an item to have several alternative prerequisite sets, which is the same shape as several chains sharing a conclusion, and argument-mapping practice distinguishes premises that work jointly from those that work independently. The repo's rule that two chains with the same conclusion are different arguments is consistent with both.
- **Two graphs that never meet.** `plan.md` holds a pairwise prerequisite map over slugs; the durable graph holds chains over node ids. Nothing links a plan slug to the nodes it produced, so the plan's prerequisite judgments (the thing KST would use to compute a fringe) are lost at extraction.
- **Construction beats study.** Schroeder et al. found constructing maps more effective than studying them. In this repo the LLM constructs and the learner, at most, reads. Having the learner state or confirm a chain's premises before it is written is the cheap way to capture the larger effect.
- **Entity resolution.** "LLM judgment against the full statement text" has no candidate-generation step, no recorded decision and no review. Every source above that builds graphs incrementally adds an explicit resolution or fusion stage, and Zep narrows candidates before asking the LLM. As `nodes.jsonl` grows past what fits comfortably in context, silent duplicates and wrong merges should be expected. First-write-wins then makes a wrong merge permanent.
- **Extraction from teacher prose only.** This is a sound choice for keeping learner errors out of the domain model, but it makes the graph exactly as accurate as the LLM teacher, with no source grounding. A proposition's provenance points to `transcript.md`, that is, to the same model's own output.
- **Misconceptions.** The repo records them per strand in `grounding.md` and then drops them. The literature treats them as reusable, nameable objects linked to the correct knowledge they compete with.

### Gaps
- No error-rate study found for LLM extraction of *propositions and argument chains* from tutoring dialogue. The numbers above are for concept and prerequisite extraction from course materials, a related but easier task.
- No empirical comparison found of hypergraph versus pairwise representations for tutoring or learner modelling.
- The 3,318-error breakdown in Yang et al. (2025) could not be retrieved, so I cannot say what share of errors were granularity, hallucination or resolution.
- I could not verify a primary source for Novak's concept-mapping theory in this session, so it is not cited; the Schroeder et al. meta-analysis stands in for the evidence.
- I did not confirm the Cullen et al. (2018) argument-mapping study, so the argument-mapping evidence rests on one proponent-authored chapter and should be treated as weak.

---

## 5. Belief revision and provenance: wrong or superseded content, and durable storage of learner misconceptions

### Takeaway
Append-only storage with provenance is consistent with good practice, but practice pairs it with an explicit way to supersede or invalidate a record; the repo has none. On misconceptions the cognitive evidence is fairly clear: prior misconceptions persist after instruction and are best addressed by explicit refutation, which argues for storing them durably and linked to the propositions they contradict.

### Cited Findings

**How systems handle superseded content**
- Zep/Graphiti keeps each fact edge on two timelines: when the fact was true (`t_valid`, `t_invalid`) and when the system recorded or expired it (`t'_created`, `t'_expired`). When a new edge contradicts an existing one, the older edge's `t_invalid` is set rather than the edge being deleted. Raw inputs ("episodes") are a "non-lossy data store from which semantic entities and relations are extracted", with bidirectional links so any fact can be traced to its source. — Rasmussen et al. (2025), arXiv:2501.13956. **Vendor preprint.** [V-full] [arXiv](https://arxiv.org/html/2501.13956)
- A 2026 survey of persistent agent memory lists "provenance preservation" and "rollback traceability" among the invariants a memory lifecycle should maintain, warns that "Stale memory can override fresh observation because nothing marks it as expired", and observes that few systems validate writes at promotion time. — Ding, Nannapaneni, Liu & Zhang (2026), "Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents", arXiv:2606.30306. **Preprint.** [V-full for these general claims] [arXiv](https://arxiv.org/html/2606.30306v1)
- A search summary of the same survey attributes to it the claim that the learner model is the most sensitive long-horizon record and the least governed. I could not locate that passage in the text I retrieved. [V-snip, unconfirmed] [arXiv](https://arxiv.org/html/2606.30306v1)
- DeepTutor's consolidation writes a timestamped session-log entry and overwrites a concise learner profile whose gaps carry an active or resolved status. — Zhao et al. (2026), as above. **Preprint.** [V-full] [arXiv](https://arxiv.org/html/2604.26962)
- Graphusion's fusion stage includes explicit conflict resolution between extracted triples. — Yang et al. (2024), as above. **Preprint.** [V-snip] [arXiv](https://arxiv.org/abs/2407.10794)

**Misconceptions persist and respond to explicit refutation**
- Across ten domains of science, adults were slower and less accurate at verifying statements whose truth value differs between naive and scientific theories; the authors conclude naive theories "are suppressed by scientific theories but not supplanted by them". — Shtulman & Valcarcel (2012), *Cognition* 124(2):209–215. [V-bib; finding V-snip; DOI not confirmed] [PhilArchive record](https://dc2.philarchive.org/rec/SHTSKS)
- Chi distinguishes kinds of conceptual change (belief revision, mental-model transformation, categorical shift); false beliefs at the single-proposition level can be corrected by explicit contradiction and refutation, while misconceptions rooted in a wrong category are far more robust. — Chi (2008), "Three types of conceptual change: Belief revision, mental model transformation, and categorical shift", in Vosniadou (ed.), *International Handbook of Research on Conceptual Change*, Routledge, pp. 61–82. [V-bib; summary V-snip via a secondary source] [author PDF](https://www.public.asu.edu/~mtchi/papers/Chi_concpetualchangechapter.pdf)
- Refutation text (which states a misconception, says it is wrong and explains why) has a positive, moderate effect on learning against other conditions: g = 0.41 over 44 independent comparisons, n = 3,869. — *Educational Psychology Review*, DOI 10.1007/s10648-021-09656-z. [V-snip; I believe the authors are Schroeder & Kucera but did not confirm this in session] [Springer](https://link.springer.com/article/10.1007/s10648-021-09656-z)
- A pre-registered meta-analysis in *Educational Psychologist* also compares refutation with non-refutation texts. — Danielson et al. (2024). [V-snip; details not retrieved]
- High-confidence errors are the most readily corrected when feedback is given. — Butterfield & Metcalfe (2001), as in section 2. [V-snip]

### Inferences
- **Keep append-only, add supersession.** Append-only JSONL plus git already gives the transaction timeline (when a line was written). What is missing is the valid timeline: a way to say "this node or chain is retracted, or superseded by that one". Because the merge is "first line wins", a later line cannot even correct a typo in a `statement`; the correction is demoted to an alias. A tombstone-style line (`supersedes` or `retractedAt` with a reason and provenance), honoured by `merge_graph.py`, keeps the append-only property and fixes this.
- **This matters more here than in most systems** because the only source of propositions is an LLM teacher. A hallucinated or over-simplified claim, once extracted, is then "pre-read" by the next session as established domain structure. The survey's stale-memory warning describes this exact failure.
- **The template's "one true claim" assumption is domain-bound.** The repo's active session is on Heidegger. In interpretive domains a proposition is true *according to* a text or reading, and rival chains to incompatible conclusions are normal. A node needs a way to carry attribution or scope, and the graph needs a "contradicts" relation, or first-write-wins will silently pick a side.
- **Store misconceptions durably.** Shtulman & Valcarcel imply a repaired misconception is suppressed, not gone, so it is a standing prediction about where this learner will slip again. Refutation needs the misconception stated explicitly, so the tutor benefits from having it on file. The natural shape: a learner-side record with the misconception's statement, the node(s) it contradicts, when it was observed, when it was repaired, and status.
- **Keep them out of `nodes.jsonl`.** The repo's rule that the graph holds only teacher-asserted claims is right; a false statement in the domain graph would be read as true. A separate file (or a `kind` the pre-read treats differently) preserves the separation.
- Chi's distinction suggests tagging a misconception's depth is worthwhile: a false belief needs one refutation, while a wrong mental model predicts repeated failures across many nodes and should shape the next plan.

### Gaps
- I found no education-specific study of retraction or supersession mechanisms in tutoring knowledge bases. The engineering evidence is from general agent-memory preprints, one of them vendor-authored.
- I did not verify primary sources on formal belief-revision theory (AGM) or truth-maintenance systems, so neither is cited.
- No source found measures how often an LLM tutor's own explanations contain errors that would be frozen into such a graph.
- Whether durably storing a learner's misconceptions risks anchoring the tutor on an outdated picture of the learner is not addressed in anything I found. LOOM's overgeneralisation observation is the nearest signal.

---

## 6. LLM tutors with persistent memory across sessions (2023–2026): what structures do they use?

### Takeaway
Published systems converge on a layered design: a non-lossy episodic log, a distilled and regularly rewritten learner profile, and a separate content knowledge base or graph. None of those found omits per-learner state as this repo does. The evidence base is weak (preprints, simulated students, LLM judges, N ≤ 30), and the best benchmarks find that sustaining good tutoring over a long horizon is unsolved.

### Cited Findings
- **DeepTutor** separates "Static Knowledge Grounding" (source documents split into atomic content units with a knowledge graph over them) from "Dynamic Personal Memory": a multi-level, searchable trace of every session plus a distilled profile with three parts (session history and performance trends; an evidence-backed inventory of confusions and active/resolved gaps; pedagogical self-reflections). The knowledge graph covers course content, not the learner. Ablation: removing learner memory hurts personalisation most. Evaluation: 270 tasks over 90 simulated learner profiles, Gemini student simulator, Claude judge; human check on 45 sessions (r = 0.82 with the judge). — Zhao, Zhang, Ren, Guo, Chu, Ma & Huang (2026), arXiv:2604.26962. **Preprint; the authors state human-student validation is still needed.** [V-full] [arXiv](https://arxiv.org/html/2604.26962)
- **LOOM** builds a "learner memory graph" from the learner's everyday LLM chats. In the prototype it is a simple two-level graph linking goals to courses with per-module completion; completed courses are "concrete evidence of mastery". There are no prerequisite edges and no decay. Learners cannot edit the structure. — Cui, Pu & Grossman (2025), arXiv:2511.21037. **Workshop preprint; N = 10 formative study.** [V-full] [arXiv](https://arxiv.org/html/2511.21037)
- **TutorLLM** keeps the learner state inside a trained KT model and passes its predictions to a RAG tutor. — Li et al. (2025), arXiv:2502.15709. **Preprint; N = 30, two weeks.** [V-snip] [arXiv](https://arxiv.org/abs/2502.15709)
- **Dialogue KT** (Scarlatos et al., LAK 2025) is within-dialogue only and explicitly does not link students across dialogues. [V-full] [arXiv](https://arxiv.org/html/2409.16490v2)
- **LongTutor** benchmarks LLMs on long real-world learning logs across historical evidence acquisition, knowledge-state diagnosis and adaptive teaching action; models are strong at the first and weak at the other two. — Li et al. (2026), *Proc. ACL 2026*. [V-snip] [ACL Anthology](https://aclanthology.org/2026.acl-long.1371/)
- **EduClaw-Bench** puts agent tutors in a continuous 30-day relationship with a KT-grounded simulated learner over 55 scenarios and ten agent configurations; "almost no combination sustains good tutoring over the full horizon", and quality depends on the base model and the agent harness together. — Lee, Lee, Jeong, Lee, Shin & Kwon (2026), arXiv:2608.03206. **Preprint; simulated learners, LLM judges for some axes.** [V-full for the abstract] [arXiv](https://arxiv.org/abs/2608.03206)
- **General agent memory**: Zep/Graphiti (episodes, then an entity graph with bi-temporal fact edges) is the clearest published description of a temporal knowledge graph used as agent memory. — Rasmussen et al. (2025), arXiv:2501.13956. **Vendor preprint; benchmark claims are contested between vendors.** [V-full] [arXiv](https://arxiv.org/html/2501.13956)

### Inferences
- The repo already has two of the three layers: a non-lossy episodic store (`transcript.md`, `grounding.md`, kept in git) and a content graph. It lacks the middle layer, a distilled learner profile that is rewritten each session and points back to evidence.
- The repo's content graph is richer than any found in these systems: none stores joint-premise argument chains. That is a genuine differentiator, and unevaluated.
- Its storage is more transparent than any of them. DeepTutor does not specify a format, LOOM's graph is not editable, TutorLLM's state is inside a neural model. Plain JSONL and markdown in git satisfy the survey's provenance and rollback invariants almost by default.
- DeepTutor's "active/resolved gap with evidence" entry is the best available template for a learner record that respects the repo's "not a gradebook" rule.
- LongTutor and EduClaw-Bench both indicate that handing an LLM a long raw history does not yield good diagnosis or sustained adaptation. That weakens the case for relying on re-reading old session folders and strengthens the case for a compact, structured carry-over file. It equally weakens any assumption that adding memory will by itself make later sessions better; the repo's fresh probe remains necessary.

### Gaps
- I found no peer-reviewed study of an LLM tutor with persistent cross-session memory evaluated on real learners' learning outcomes over more than two weeks. A follow-up search aimed at exactly this returned only simulated-learner work.
- No published system found stores tutor memory as learner-owned plain text under version control, or as a proposition-plus-hyperedge graph, so there is no direct comparator for this repo's design.
- MemGPT and Mem0 were not verified in primary sources and are not cited.
- This area moves monthly; several items above are first-version preprints from mid-2026 and may change.

---

## 7. Evidence-linked implications for this repo's schema and files

### Takeaway
Keep the domain graph, its hyperedges, its plain-text git storage and its fresh probe. Add a small learner-side evidence log keyed to node ids, a durable misconception record, a supersession mechanism, and an auditable link-or-create step. Do not add mastery scores.

### Cited Findings
Each item names the supporting finding from sections 1–6; citations are given there.

**Keep (the evidence supports the current design)**
1. **A domain graph with no learner state on its nodes.** Domain/learner separation is standard (Corbett & Anderson 1995; Desmarais & Baker 2012; Doignon & Falmagne 1985), and DeepTutor keeps its knowledge graph content-only. Keep the "do not store mastery on nodes" rule in `graph-schema.md`.
2. **No scalar mastery or fitted probability.** One learner and a few observations per proposition cannot support KT parameter fitting (sparsity failures in Scarlatos et al. 2025; model-family dependence on data volume in Gervet et al. 2020); DeepTutor argues against coarse mastery scores.
3. **Joint-premise chains, and multiple chains per conclusion.** Consistent with KST's alternative prerequisite sets and with argument-mapping practice; no contrary evidence found (and no direct supporting experiment either).
4. **Propositions as the unit.** Compatible with KLI's knowledge component and with Dense X's retrieval result.
5. **Plain text, append-only, git-tracked.** Delivers inspectability and learner control (Bull & Kay 2007/2016; Kay 2008) and the provenance and rollback invariants of Ding et al. (2026).
6. **Probing at the start of each session.** A delayed probe is stronger evidence than an in-session check (Lindsey et al. 2014; Settles & Meeder 2016), and LLMs are weak at diagnosing state from history alone (LongTutor 2026). Keep the probe; change what it is aimed at (item 8).
7. **Extracting graph content from teacher prose only.** Keeps learner errors out of the domain model, in line with bug-library practice of holding misconceptions as separate objects (Brown & Burton 1978).

**Add**
8. **A learner evidence log, separate from the graph**, for example `.learning/learner/observations.jsonl`, append-only, one line per check or probe: `{nodeId|chainId, sessionId, step, at, kind: probe|check, form: recall|apply|predict, outcome: held|repaired|missed, confidence?}`. Supported by overlay modelling generally; by timestamps and outcome counts being the predictive features in Settles & Meeder (2016) and Lindsey et al. (2014); by KST's state-as-a-set; by DeepTutor's evidence-backed gaps. `learning-ground` then uses it to order the probe (stale, previously repaired or never-probed nodes first) and to fill "Prior graph" honestly.
9. **Write the node link at check time in `learning-teach`**, not by inference in `learning-graph`. KC attribution is the unreliable step in LLM dialogue annotation (0.35 annotator overlap, Scarlatos et al. 2025), whereas the teaching skill knows which step it is checking. Practically: carry the plan slug in each `## Step:` heading (already the convention) and have `learning-graph` record slug → node ids in `extraction.md`.
10. **Optional one-word confidence on check answers.** High-confidence errors flag misconceptions and correct readily (Butterfield & Metcalfe 2001); low-confidence correct answers benefit most from confirmation (Butler, Karpicke & Roediger 2008).
11. **Record confirmations, not only repairs.** Positive feedback on correct steps doubled learning speed in SQL-Tutor (Mitrovic, Ohlsson & Barrow 2013).
12. **A durable misconception record**, for example `.learning/learner/misconceptions.jsonl`: `{id, statement, contradicts: [nodeId], observedAt, sessionId, status: active|repaired, repairedAt?, depth: belief|model?}`. Supported by persistence of prior conceptions (Shtulman & Valcarcel 2012), the refutation-text effect (g = 0.41), Chi (2008) on kinds of conceptual change, bug libraries (Brown & Burton 1978), the Eedi library, and DeepTutor's profile. Keep it out of `nodes.jsonl`.
13. **Supersession and retraction in the graph.** Allow a later line to carry `supersedes: <id>` or `retracted: {at, reason, provenance}`, honoured by `merge_graph.py`, and add a `contradicts` relation. Supported by Zep's bi-temporal invalidation, the stale-memory warning and rollback invariant in Ding et al. (2026), and Graphusion's conflict-resolution stage. Without it an LLM teacher's error is permanent and is pre-read as fact.
14. **An auditable link-or-create step.** Generate candidates cheaply (lexical or embedding match over `name`, `statement`, `aliases`) before the LLM judges, and log each decision with the candidates considered in `extraction.md`. Supported by Zep's three-step resolution, iText2KG, the judge step in arXiv:2411.17388, and Graphusion's fusion ablation. Add a periodic duplicate-review pass, since the reported concept-extraction accuracy tops out near 88% on an easier task.
15. **A learner confirmation step before the merge.** Show the learner the proposed propositions and chains and what will be logged as held, and let them contest it. Supported by OLM evidence on self-assessment (Mitrovic & Martin 2007; Long & Aleven 2017), by constructing maps beating studying them (Schroeder et al. 2018), and by LOOM participants' request for control.

**Change**
16. **Fix the "Prior graph" wording in `folder-layout.md`.** It asks what the graph "suggested was held", which contradicts "presence ≠ held". With item 8 it can read from the evidence log; without it, it should say "encountered", as `graph-schema.md` does.
17. **State an atomicity rule for `statement`.** One claim per node; a "because" belongs in a chain. The schema's own "Primary key" example bundles premises and a conclusion. Supported by the granularity instability reported for LLM extraction (ACM course-graph paper; Yang et al. 2025) and by the Dense X definition of a proposition as atomic.
18. **Soften "one true claim" for interpretive domains.** Allow attribution or scope on a node (true according to which text or reading) so rival readings are not forced through first-write-wins. Supported by Chi's (2008) distinction between belief-level and model-level change; this is otherwise my inference from the active Heidegger session, with no direct study.
19. **Preserve the plan's prerequisite judgments.** Link `plan.md` slugs to node ids at extraction so prerequisite structure accumulates across sessions instead of being redrawn each time. Supported by KST's use of prerequisite structure to compute what a learner is ready to learn.
20. **Weight the terminal condition toward demonstrated outcomes.** "Feels obviously true" is vulnerable to the illusion of explanatory depth (Rozenblit & Keil 2002). Log the apply/predict outcome as the evidence and treat the feeling as a secondary note.

### Inferences
- The smallest change set with the most support is items 8, 12 and 13: two new append-only files and one merge rule. Together they close the gap with the learner-modelling literature without touching the graph's "not a gradebook" character.
- Items 14 and 13 matter more as the graph grows. At today's size (one session) duplicates and wrong merges are unlikely to have occurred yet, so this is the cheap moment to add the audit trail.
- Nothing here is validated for this design. The classical evidence comes from structured-problem tutors and paired-associate learning; the LLM-era evidence is mostly preprints with simulated learners. The recommendations are best read as "consistent with the evidence", not "shown to work in a 1:1 LLM chat tutor".

### Gaps
- No direct evaluation exists of any of these changes in a chat-based LLM tutor with a single real learner. Whether a node-keyed evidence log actually improves the next session's probe is an open empirical question the repo could answer for itself by comparing probe plans with and without it.
- Claims marked [V-snip] in sections 1–6 should be checked against the full papers before they are quoted in a final report. The most load-bearing of these are the Mitrovic & Martin (2007) and Long & Aleven (2017) outcomes, the Gervet et al. (2020) conditions, the refutation-text meta-analysis authorship, and the Yang et al. (2025) numbers.
