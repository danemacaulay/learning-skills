from learnlib.store import append
from learnlib.view import render


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
    text = render(root, "2026-11-09T00:00:00Z")
    assert "resolved" in text.lower() and "suspected" not in text.lower()


def test_chain_with_a_retracted_premise_is_not_due_or_taught(root, obs):
    a = append(root, "nodes", {"name": "a", "statement": "A holds."}, prefix="n")
    b = append(root, "nodes", {"name": "b", "statement": "B holds."}, prefix="n")
    c = append(root, "chains", {"premises": [a["id"]], "conclusion": b["id"]}, prefix="c")
    append(root, "observations", obs(target={"type": "chain", "id": c["id"]}, ts="2026-11-01T10:00:00Z"),
           prefix="o")
    append(root, "edits", {"op": "retract", "target": a["id"], "reason": "wrong", "ts": "2026-11-02T10:00:00Z"},
           prefix=None)
    text = render(root, "2026-11-20T00:00:00Z")
    assert c["id"] not in text


def test_confident_dont_know_is_not_counted_as_a_miss(root, obs):
    append(root, "observations", obs(confidence="high", grade="dont_know"), prefix="o")
    text = render(root, "2026-11-09T00:00:00Z")
    assert "0 high-confidence misses" in text
