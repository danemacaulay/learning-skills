# Learn Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build five agent skills (`learn-ground`, `learn-plan`, `learn-teach`, `learn-record`, `learn-review`) and a small plain-text store so that each learning session leaves evidence the next one builds on.

**Architecture:** Skills are prose (`SKILL.md`) that an agent follows in chat. Everything deterministic (validating and appending records, merging the graph, deriving what is due) lives in one stdlib-only Python CLI the skills call, so no skill hand-writes JSONL. The store is append-only JSONL plus per-session markdown under `.learn/`, split into a domain graph (no learner state) and a learner log (raw events, no scores).

**Tech Stack:** Python 3.11 standard library only; pytest 9 for tests; Markdown skills; git.

**Spec:** The "Design" section below, which is the proposal agreed in conversation. Its evidence is in `research_notes/AI augmented learning skills review/*.md`; each rule in `skills/_learn/theory.md` cites the note it rests on. The existing `skills/learning-*`, `skills/_shared`, `.learning/` and `docs/2026-11-09-skills-redesign-design.md` are out of scope: do not read, edit or delete them.

## Design

Loop: ground → plan → teach → record → review, and review output feeds the next ground.

```
skills/
  _learn/
    theory.md              shared rules, each with its research basis
    store.md               layout, record schemas, session file templates
    scripts/
      learn.py             CLI entry point
      learnlib/
        schema.py          record validators and enums
        store.py           find/init the store, append, read
        graph.py           current graph view, supersede/retract, candidates
        schedule.py        replay observations into per-target state and due list
        view.py            learner-model markdown view
  learn-ground/SKILL.md
  learn-plan/SKILL.md
  learn-teach/SKILL.md
  learn-record/SKILL.md
  learn-review/SKILL.md
tests/learn/
  conftest.py  test_schema.py  test_store.py  test_graph.py
  test_schedule.py  test_view.py  test_cli.py  test_skills.py  test_walkthrough.py

.learn/                    created in the learner's project by `learn.py init`
  graph/nodes.jsonl        propositions
  graph/chains.jsonl       joint premises -> conclusion
  graph/edits.jsonl        supersede / retract / contradicts
  learner/observations.jsonl   one event per probe, check or review
  learner/misconceptions.jsonl
  learner/links.jsonl      session plan slug -> node/chain ids
  sessions/<YYYYMMDD-topic>/grounding.md plan.md transcript.md extraction.md
```

## Global Constraints

- Python standard library only in `skills/_learn/scripts/`; no third-party imports.
- All JSONL files are append-only. No command rewrites or deletes a line. A correction is a new line.
- No mastery score, probability or percentage is stored anywhere. Status and due dates are derived by replay.
- Learner state never appears in `graph/`; false statements (misconceptions) never appear in `graph/`.
- Timestamps are ISO 8601 UTC with a `Z` suffix, second precision (`2026-11-09T22:19:00Z`).
- Ids are a type prefix plus 8 lowercase hex characters: `o-` observation, `m-` misconception, `n-` node, `c-` chain.
- Skills call the CLI as `python3 <skills-dir>/_learn/scripts/learn.py <subcommand>`; every subcommand prints JSON on stdout, and on failure prints one line to stderr and exits 2.
- Every `SKILL.md` has frontmatter `name` (equal to its directory) and `description` beginning "Use when"; body at most 200 lines; shared rules are linked from `_learn/theory.md`, not copied.
- Default numbers (design defaults, not research findings; say so where they appear): probe budget 3–5 questions per strand and 12–20 per session; review ladder 1, 3, 7, 21, 60 days; review cap 8 targets per sitting; a retrieval counts as delayed when at least 8 hours have passed since the previous event on that target.

## Review Focus

1. **Hand-edited or truncated JSONL line** (the store is meant to be learner-editable): every command fails with `<file>:<line>: <reason>` and exits 2; nothing is appended. Test in Task 1.
2. **Session interrupted after teaching, before recording** (observations keyed to plan slugs that were never linked to nodes): replay keeps them, `due` excludes them, `show` lists the session under "Not yet recorded". Tests in Tasks 3 and 4.
3. **Observation on a node later superseded or retracted**: a superseded target's history carries to its replacement; a retracted target is never due and is reported as `retracted`. Test in Task 3.
4. **Long absence** (dozens of targets due at once): `due` returns at most the limit, chains before nodes, oldest first, with `--prefer` ids ahead of everything. Test in Task 3.
5. **Learner responses with newlines, quotes, emoji or non-Latin text**: stored verbatim and read back byte-identical. Test in Task 1.

---

### Task 1: Store and learner records

**Files:**
- Create: `skills/_learn/scripts/learn.py`, `skills/_learn/scripts/learnlib/__init__.py`, `skills/_learn/scripts/learnlib/schema.py`, `skills/_learn/scripts/learnlib/store.py`
- Test: `tests/learn/conftest.py`, `tests/learn/test_schema.py`, `tests/learn/test_store.py`, `tests/learn/test_cli.py`

**Interfaces:**
- Produces, in `schema.py`:
  - `class ValidationError(ValueError)`
  - `KINDS = ("probe", "check", "review", "final")`
  - `FORMS = ("mc", "free", "predict", "explain-why", "apply", "reconstruct", "counterfactual", "discriminate", "teach-back", "transfer")`
  - `CONFIDENCE = ("low", "med", "high", "not_given")`
  - `GRADES = ("took", "missed", "dont_know")`
  - `validate_observation(rec: dict) -> dict`
  - `validate_misconception(rec: dict) -> dict`
- Produces, in `store.py`:
  - `class StoreNotFound(Exception)`, `class CorruptStore(Exception)` (message `"<relative file>:<line>: <reason>"`)
  - `FILES: dict[str, str]` with keys `observations, misconceptions, links, nodes, chains, edits` mapping to the paths in the Design tree
  - `init_store(cwd: Path) -> Path` (returns the `.learn` directory; idempotent)
  - `find_root(start: Path) -> Path` (walks up from `start` to the first directory containing `.learn`; `LEARN_ROOT` env var overrides)
  - `append(root: Path, file: str, rec: dict, prefix: str | None) -> dict` (adds `id` when `prefix` is given and `id` is absent, adds `ts` when absent, writes one line, returns the stored record)
  - `read(root: Path, file: str) -> list[dict]`
- Produces, in `learn.py`: subcommands `init`, `observe --json <obj>`, `misconception --json <obj>`; global options `--root <dir>` and `--now <ts>`. A module-level `SUBCOMMANDS: tuple[str, ...]` lists every subcommand name (later tasks extend it).

