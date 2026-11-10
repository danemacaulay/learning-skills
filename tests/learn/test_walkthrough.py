import json

from test_cli import run

S = "s1"
DAY0 = "2026-11-09T10:00:00Z"


def call(root, now, *args):
    out = run("--root", str(root), "--now", now, *args, cwd=root)
    assert out.returncode == 0, out.stderr
    return out.stdout if args[0] == "show" else json.loads(out.stdout)


def snapshot(root):
    return {p.name: p.read_text() for p in sorted((root / ".learn").rglob("*.jsonl"))}


def test_two_sessions_build_on_each_other(tmp_path):
    def at(now, *args):
        return call(tmp_path, now, *args)

    def observe(now, kind, slug, grade, confidence, expected=None, **extra):
        rec = {"session": S, "kind": kind, "form": "free", "target": {"type": "slug", "id": slug},
               "prompt": f"Question about {slug}", "expected": expected, "response": "an answer",
               "confidence": confidence, "grade": grade, "produced": True}
        rec.update(extra)
        return at(now, "observe", "--json", json.dumps(rec))["id"]

    def node(name, statement):
        rec = {"name": name, "statement": statement, "claimType": "consensus",
               "status": "tutor-asserted", "source": None, "scope": None, "session": S}
        return at(DAY0, "node", "--json", json.dumps(rec))["id"]

    # Day 0: ground, teach, record.
    at(DAY0, "init")
    o1 = observe(DAY0, "probe", "halving", "missed", "high")
    observe(DAY0, "probe", "depth", "dont_know", "low")
    observe(DAY0, "probe", "logs", "missed", "med")
    at(DAY0, "misconception", "--json", json.dumps({
        "statement": "Binary search checks every element once", "counterpart": "It discards half the range per step",
        "contradicts": [], "evidence": [o1], "stability": "one-off", "kind": "missing-distinction",
        "status": "suspected", "session": S}))
    observe(DAY0, "check", "halving", "took", "med", expected="Half the range remains")
    observe(DAY0, "check", "depth", "took", "med", expected="About log2 n steps")
    observe(DAY0, "final", "logs", "took", "high", expected="Each step halves the remaining range")
    n1 = node("halving", "Each comparison discards half of the remaining range")
    n2 = node("depth", "Halving n items down to one takes about log2 of n steps")
    n3 = node("logn", "Binary search takes a number of comparisons proportional to log2 of n")
    c1 = at(DAY0, "chain", "--json", json.dumps({"premises": [n1, n2], "conclusion": n3, "session": S}))["id"]
    for slug, targets in (("halving", n1), ("depth", n2), ("logs", f"{n3},{c1}")):
        at(DAY0, "link", "--session", S, "--slug", slug, "--targets", targets)

    def states(now):
        return {s["target_id"]: s for s in at(now, "state")}

    st = states(DAY0)
    assert {st[t]["status"] for t in (c1, n1, n2, n3)} == {"taught"}
    assert at("2026-11-09T12:00:00Z", "due") == []
    after_day0 = snapshot(tmp_path)

    # Day 2: review.
    day2 = "2026-11-11T10:00:00Z"
    assert at(day2, "due")[0]["target_id"] == c1
    for target, grade in ((c1, "took"), (n1, "missed")):
        at(day2, "observe", "--json", json.dumps({
            "session": S, "kind": "review", "form": "reconstruct", "target": {"type": "chain" if target == c1 else "node", "id": target},
            "prompt": "Rebuild the argument", "expected": "Halving gives log2 n steps", "response": "my attempt",
            "confidence": "med", "grade": grade, "produced": True}))
    st = states(day2)
    assert st[c1]["status"] == "retained" and st[c1]["due_at"] == "2026-11-14T10:00:00Z"
    assert st[n1]["status"] == "taught" and st[n1]["due_at"] == "2026-11-12T10:00:00Z"

    # Day 3: retract the missed node.
    day3 = "2026-11-12T10:00:00Z"
    at(day3, "edit", "--json", json.dumps({"op": "retract", "target": n1, "reason": "claim was imprecise", "session": S}))
    graph = json.dumps(at(day3, "graph"))
    assert n1 not in graph and c1 not in graph
    assert not {n1, c1} & {d["target_id"] for d in at("2026-11-22T10:00:00Z", "due")}
    shown = at(day3, "show")
    assert "## Misconceptions" in shown and "## Not yet recorded" not in shown
    later = at("2026-11-22T10:00:00Z", "show")  # c1 would be overdue here had it survived
    assert c1 not in later and n1 not in later
    assert {s["target_id"]: s["status"] for s in at(day3, "state")}[c1] == "retracted"

    # Append-only: every file only grew.
    after = snapshot(tmp_path)
    for name, text in after_day0.items():
        assert after[name].startswith(text), name