Observation record (required unless marked optional):

| Field | Value |
|---|---|
| `session` | non-empty string |
| `kind` | one of `KINDS` |
| `form` | one of `FORMS` |
| `target` | `{"type": "slug" \| "node" \| "chain", "id": str}` |
| `prompt` | non-empty string |
| `expected` | string or null; required non-null when `kind` is `check`, `review` or `final` (the pre-committed answer) |
| `response` | string, stored verbatim |
| `confidence` | one of `CONFIDENCE` |
| `grade` | one of `GRADES` |
| `produced` | bool (false means recognised from options) |
| `hinted` | bool, default false |
| `lowEffort` | bool, default false |
| `misconception` | optional `m-` id |
| `id`, `ts` | optional; supplied by `append` when absent |

Any other field is rejected.

Misconception record: `statement` (learner's words), `counterpart`, `contradicts` (list of node ids or slugs, may be empty), `evidence` (list of `o-` ids, at least one), `stability` in `stable | shifting | one-off`, `kind` in `category-error | missing-distinction | overgeneralized-fragment`, `status` in `suspected | confirmed | addressed | resolved`, `session`. A line that reuses an existing `id` is an update; the last line for an id wins. `status` of `confirmed` or later requires at least two `evidence` ids.

- [ ] **Step 1: Write `tests/learn/conftest.py`**

Insert `skills/_learn/scripts` at the front of `sys.path`; provide fixture `root(tmp_path) -> Path` that calls `init_store(tmp_path)`, and fixture `obs(**overrides) -> dict` returning this valid observation merged with overrides:

```python
{"session": "20261109-demo", "kind": "check", "form": "apply",
 "target": {"type": "slug", "id": "ready-to-hand"},
 "prompt": "What would this predict when the hammer breaks?",
 "expected": "The tool becomes conspicuous", "response": "you notice it",
 "confidence": "med", "grade": "took", "produced": True}
```

- [ ] **Step 2: Write the failing tests**

```python
# test_schema.py
def test_valid_observation_gets_defaults(obs):
    out = validate_observation(obs())
    assert out["hinted"] is False and out["lowEffort"] is False

@pytest.mark.parametrize("field,value", [
    ("kind", "quiz"), ("form", "cloze"), ("confidence", "sure"),
    ("grade", "partial"), ("prompt", ""), ("target", {"type": "card", "id": "x"}),
])
def test_bad_observation_field_rejected(obs, field, value):
    with pytest.raises(ValidationError, match=field):
        validate_observation(obs(**{field: value}))

def test_check_without_precommitted_expected_rejected(obs):
    with pytest.raises(ValidationError, match="expected"):
        validate_observation(obs(expected=None))

def test_probe_may_omit_expected(obs):
    validate_observation(obs(kind="probe", expected=None))

def test_confirmed_misconception_needs_two_evidence():
    rec = {"statement": "s", "counterpart": "c", "contradicts": [], "evidence": ["o-00000001"],
           "stability": "stable", "kind": "category-error", "status": "confirmed", "session": "s1"}
    with pytest.raises(ValidationError, match="evidence"):
        validate_misconception(rec)
    validate_misconception({**rec, "status": "suspected"})

# test_store.py
def test_init_is_idempotent_and_creates_all_files(tmp_path):
    r = init_store(tmp_path); init_store(tmp_path)
    assert all((r / p).exists() for p in FILES.values()) and (r / "sessions").is_dir()

def test_append_assigns_id_and_ts_and_never_rewrites(root):
    a = append(root, "observations", {"x": 1}, prefix="o")
    b = append(root, "observations", {"x": 2}, prefix="o")
    assert re.fullmatch(r"o-[0-9a-f]{8}", a["id"]) and a["ts"].endswith("Z")
    assert [r["x"] for r in read(root, "observations")] == [1, 2]

def test_verbatim_text_round_trips(root):
    text = 'line one\n"quoted" — 存在 🙂'
    append(root, "observations", {"response": text}, prefix="o")
    assert read(root, "observations")[0]["response"] == text

def test_corrupt_line_names_file_and_line(root):
    (root / FILES["observations"]).write_text('{"ok": 1}\n{broken\n')
    with pytest.raises(CorruptStore, match=r"learner/observations\.jsonl:2"):
        read(root, "observations")

def test_find_root_walks_up(root):
    deep = root.parent / "a" / "b"; deep.mkdir(parents=True)
    assert find_root(deep) == root

# test_cli.py  (helper `run(*args, cwd) -> CompletedProcess` invoking learn.py with sys.executable)
def test_observe_appends_and_prints_id(tmp_path, obs):
    run("init", cwd=tmp_path)
    out = run("observe", "--json", json.dumps(obs()), cwd=tmp_path)
    assert out.returncode == 0 and json.loads(out.stdout)["id"].startswith("o-")

def test_invalid_observation_exits_2_and_appends_nothing(tmp_path, obs):
    run("init", cwd=tmp_path)
    out = run("observe", "--json", json.dumps(obs(grade="partial")), cwd=tmp_path)
    assert out.returncode == 2 and "grade" in out.stderr
    assert (tmp_path / ".learn/learner/observations.jsonl").read_text() == ""

def test_corrupt_store_exits_2_without_appending(tmp_path, obs):
    run("init", cwd=tmp_path)
    f = tmp_path / ".learn/learner/observations.jsonl"; f.write_text("{broken\n")
    out = run("observe", "--json", json.dumps(obs()), cwd=tmp_path)
    assert out.returncode == 2 and "observations.jsonl:1" in out.stderr
    assert f.read_text() == "{broken\n"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python3 -m pytest tests/learn -q`
Expected: collection errors, `ModuleNotFoundError: learnlib`

- [ ] **Step 4: Implement `schema.py`, `store.py` and the three subcommands in `learn.py`**

`observe` and `misconception` read the whole target file first (so a corrupt store blocks the write), validate, then append. `ValidationError` messages start with the offending field name. Use `argparse` with subparsers; `--now` replaces the wall clock everywhere a timestamp is generated.

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/learn -q`
Expected: all pass

- [ ] **Step 6: Commit**

```bash
git add skills/_learn/scripts tests/learn
git commit -m "feat(learn): store, observation and misconception records, CLI skeleton"
```

---

### Task 2: Domain graph

**Files:**
- Create: `skills/_learn/scripts/learnlib/graph.py`
- Modify: `skills/_learn/scripts/learnlib/schema.py`, `skills/_learn/scripts/learn.py`
- Test: `tests/learn/test_graph.py`, extend `tests/learn/test_schema.py`, `tests/learn/test_cli.py`

**Interfaces:**
- Consumes: `append`, `read`, `FILES`, `ValidationError` from Task 1.
- Produces, in `schema.py`:
  - `CLAIM_TYPES = ("definition", "result", "attribution", "consensus", "interpretation")`
  - `NODE_STATUS = ("source-verified", "tutor-asserted", "contested")`
  - `validate_node(rec: dict) -> dict`, `validate_chain(rec: dict, known: set[str]) -> dict`, `validate_edit(rec: dict, known: set[str]) -> dict`
- Produces, in `graph.py`:
  - `current(nodes: list[dict], chains: list[dict], edits: list[dict]) -> tuple[dict[str, dict], dict[str, dict]]` (active nodes by id, active chains by id)
  - `resolve(target_id: str, edits: list[dict]) -> str | None` (follows `supersede` to the live id; `None` when retracted)
  - `candidates(statement: str, nodes: Iterable[dict], k: int = 5, threshold: float = 0.2) -> list[tuple[str, float]]`
- Produces, in `learn.py`: subcommands `node --json`, `chain --json`, `edit --json`, `candidates --statement <text>`, `graph` (prints the current view as `{"nodes": [...], "chains": [...]}`).

Node: `name` (kebab-case), `statement`, `claimType`, `status`, `source` (string or null), `scope` (string or null: "according to which text or reading"), `session`. Rules: `source` is required when `status` is `source-verified` or `claimType` is `attribution`; `scope` is required when `claimType` is `interpretation`; a `statement` containing any of `" because "`, `" therefore "`, `" hence "`, `" which means "` (case-insensitive) is rejected with a message telling the caller to split it into premises and a chain.

Chain: `premises` (one or more node ids, no duplicates), `conclusion` (node id not in `premises`), `session`; every id must be in `known`.

Edit: `{"op": "supersede", "target": id, "by": id, "reason": str}`, `{"op": "retract", "target": id, "reason": str}` or `{"op": "contradicts", "a": id, "b": id, "reason": str}`, each with `session`. A node or chain may be the target. A chain is inactive when it, any premise or its conclusion is retracted; a superseded member is replaced by its live id in the returned chain.

`candidates` scores Jaccard similarity over lowercase word sets of `name` (hyphens split) plus `statement`, after dropping words of three letters or fewer; returns active nodes at or above `threshold`, best first, at most `k`.

- [ ] **Step 1: Write the failing tests**

```python
N = lambda **kw: {"name": "equipment-is-ready-to-hand", "statement": "Equipment in use is ready-to-hand.",
                  "claimType": "attribution", "status": "source-verified",
                  "source": "Being and Time §15", "scope": None, "session": "s1", **kw}

def test_compound_statement_rejected():
    with pytest.raises(ValidationError, match="chain"):
        validate_node(N(statement="Tools withdraw because we attend to the work."))

def test_attribution_requires_source():
    with pytest.raises(ValidationError, match="source"):
        validate_node(N(source=None, status="tutor-asserted"))

def test_interpretation_requires_scope():
    with pytest.raises(ValidationError, match="scope"):
        validate_node(N(claimType="interpretation", scope=None))

def test_chain_ids_must_exist_and_conclusion_not_a_premise():
    with pytest.raises(ValidationError, match="premises"):
        validate_chain({"premises": ["n-1"], "conclusion": "n-2", "session": "s"}, known={"n-2"})
    with pytest.raises(ValidationError, match="conclusion"):
        validate_chain({"premises": ["n-1"], "conclusion": "n-1", "session": "s"}, known={"n-1"})

def test_supersede_replaces_and_chains_follow():
    nodes = [{"id": "n-1"}, {"id": "n-2"}, {"id": "n-3"}]
    chains = [{"id": "c-1", "premises": ["n-1"], "conclusion": "n-2"}]
    edits = [{"op": "supersede", "target": "n-1", "by": "n-3"}]
    active_nodes, active_chains = current(nodes, chains, edits)
    assert set(active_nodes) == {"n-2", "n-3"} and active_chains["c-1"]["premises"] == ["n-3"]
    assert resolve("n-1", edits) == "n-3"

def test_retract_deactivates_dependent_chains():
    nodes = [{"id": "n-1"}, {"id": "n-2"}]
    chains = [{"id": "c-1", "premises": ["n-1"], "conclusion": "n-2"}]
    edits = [{"op": "retract", "target": "n-1", "reason": "tutor error"}]
    active_nodes, active_chains = current(nodes, chains, edits)
    assert set(active_nodes) == {"n-2"} and active_chains == {} and resolve("n-1", edits) is None

def test_candidates_rank_similar_statement_first_and_skip_unrelated():
    nodes = [N(id="n-1"), N(id="n-2", name="primary-key", statement="A primary key identifies a row.")]
    got = candidates("Equipment being used is ready-to-hand", nodes)
    assert [i for i, _ in got] == ["n-1"]

# test_cli.py
def test_chain_with_unknown_node_exits_2(tmp_path):
    run("init", cwd=tmp_path)
    out = run("chain", "--json", '{"premises":["n-deadbeef"],"conclusion":"n-00000000","session":"s"}', cwd=tmp_path)
    assert out.returncode == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/learn/test_graph.py tests/learn/test_schema.py -q`
Expected: FAIL, `ImportError` for `learnlib.graph` / `validate_node`

- [ ] **Step 3: Implement the validators, `graph.py` and the five subcommands**

`known` for `chain` and `edit` is every id ever written to `nodes.jsonl` and `chains.jsonl` (edits may target inactive ids so mistakes in edits can themselves be corrected).

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/learn -q`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add skills/_learn/scripts tests/learn
git commit -m "feat(learn): domain graph with claim types, supersede/retract, link candidates"
```

---

### Task 3: Replay and review schedule

**Files:**
- Create: `skills/_learn/scripts/learnlib/schedule.py`
- Modify: `skills/_learn/scripts/learn.py`
- Test: `tests/learn/test_schedule.py`, extend `tests/learn/test_cli.py`

**Interfaces:**
- Consumes: `read`, `append` (Task 1); `resolve`, `current` (Task 2).
- Produces, in `schedule.py`:
  - `LADDER_DAYS = (1, 3, 7, 21, 60)`, `MIN_DELAY_HOURS = 8`
  - `@dataclass TargetState`: `target_id: str`, `target_type: str` (`slug | node | chain`), `status: str` (`taught | retained | lapsed | retracted | unlinked`), `rung: int`, `due_at: str | None`, `last_ts: str`, `last_grade: str`, `events: int`, `session: str` (session of the first event)
  - `replay(observations: list[dict], links: list[dict], edits: list[dict], chains: Sequence[dict] = ()) -> dict[str, TargetState]`
  - `due(states: dict[str, TargetState], now: str, limit: int = 8, prefer: Sequence[str] = ()) -> list[TargetState]`
- Produces, in `learn.py`: subcommands `link --session S --slug X --targets id[,id...]` (appends `{"session","slug","targets"}` to `links.jsonl`; every target must be a known id), `state [--target id]`, `due [--limit N] [--prefer id,id]`.

Replay rules, applied to observations in `(ts, file order)` order:

1. Target key. A `slug` target is replaced by each id it links to (matching `session` and `slug`), so one observation can count for several nodes or chains. An unlinked slug keeps key `"<session>/<slug>"` and status `unlinked`. Node and chain ids pass through `resolve`; a `None` result gives status `retracted` and no further updates. A chain in `chains` whose premises or conclusion include a retracted node is also `retracted`. An id's type is read from its prefix (`n-` node, `c-` chain).
2. Observations with `lowEffort: true` increment `events` and nothing else.
3. An observation is *delayed* when the target has no earlier event, or at least `MIN_DELAY_HOURS` separate it from the target's previous event.
4. First event on a target: `took` with `produced` true, `hinted` false and `kind` `probe` or `review` → `retained`, rung 1 (prior knowledge shown cold). Any other first event → `taught`, rung 0.
5. Later, delayed, `took`, `produced`, not `hinted` → `retained`, rung `min(rung + 1, 4)`.
6. Later, delayed, `took` but hinted or not produced → status and rung unchanged.
7. Later, delayed, `missed` or `dont_know` → `lapsed` if status was `retained`, otherwise unchanged; rung `max(rung - 1, 0)`.
8. Not delayed → status and rung unchanged (same-sitting re-asks do not climb the ladder).
9. After every non-low-effort event, `due_at = ts + LADDER_DAYS[rung]` days; `last_ts` and `last_grade` are updated.

`due` returns states with a `due_at` at or before `now`, excluding `unlinked` and `retracted`; order: ids in `prefer` first (in the given order), then chains before nodes, then oldest `due_at`; truncated to `limit`.

- [ ] **Step 1: Write the failing tests**

Helper `ev(ts, target="n-1", ttype="node", **kw)` builds a valid observation dict with that `ts`.

```python
def test_in_session_check_is_taught_and_due_next_day():
    s = replay([ev("2026-11-09T10:00:00Z")], [], [])["n-1"]
    assert (s.status, s.rung, s.due_at) == ("taught", 0, "2026-11-10T10:00:00Z")

def test_delayed_success_becomes_retained_and_climbs():
    s = replay([ev("2026-11-09T10:00:00Z"),
                ev("2026-11-10T10:00:00Z", kind="review", form="reconstruct")], [], [])["n-1"]
    assert (s.status, s.rung, s.due_at) == ("retained", 1, "2026-11-13T10:00:00Z")

def test_same_sitting_reask_does_not_climb():
    s = replay([ev("2026-11-09T10:00:00Z"), ev("2026-11-09T10:20:00Z"), ev("2026-11-09T10:40:00Z")], [], [])["n-1"]
    assert (s.status, s.rung) == ("taught", 0)

def test_hinted_or_recognised_success_does_not_climb():
    base = [ev("2026-11-09T10:00:00Z")]
    assert replay(base + [ev("2026-11-10T10:00:00Z", hinted=True)], [], [])["n-1"].status == "taught"
    assert replay(base + [ev("2026-11-10T10:00:00Z", produced=False)], [], [])["n-1"].status == "taught"

def test_delayed_miss_lapses_and_drops_a_rung():
    evs = [ev("2026-11-01T10:00:00Z"), ev("2026-11-02T10:00:00Z"), ev("2026-11-05T10:00:00Z"),
           ev("2026-11-12T10:00:00Z", grade="missed")]
    s = replay(evs, [], [])["n-1"]
    assert (s.status, s.rung, s.due_at) == ("lapsed", 1, "2026-11-15T10:00:00Z")

def test_rung_is_capped_at_sixty_days():
    evs = [ev(f"2026-{m:02d}-01T10:00:00Z") for m in range(1, 10)]
    assert replay(evs, [], [])["n-1"].rung == 4

def test_cold_probe_success_counts_as_prior_knowledge():
    s = replay([ev("2026-11-09T10:00:00Z", kind="probe", form="free")], [], [])["n-1"]
    assert (s.status, s.rung) == ("retained", 1)

def test_low_effort_events_do_not_change_state():
    s = replay([ev("2026-11-09T10:00:00Z"), ev("2026-11-10T10:00:00Z", lowEffort=True)], [], [])["n-1"]
    assert (s.status, s.events) == ("taught", 2)

def test_slug_events_follow_links_and_unlinked_are_flagged():
    evs = [ev("2026-11-09T10:00:00Z", target="tool-use", ttype="slug", session="s1")]
    assert replay(evs, [], [])["s1/tool-use"].status == "unlinked"
    linked = replay(evs, [{"session": "s1", "slug": "tool-use", "targets": ["n-1", "c-1"]}], [])
    assert set(linked) == {"n-1", "c-1"} and linked["c-1"].target_type == "chain"

def test_superseded_history_carries_over_and_retracted_is_never_due():
    evs = [ev("2026-11-09T10:00:00Z")]
    assert "n-2" in replay(evs, [], [{"op": "supersede", "target": "n-1", "by": "n-2"}])
    states = replay(evs, [], [{"op": "retract", "target": "n-1", "reason": "x"}])
    assert states["n-1"].status == "retracted" and due(states, "2027-01-01T00:00:00Z") == []

def test_chain_with_a_retracted_premise_is_retracted():
    evs = [ev("2026-11-09T10:00:00Z", target="c-1", ttype="chain")]
    chains = [{"id": "c-1", "premises": ["n-1"], "conclusion": "n-2"}]
    states = replay(evs, [], [{"op": "retract", "target": "n-1", "reason": "x"}], chains)
    assert states["c-1"].status == "retracted"

def test_events_out_of_file_order_are_sorted_by_ts():
    evs = [ev("2026-11-10T10:00:00Z", kind="review"), ev("2026-11-09T10:00:00Z")]
    assert replay(evs, [], [])["n-1"].status == "retained"

def test_due_caps_prefers_and_orders_chains_first():
    evs = [ev("2026-11-01T10:00:00Z", target=f"n-{i}") for i in range(20)]
    evs += [ev("2026-11-02T10:00:00Z", target="c-1", ttype="chain")]
    got = due(replay(evs, [], []), "2026-12-01T00:00:00Z", limit=8, prefer=["n-19"])
    assert len(got) == 8 and [g.target_id for g in got[:2]] == ["n-19", "c-1"]

def test_nothing_due_before_its_date():
    assert due(replay([ev("2026-11-09T10:00:00Z")], [], []), "2026-11-09T12:00:00Z") == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/learn/test_schedule.py -q`
Expected: FAIL, `ModuleNotFoundError: learnlib.schedule`

- [ ] **Step 3: Implement `schedule.py` and the `link`, `state`, `due` subcommands**

`state` and `due` print lists of `dataclasses.asdict(TargetState)`; `due` honours `--now`.

- [ ] **Step 4: Add a CLI test and run everything**

```python
def test_due_cli_round_trip(tmp_path, obs):
    run("init", cwd=tmp_path)
    run("--now", "2026-11-09T10:00:00Z", "observe", "--json",
        json.dumps(obs(target={"type": "node", "id": "n-00000001"})), cwd=tmp_path)
    out = run("--now", "2026-11-11T10:00:00Z", "due", cwd=tmp_path)
    assert [s["target_id"] for s in json.loads(out.stdout)] == ["n-00000001"]
```

Run: `python3 -m pytest tests/learn -q`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add skills/_learn/scripts tests/learn
git commit -m "feat(learn): replay observations into status and a spaced review queue"
```

---

### Task 4: Learner-model view

**Files:**
- Create: `skills/_learn/scripts/learnlib/view.py`
- Modify: `skills/_learn/scripts/learn.py`
- Test: `tests/learn/test_view.py`

**Interfaces:**
- Consumes: `read` (Task 1); `current` (Task 2); `replay`, `due` (Task 3).
- Produces: `render(root: Path, now: str) -> str` in `view.py`; subcommand `show` (prints the markdown, the one command whose stdout is not JSON).

The view has these `##` sections in this order, each omitted when empty: `Due now` (target, statement or chain conclusion, days overdue), `Retained`, `Taught, not yet retained`, `Lapsed`, `Misconceptions` (latest line per id, grouped by status, with `resolved` last), `Calibration`, `Not yet recorded` (sessions with unlinked slug observations, with the instruction "run learn-record for this session"). `Calibration` is a table of counts of non-low-effort observations by `confidence` (rows: high, med, low) and `grade` (columns), followed by one sentence naming the count of high-confidence misses.

- [ ] **Step 1: Write the failing tests**

```python
def test_empty_store_renders_a_single_line(root):
    assert render(root, "2026-11-09T00:00:00Z").strip() == "Nothing recorded yet."

def test_sections_reflect_state(root, obs):
    n = append(root, "nodes", {"name": "a", "statement": "A holds."}, prefix="n")
    append(root, "observations", obs(target={"type": "node", "id": n["id"]}, ts="2026-11-01T10:00:00Z",
                                     confidence="high", grade="missed"), prefix="o")
    append(root, "observations", obs(target={"type": "slug", "id": "loose"}, session="s9",
                                     ts="2026-11-01T10:05:00Z"), prefix="o")
    append(root, "misconceptions", {"statement": "Tools are just objects", "status": "suspected"}, prefix="m")
    text = render(root, "2026-11-09T00:00:00Z")
    assert "## Due now" in text and "A holds." in text
    assert "## Misconceptions" in text and "Tools are just objects" in text
    assert "1 high-confidence miss" in text
    assert "## Not yet recorded" in text and "s9" in text
    assert "## Retained" not in text

def test_latest_misconception_line_wins(root):
    m = append(root, "misconceptions", {"statement": "x", "status": "suspected"}, prefix="m")
    append(root, "misconceptions", {**m, "status": "resolved"}, prefix=None)
    assert "resolved" in render(root, "2026-11-09T00:00:00Z").lower()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/learn/test_view.py -q`
Expected: FAIL, `ModuleNotFoundError: learnlib.view`

- [ ] **Step 3: Implement `render` and the `show` subcommand**

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/learn -q`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add skills/_learn/scripts tests/learn
git commit -m "feat(learn): inspectable learner-model view with calibration"
```

---

### Task 5: Shared theory, store reference and skill lint

**Files:**
- Create: `skills/_learn/theory.md`, `skills/_learn/store.md`
- Test: `tests/learn/test_skills.py`

**Interfaces:**
- Consumes: `SUBCOMMANDS` from `learn.py` (Tasks 1–4).
- Produces: `REQUIRED: dict[str, list[str]]` in `test_skills.py`, mapping a skill directory name to phrases its `SKILL.md` must contain. Tasks 6–10 each add one entry. Rule ids `T1`–`T12` in `theory.md`, which skills cite as `theory.md#T<n>`.

`theory.md` holds exactly these rules. Each is a heading `### T<n>: <rule>`, two to four sentences of instruction, and a `Basis:` line naming the research note file and section it rests on.

| Id | Rule | Basis (file § section) |
|---|---|---|
| T1 | The goal is written as 2–4 things the learner will do unaided; felt obviousness is recorded but never ends a session by itself | diagnosis_and_planning §7; retention_and_metacognition §3 |
| T2 | Learner attempts first on any step derivable from what they hold; assert only what cannot be derived, or after a failed attempt shows a missing prerequisite | llm_tutoring_evidence §4; retention_and_metacognition §4 |
| T3 | One meaningful inference per step, one check per step, repair before building; never split finer than one inference | llm_tutoring_evidence §1 |
| T4 | Write the expected answer and the named wrong models before the learner replies; judge took / missed before composing any response; "makes sense" is never a pass | llm_tutoring_evidence §6 |
| T5 | Ask confidence (low / med / high) before giving feedback on every question; record it next to the outcome, never instead of it | diagnosis_and_planning §4; llm_tutoring_evidence §3 |
| T6 | Feedback addresses the task or the reasoning, never the person; give it on every miss and on every low-confidence correct answer | diagnosis_and_planning §5 |
| T7 | A misconception inferred by the tutor is `suspected` until a second probe confirms it; stable ones get a refutation (state it, say it is wrong, explain why, then a check it would fail), shifting ones get a "when does each idea apply" step | diagnosis_and_planning §3; learner_models_and_graph §5 |
| T8 | An in-session pass means `taught`; only an unhinted, produced answer after a delay means `retained` | retention_and_metacognition §2 |
| T9 | Review whole chains by reconstruction, application or dropping a premise; never cloze or verbatim recall of a statement; never interleave new teaching | retention_and_metacognition §1, §7 |
| T10 | Every claim carries its epistemic status in one clause (definition, established result, the author's claim with locus, scholarly consensus, one reading among several); nothing unverified is stored as verified | llm_tutoring_evidence §5; learner_models_and_graph §5 |
| T11 | The system owns ordering and sourcing; the learner owns the goal, the pace and when to stop; the system never does the learner's retrieval or generation for them | llm_tutoring_evidence §3, §7; diagnosis_and_planning §8 |
| T12 | Tell the learner up front that attempting first and delayed recall feel harder and slower, and that this is the mechanism; none of this method has been tested in this setting | retention_and_metacognition §8; llm_tutoring_evidence §8 |

`store.md` contains: the `.learn/` tree from the Design section; one field table per record type copied from Tasks 1–3; one example CLI invocation per subcommand; the derived statuses and ladder from Task 3; and the four session file templates below.

- `grounding.md`: `## Goal`, `## Success criteria` (2–4 numbered performances), `## Strands` (per strand: status `bracketed | held-to-goal | partial | not-probed`, floor, ceiling, floor quality `produced | recognised-only | fragile`, evidence as `o-` ids), `## Misconceptions` (`m-` ids), `## Session conditions` (questions asked, stop reason `complete | budget | learner-request | effort-drop`, strands not probed).
- `plan.md`: `## Goal in one paragraph`, `## Sources` (or the line `Unverified: no sources available this session`), `## Map` (a mermaid graph over slugs), `## Landmarks` table with columns `slug | claim | epistemic status | source | grounding status | move (attempt-first / assert / refute / discriminate / contrast) | check | expected answer | wrong models`, `## Final tasks` (the closed-transcript teach-back prompt and one transfer question, each with its scoring points).
- `transcript.md`: per step `## Step: <slug>` with `Prediction:`, `Explanation:`, `Check:`, `Expected:`, `Wrong models:`, `Confidence:`, `Response:`, `Judgement:`, `Repair:` (if any), `Observation: o-…`.
- `extraction.md`: `## Verification` (per claim: checked against which source, result), `## Proposed nodes and chains`, `## Link decisions` (per proposed node: candidates returned, decision `linked to <id>` or `created`, one-line reason), `## Learner review` (what the learner contested and the outcome), `## Written` (ids and the slug links).

- [ ] **Step 1: Write the failing test**

```python
SKILLS = Path(__file__).parents[2] / "skills"
REQUIRED: dict[str, list[str]] = {}   # filled by Tasks 6-10

def test_theory_has_all_rules_each_with_a_basis():
    text = (SKILLS / "_learn/theory.md").read_text()
    for n in range(1, 13):
        section = re.search(rf"### T{n}:.*?(?=### T\d+:|\Z)", text, re.S)
        assert section and "Basis:" in section.group(0), f"T{n}"

def test_store_doc_shows_every_subcommand():
    text = (SKILLS / "_learn/store.md").read_text()
    assert all(f"learn.py {c}" in text for c in learn.SUBCOMMANDS)

@pytest.mark.parametrize("skill", sorted(REQUIRED))
def test_skill_file(skill):
    text = (SKILLS / skill / "SKILL.md").read_text()
    front, body = text.split("---", 2)[1:]
    assert re.search(rf"^name: {skill}$", front, re.M)
    assert re.search(r"^description: Use when", front, re.M)
    assert len(body.splitlines()) <= 200
    assert all(p in body for p in REQUIRED[skill]), [p for p in REQUIRED[skill] if p not in body]
    for cmd in re.findall(r"learn\.py ([a-z-]+)", body):
        assert cmd in learn.SUBCOMMANDS, cmd
    for ref in re.findall(r"\((\.\./_learn/[^)#]+)", body):
        assert (SKILLS / skill / ref).exists(), ref
    for rule in re.findall(r"theory\.md#T(\d+)", body):
        assert 1 <= int(rule) <= 12
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 -m pytest tests/learn/test_skills.py -q`
Expected: FAIL, `FileNotFoundError` for `theory.md`

- [ ] **Step 3: Write `theory.md` and `store.md`** from the tables and templates above. Take each `Basis:` line's wording from the named section of the research note; quote no number tagged `[R]`, `[S]`, "secondary only" or "not re-fetched" in that note.

- [ ] **Step 4: Run to verify it passes**

Run: `python3 -m pytest tests/learn -q`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add skills/_learn/theory.md skills/_learn/store.md tests/learn/test_skills.py
git commit -m "docs(learn): shared theory with research basis, store reference, skill lint"
```

---

### Tasks 6–10: the five skills

Each of these tasks has the same five steps; only the content differs.

- [ ] **Step 1:** Add the task's `REQUIRED` entry to `tests/learn/test_skills.py`.
- [ ] **Step 2:** Run `python3 -m pytest tests/learn/test_skills.py -q`; expected: FAIL, `FileNotFoundError` for that `SKILL.md`.
- [ ] **Step 3:** Write the `SKILL.md` with sections `## When to use`, `## Reads`, `## Procedure` (the numbered steps given in the task), `## Hard rules` (the listed rules, each citing its `theory.md#T<n>`), `## Writes`. Link `../_learn/theory.md` and `../_learn/store.md`; do not restate their content.
- [ ] **Step 4:** Run `python3 -m pytest tests/learn -q`; expected: all pass.
- [ ] **Step 5:** `git add skills/<skill> tests/learn/test_skills.py && git commit -m "feat(learn): <skill> skill"`.

---

### Task 6: `learn-ground`

**Files:** Create `skills/learn-ground/SKILL.md`; modify `tests/learn/test_skills.py`.

**Interfaces:** Consumes `learn.py init | show | state | due | observe | misconception`. Produces `.learn/sessions/<id>/grounding.md` (template in `store.md`) and `probe` observations keyed to slugs or, for prior items, node/chain ids.

`description: Use when someone wants to learn or understand a topic and no grounding exists yet for this session's goal`

`REQUIRED["learn-ground"] = ["learn.py init", "learn.py due", "learn.py observe", "learn.py misconception", "Success criteria", "3–5", "12–20", "stop and plan from here", "theory.md#T1", "theory.md#T5", "theory.md#T7", "theory.md#T12"]`

Procedure the skill must state:
1. Run `init` if there is no store; create the session folder `YYYYMMDD-<topic>`; run `show` and read it.
2. Ask until the goal is specific, then write 2–4 success criteria as unaided performances (explain X in own words; apply to a new case; say what a named rival view gets wrong). The learner confirms them.
3. Say the purpose and the budget out loud: about 12–20 questions, wrong answers are the point, the learner can stop at any strand boundary. Give the T12 warning once.
4. If `due --prefer <ids relevant to this goal>` returns anything, cold-probe those first, one question each, free response, no recap beforehand. These are `kind: probe` on the node or chain id.
5. Split the goal into strands; let the learner choose the order. Per strand, one question at a time, each chosen from the last answer, entering above the expected floor with large jumps after confident correct answers. No teaching and no feedback during the probe; tell the learner feedback comes in teaching.
6. Every question asks for confidence. Multiple-choice questions also ask for a one-line reason, and each wrong option is written to embody a named candidate wrong idea.
7. Log every answer with `observe` immediately (`kind: probe`, `produced` false for option picks).
8. A strand is finished when it holds at the level the goal needs, or floor and ceiling are adjacent, or two consecutive questions moved neither edge, or 5 questions are spent. A floor needs at least one produced answer.
9. Two consecutive bare option picks without reason or confidence: mark them `lowEffort`, switch to one free-response question, and if that is also minimal, stop.
10. On a wrong answer, one follow-up to tell slip, gap or wrong idea apart. Record a wrong idea with `misconception` as `suspected`, in the learner's words; `confirmed` only after a second observation.
11. At each strand boundary offer "stop and plan from here". Partial grounding is a valid end: mark unprobed strands `not-probed`.
12. Write `grounding.md`; hand off to `learn-plan`.

---

### Task 7: `learn-plan`

**Files:** Create `skills/learn-plan/SKILL.md`; modify `tests/learn/test_skills.py`.

**Interfaces:** Consumes `grounding.md`; `learn.py graph | candidates | state`. Produces `plan.md` (template in `store.md`).

`description: Use when a session has a grounding.md and no approved plan.md`

`REQUIRED["learn-plan"] = ["learn.py graph", "learn.py candidates", "Unverified", "contrasting case", "refut", "expected answer", "wrong models", "theory.md#T2", "theory.md#T4", "theory.md#T7", "theory.md#T10", "theory.md#T11"]`

Procedure the skill must state:
1. Read `grounding.md`; run `graph`, and `candidates` on the goal and each strand to find propositions already in the store.
2. Gather sources: texts the learner supplies, then web or file tools if available. List them under `## Sources` with what each supports. With no sources, write the `Unverified` line and tell the learner.
3. Write the goal as the simplest true version of the whole, in one paragraph.
4. Build the prerequisite map from each strand's floor up to the success criteria: nothing below a floor, nothing above the goal, no tangents however interesting.
5. Choose each landmark's move: `attempt-first` when its premises are held; `assert` when it cannot be derived from what is held; `refute` for each confirmed, stable misconception; `discriminate` for shifting or one-off ones; `contrast` (one paired contrasting case, principle stated after the comparison) for each landmark a success criterion depends on.
6. Where a strand's floor is low, add the connecting steps explicitly; where it is high, keep it lean. Split any landmark that needs several unheld ideas related at once.
7. For every landmark write the epistemic status and source, the check (apply, predict or explain-why, never parrot), the expected answer, and the wrong models with what each would reveal. For a `refute` landmark the check must be one the misconception gets wrong.
8. Mark landmarks that reuse a store node as "retrieve, do not re-teach": they get a cold question first and become repair steps only on a miss.
9. Write `## Final tasks`: a closed-transcript teach-back of the goal and one transfer question on a case not used in the plan, with scoring points taken from the landmark chain.
10. Show the map and ask exactly two things: is this the goal you meant, and do you really hold the landmarks marked held? Revise until approved. Do not ask the learner to validate the dependency structure.

---

### Task 8: `learn-teach`

**Files:** Create `skills/learn-teach/SKILL.md`; modify `tests/learn/test_skills.py`.

**Interfaces:** Consumes `plan.md`, `grounding.md`; `learn.py observe | misconception | due`. Produces `transcript.md` and `check` / `final` observations keyed to plan slugs.

`description: Use when a session has an approved plan.md and teaching is not finished, including resuming a paused session`

`REQUIRED["learn-teach"] = ["learn.py observe", "Expected:", "Wrong models:", "before the learner replies", "closed transcript", "taught", "retained", "theory.md#T2", "theory.md#T3", "theory.md#T4", "theory.md#T5", "theory.md#T6", "theory.md#T8"]`

Procedure the skill must state:
1. Starting or resuming: ask the learner to recall the steps so far from memory before any recap. On a first start, give feedback on every probe answer that was wrong or low-confidence correct in grounding.
2. One landmark at a time, in map order. For each, write `## Step: <slug>` in `transcript.md`, including `Expected:` and `Wrong models:` copied from the plan, before the learner replies.
3. Move `attempt-first`: pose the question and wait for the learner's attempt, then consolidate from what they produced. If the attempt shows a missing prerequisite, switch to a worked explanation and add the prerequisite to the plan.
4. Move `assert`: state it with its epistemic status in one clause, then check with an application.
5. Moves `refute`, `discriminate`, `contrast`: as defined in `theory.md#T7` and the plan.
6. Ask the check, ask confidence, and stop until the learner answers. One question per message.
7. Judge against `Expected:` as took or missed and write `Judgement:` before composing the reply. A reply of agreement without content is a miss; ask again.
8. Log with `observe` (`kind: check`). On a miss, name the wrong model shown, repair, and re-ask in a different form; log the re-ask too. Update the matching misconception's status (`addressed` when its refutation check is passed).
9. Every third step, ask one question that needs an earlier step, with no scrolling back.
10. The step into each success criterion uses an explain-why check ("why does this follow from what you already held?").
11. After the last landmark: free recall of the whole path, then the plan's final tasks with the transcript closed. Score against the plan's scoring points; log as `kind: final`, forms `teach-back` and `transfer`.
12. Ask whether the goal now feels obvious; record the answer beside the scores and show the learner any gap between them.
13. Close by saying the result is `taught`, that `retained` is decided at the next review, and when that is due. Hand off to `learn-record`.

---

### Task 9: `learn-record`

**Files:** Create `skills/learn-record/SKILL.md`; modify `tests/learn/test_skills.py`.

**Interfaces:** Consumes `transcript.md`, `plan.md`; `learn.py candidates | node | chain | edit | link | show`. Produces `extraction.md`, graph lines, and one `links.jsonl` line per taught slug.

`description: Use when a session's teaching is finished or paused and its transcript has not been written to the store, or when show lists a session as not yet recorded`

`REQUIRED["learn-record"] = ["learn.py candidates", "learn.py node", "learn.py chain", "learn.py edit", "learn.py link", "tutor-asserted", "source-verified", "one claim", "Link decisions", "theory.md#T10"]`

Procedure the skill must state:
1. Extract candidate propositions and chains from the tutor's explanations in the transcript only. Learner answers are never a source of graph content.
2. Atomicity: one claim per node; anything with a "because" becomes premises plus a chain. All premises of a chain are jointly needed; two routes to one conclusion are two chains.
3. Verify each claim against the plan's sources before writing anything, in a pass separate from extraction. Set `status`: `source-verified` (with `source`), `tutor-asserted` (no source checked), or `contested`. Set `claimType`; an `interpretation` carries its `scope`.
4. For each proposed node run `candidates`; decide link or create; write the candidates, decision and reason under `## Link decisions`.
5. Show the learner the proposed nodes and chains and which slugs will be linked. Ask them to restate or correct each chain's premises. Record what they contest; change the proposal or mark the node `contested`.
6. Write with `node`, then `chain`, then `link` for every slug that has observations in this session.
7. If the session exposed an error in an existing node, write a `supersede` or `retract` edit with the reason; rival readings get a `contradicts` edit, never a silent overwrite.
8. Run `show`, confirm "Not yet recorded" no longer lists the session, and tell the learner the next review date.

---

### Task 10: `learn-review`

**Files:** Create `skills/learn-review/SKILL.md`; modify `tests/learn/test_skills.py`.

**Interfaces:** Consumes `learn.py due | graph | observe | misconception | show`. Produces `review` observations keyed to node or chain ids.

`description: Use when the learner wants to review or practise earlier material, or at the start of any learning session when learn.py due returns items`

`REQUIRED["learn-review"] = ["learn.py due", "learn.py observe", "reconstruct", "counterfactual", "discriminate", "hinted", "at most 8", "theory.md#T4", "theory.md#T5", "theory.md#T8", "theory.md#T9"]`

Procedure the skill must state:
1. Run `due` (at most 8 targets); if nothing is due, say when the next item is and stop. Do not show transcripts or statements beforehand.
2. Per target choose a form: chains get `reconstruct` ("without looking, why does C hold? give the premises and how they combine"), then on later visits `apply` to a new case or `counterfactual` ("if this premise were false, what happens to the conclusion?"); two easily confused nodes from different sessions get `discriminate`. Never cloze or verbatim recall.
3. Before asking, write the expected answer: for a chain, its premises and the linking inference as scoring points.
4. Ask, ask confidence, wait. Judge took only if every premise and the link are produced; otherwise missed. Log with `observe` (`kind: review`).
5. On a miss: give task-level feedback, re-teach that chain briefly from its premises, continue with other targets, then re-ask the missed one once more in the same sitting. Log the re-ask with `hinted: true`.
6. A miss that matches a recorded misconception reopens it (`status: confirmed`, evidence appended); a new wrong idea is recorded as `suspected`.
7. End with `show`; tell the learner what moved to retained, what lapsed, and the next due date. No new material in a review sitting.

---

### Task 11: End-to-end walkthrough

**Files:**
- Test: `tests/learn/test_walkthrough.py`
- Create: `skills/_learn/README.md`

**Interfaces:**
- Consumes: every subcommand from Tasks 1–4; the skill files from Tasks 6–10.

- [ ] **Step 1: Write the walkthrough test**

One test, `test_two_sessions_build_on_each_other(tmp_path)`, driving only the CLI with `--now`:

1. Day 0 (`2026-11-09T10:00:00Z`): `init`; three `probe` observations on slugs in session `s1`, all graded `missed` or `dont_know`, one of them a high-confidence miss; a `suspected` misconception citing it; two `check` observations and one `final`; then `node` ×3, `chain` ×1, `link` for each slug.
2. Assert `state` shows the chain and its nodes as `taught`, and `due` at day 0 + 2 hours is empty.
3. Day 2: assert `due` lists the chain first. Log a `review` `took` on the chain and a `review` `missed` on one node.
4. Assert the chain is `retained` with `due_at` three days later, and the missed node is still `taught` and due the next day.
5. Day 3: `retract` the missed node with a reason. Assert `graph` no longer contains the node or the chain, `due` ten days later contains neither of them, and `show` contains `## Misconceptions` and no `## Not yet recorded`.
6. Assert every `.jsonl` file only grew: each file's content at step 5 starts with its content at step 2.

- [ ] **Step 2: Run it**

Run: `python3 -m pytest tests/learn -q`
Expected: all pass. A failure here is a defect in Tasks 1–4; fix it in the owning module and add a unit test there.

- [ ] **Step 3: Write `skills/_learn/README.md`**

Sections: what the five skills are and the order they run in (one line each); how to install (copy or symlink `skills/learn-*` and `skills/_learn` into the agent's skills directory); where the store lives and that it is the learner's to read and edit; the `show` command; and a limits paragraph stating that the method is assembled from adjacent research, has not been evaluated in an LLM chat tutor, and that the question budgets and review intervals are defaults to tune.

- [ ] **Step 4: Live dry run**

In a scratch directory outside the repo, dispatch a fresh agent with only the five skill directories and `_learn/`, and the prompt "I want to understand why binary search is O(log n)". Play the learner for one short session through ground, plan, teach and record, including one deliberately wrong answer given with high confidence and one bare "makes sense" reply. Then run `learn.py --now <two days later> due` and start `learn-review`.

Pass conditions, each checked against the files in `.learn/`:
- every question the agent asked has an observation with a confidence value;
- the wrong answer produced a misconception record and a later refute or repair step;
- the "makes sense" reply was not graded `took`;
- `transcript.md` shows `Expected:` written before each response;
- no node has `status: source-verified` without a `source`;
- the review asked for a reconstruction and did not show the chain first.

For each condition that fails, tighten the wording of the owning skill's procedure step or hard rule, add the phrase to its `REQUIRED` list if one is missing, and rerun the dry run once.

- [ ] **Step 5: Commit**

```bash
git add tests/learn/test_walkthrough.py skills/_learn/README.md skills/learn-*
git commit -m "test(learn): two-session walkthrough; docs: README and dry-run fixes"
```
