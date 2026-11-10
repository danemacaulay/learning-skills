import json
import subprocess
import sys
from pathlib import Path

import pytest

LEARN = Path(__file__).resolve().parents[2] / "skills" / "_learn" / "scripts" / "learn.py"


def run(*args, cwd):
    return subprocess.run([sys.executable, str(LEARN), *args], cwd=cwd,
                          capture_output=True, text=True)


def test_observe_appends_and_prints_id(tmp_path, obs):
    run("init", cwd=tmp_path)
    out = run("observe", "--json", json.dumps(obs()), cwd=tmp_path)
    assert out.returncode == 0 and json.loads(out.stdout)["id"].startswith("o-")


def test_now_sets_timestamp(tmp_path, obs):
    run("init", cwd=tmp_path)
    out = run("--now", "2026-11-09T22:19:00Z", "observe", "--json", json.dumps(obs()), cwd=tmp_path)
    assert json.loads(out.stdout)["ts"] == "2026-11-09T22:19:00Z"


def test_invalid_observation_exits_2_and_appends_nothing(tmp_path, obs):
    run("init", cwd=tmp_path)
    out = run("observe", "--json", json.dumps(obs(grade="partial")), cwd=tmp_path)
    assert out.returncode == 2 and "grade" in out.stderr
    assert (tmp_path / ".learn/learner/observations.jsonl").read_text() == ""


def test_corrupt_store_exits_2_without_appending(tmp_path, obs):
    run("init", cwd=tmp_path)
    f = tmp_path / ".learn/learner/observations.jsonl"
    f.write_text("{broken\n")
    out = run("observe", "--json", json.dumps(obs()), cwd=tmp_path)
    assert out.returncode == 2 and "observations.jsonl:1" in out.stderr
    assert f.read_text() == "{broken\n"


def test_bad_json_exits_2(tmp_path):
    run("init", cwd=tmp_path)
    out = run("observe", "--json", "{nope", cwd=tmp_path)
    assert out.returncode == 2 and out.stdout == ""


def test_no_store_exits_2(tmp_path, obs):
    out = run("observe", "--json", json.dumps(obs()), cwd=tmp_path)
    assert out.returncode == 2 and out.stderr.strip()


def test_root_option(tmp_path, obs):
    run("init", cwd=tmp_path)
    other = tmp_path / "x"
    other.mkdir()
    out = run("--root", str(tmp_path), "observe", "--json", json.dumps(obs()), cwd=other)
    assert out.returncode == 0


MIS = {"statement": "s", "counterpart": "c", "contradicts": [], "evidence": ["o-00000001"],
       "stability": "stable", "kind": "category-error", "status": "suspected", "session": "s1"}


def test_misconception_appends_and_update_reuses_id(tmp_path):
    run("init", cwd=tmp_path)
    first = json.loads(run("misconception", "--json", json.dumps(MIS), cwd=tmp_path).stdout)
    assert first["id"].startswith("m-")
    upd = {**MIS, "id": first["id"], "evidence": ["o-00000001", "o-00000002"], "status": "confirmed"}
    out = run("misconception", "--json", json.dumps(upd), cwd=tmp_path)
    assert out.returncode == 0
    lines = (tmp_path / ".learn/learner/misconceptions.jsonl").read_text().splitlines()
    assert len(lines) == 2


def test_importable_without_side_effects():
    sys.path.insert(0, str(LEARN.parent))
    import learn
    assert {"init", "observe", "misconception"} <= set(learn.SUBCOMMANDS)


def _node(**kw):
    base = {"name": "ready-to-hand", "statement": "Equipment in use is ready-to-hand.",
            "claimType": "definition", "status": "tutor-asserted", "source": None,
            "scope": None, "session": "s"}
    base.update(kw)
    return json.dumps(base)


def test_chain_with_unknown_node_exits_2(tmp_path):
    run("init", cwd=tmp_path)
    out = run("chain", "--json", '{"premises":["n-deadbeef"],"conclusion":"n-00000000","session":"s"}', cwd=tmp_path)
    assert out.returncode == 2


def test_graph_round_trip_supersede_and_candidates(tmp_path):
    run("init", cwd=tmp_path)
    a = json.loads(run("node", "--json", _node(), cwd=tmp_path).stdout)["id"]
    b = json.loads(run("node", "--json", _node(name="presence-at-hand",
                                               statement="Objects merely beheld are present-at-hand."),
                       cwd=tmp_path).stdout)["id"]
    c = json.loads(run("chain", "--json", json.dumps({"premises": [a], "conclusion": b, "session": "s"}),
                       cwd=tmp_path).stdout)["id"]
    assert c.startswith("c-")
    cand = json.loads(run("candidates", "--statement", "equipment ready-to-hand", cwd=tmp_path).stdout)
    assert cand[0]["id"] == a
    n2 = json.loads(run("node", "--json", _node(name="ready-to-hand-2"), cwd=tmp_path).stdout)["id"]
    e = run("edit", "--json", json.dumps({"op": "supersede", "target": a, "by": n2, "reason": "r",
                                          "session": "s"}), cwd=tmp_path)
    assert e.returncode == 0
    g = json.loads(run("graph", cwd=tmp_path).stdout)
    assert {n["id"] for n in g["nodes"]} == {b, n2}
    assert g["chains"][0]["premises"] == [n2]


def test_edit_with_unknown_target_exits_2(tmp_path):
    run("init", cwd=tmp_path)
    out = run("edit", "--json", '{"op":"retract","target":"n-00000000","reason":"r","session":"s"}', cwd=tmp_path)
    assert out.returncode == 2


def test_due_cli_round_trip(tmp_path, obs):
    run("init", cwd=tmp_path)
    run("--now", "2026-11-09T10:00:00Z", "observe", "--json",
        json.dumps(obs(target={"type": "node", "id": "n-00000001"})), cwd=tmp_path)
    out = run("--now", "2026-11-11T10:00:00Z", "due", cwd=tmp_path)
    assert [s["target_id"] for s in json.loads(out.stdout)] == ["n-00000001"]


def test_link_rejects_unknown_target_and_state_follows_links(tmp_path, obs):
    run("init", cwd=tmp_path)
    bad = run("link", "--session", "20261109-demo", "--slug", "ready-to-hand",
              "--targets", "n-00000001", cwd=tmp_path)
    assert bad.returncode == 2 and bad.stdout == ""
    nid = json.loads(run("node", "--json", _node(), cwd=tmp_path).stdout)["id"]
    ok = run("link", "--session", "20261109-demo", "--slug", "ready-to-hand",
             "--targets", nid, cwd=tmp_path)
    assert ok.returncode == 0
    run("--now", "2026-11-09T10:00:00Z", "observe", "--json", json.dumps(obs()), cwd=tmp_path)
    states = json.loads(run("state", "--target", nid, cwd=tmp_path).stdout)
    assert [s["target_id"] for s in states] == [nid]


def test_misconceptions_latest_line_per_id_wins_in_first_seen_order(tmp_path):
    run("init", cwd=tmp_path)
    a = json.loads(run("misconception", "--json", json.dumps(MIS), cwd=tmp_path).stdout)
    b = json.loads(run("misconception", "--json", json.dumps({**MIS, "statement": "other"}), cwd=tmp_path).stdout)
    upd = {**MIS, "id": a["id"], "evidence": ["o-00000001", "o-00000002"], "status": "confirmed"}
    run("misconception", "--json", json.dumps(upd), cwd=tmp_path)
    out = json.loads(run("misconceptions", cwd=tmp_path).stdout)
    assert [m["id"] for m in out] == [a["id"], b["id"]]
    assert out[0]["status"] == "confirmed" and out[1]["status"] == "suspected"


def test_misconceptions_status_filter_uses_latest_status(tmp_path):
    run("init", cwd=tmp_path)
    a = json.loads(run("misconception", "--json", json.dumps(MIS), cwd=tmp_path).stdout)
    run("misconception", "--json", json.dumps({**MIS, "statement": "other"}), cwd=tmp_path)
    upd = {**MIS, "id": a["id"], "evidence": ["o-00000001", "o-00000002"], "status": "confirmed"}
    run("misconception", "--json", json.dumps(upd), cwd=tmp_path)
    assert [m["id"] for m in json.loads(run("misconceptions", "--status", "confirmed", cwd=tmp_path).stdout)] == [a["id"]]
    assert len(json.loads(run("misconceptions", "--status", "suspected", cwd=tmp_path).stdout)) == 1


def test_misconceptions_empty_store_prints_empty_list(tmp_path):
    run("init", cwd=tmp_path)
    out = run("misconceptions", cwd=tmp_path)
    assert out.returncode == 0 and json.loads(out.stdout) == []


def _ok(out):
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def _fails_cleanly(out, *needles):
    assert out.returncode == 2 and out.stdout == "", (out.returncode, out.stdout, out.stderr)
    assert len(out.stderr.strip().splitlines()) == 1 and "Traceback" not in out.stderr, out.stderr
    for n in needles:
        assert n in out.stderr, out.stderr


def test_link_none_closes_a_slug_and_a_later_link_reopens_it(tmp_path, obs):
    run("init", cwd=tmp_path)
    run("--now", "2026-11-09T10:00:00Z", "observe", "--json",
        json.dumps(obs(kind="probe", target={"type": "slug", "id": "side"})), cwd=tmp_path)
    rec = _ok(run("link", "--session", "20261109-demo", "--slug", "side", "--none",
                  "--reason", "probed strand never taught", cwd=tmp_path))
    assert rec["targets"] == [] and rec["reason"] == "probed strand never taught"
    assert [s["status"] for s in _ok(run("state", cwd=tmp_path))] == ["closed"]
    assert _ok(run("--now", "2027-01-01T00:00:00Z", "due", cwd=tmp_path)) == []
    shown = run("--now", "2027-01-01T00:00:00Z", "show", cwd=tmp_path).stdout
    assert "Not yet recorded" not in shown
    nid = _ok(run("node", "--json", _node(), cwd=tmp_path))["id"]
    _ok(run("link", "--session", "20261109-demo", "--slug", "side", "--targets", nid, cwd=tmp_path))
    assert [s["target_id"] for s in _ok(run("state", cwd=tmp_path))] == [nid]


def test_link_none_needs_a_reason_and_excludes_targets(tmp_path):
    run("init", cwd=tmp_path)
    nid = _ok(run("node", "--json", _node(), cwd=tmp_path))["id"]
    _fails_cleanly(run("link", "--session", "s", "--slug", "x", "--none", cwd=tmp_path), "--reason")
    _fails_cleanly(run("link", "--session", "s", "--slug", "x", "--none", "--reason", "r",
                       "--targets", nid, cwd=tmp_path), "--targets")
    _fails_cleanly(run("link", "--session", "s", "--slug", "x", cwd=tmp_path), "--targets")
    _fails_cleanly(run("link", "--session", "s", "--slug", "x", "--targets", nid, "--reason", "r",
                       cwd=tmp_path), "--reason")
    assert (tmp_path / ".learn/learner/links.jsonl").read_text() == ""


def test_observations_filters_by_session_and_target(tmp_path, obs):
    run("init", cwd=tmp_path)
    a = _ok(run("observe", "--json", json.dumps(obs()), cwd=tmp_path))
    b = _ok(run("observe", "--json", json.dumps(obs(session="other")), cwd=tmp_path))
    c = _ok(run("observe", "--json", json.dumps(obs(target={"type": "node", "id": "n-00000001"})), cwd=tmp_path))
    ids = lambda *args: [o["id"] for o in _ok(run("observations", *args, cwd=tmp_path))]
    assert ids() == [a["id"], b["id"], c["id"]]
    assert ids("--session", "20261109-demo") == [a["id"], c["id"]]
    assert ids("--target", "ready-to-hand") == [a["id"], b["id"]]
    assert ids("--session", "other", "--target", "ready-to-hand") == [b["id"]]
    assert ids("--target", "n-00000001") == [c["id"]]
    assert _ok(run("observations", "--target", "nothing", cwd=tmp_path)) == []


@pytest.mark.parametrize("now", ["tomorrow", "2026-11-20", "soon", "2026-11-09T22:19:00"])
@pytest.mark.parametrize("cmd", [("due",), ("show",), ("state",)])
def test_bad_now_is_rejected_before_anything_runs(tmp_path, now, cmd):
    run("init", cwd=tmp_path)
    _fails_cleanly(run("--now", now, *cmd, cwd=tmp_path), "--now")


def test_bad_now_is_not_stored(tmp_path, obs):
    run("init", cwd=tmp_path)
    _fails_cleanly(run("--now", "tomorrow", "observe", "--json", json.dumps(obs()), cwd=tmp_path), "--now")
    _fails_cleanly(run("observe", "--json", json.dumps(obs(ts="tomorrow")), cwd=tmp_path), "ts")
    assert (tmp_path / ".learn/learner/observations.jsonl").read_text() == ""


READERS = [("observe", "--json", "{}"), ("misconception", "--json", "{}"), ("misconceptions",),
           ("node", "--json", "{}"), ("chain", "--json", "{}"), ("edit", "--json", "{}"),
           ("candidates", "--statement", "x"), ("graph",), ("observations",),
           ("link", "--session", "s", "--slug", "x", "--none", "--reason", "r"),
           ("state",), ("due",), ("show",)]


@pytest.mark.parametrize("line", ["{broken\n", '{"id": "o-00000001", "ts": "tomorrow"}\n', "[1]\n"])
@pytest.mark.parametrize("cmd", READERS, ids=lambda c: c[0])
def test_every_command_rejects_a_corrupt_or_wrong_shape_line(tmp_path, cmd, line):
    run("init", cwd=tmp_path)
    for rel in ("learner/observations.jsonl", "learner/misconceptions.jsonl", "learner/links.jsonl",
                "graph/nodes.jsonl", "graph/chains.jsonl", "graph/edits.jsonl"):
        (tmp_path / ".learn" / rel).write_text(line)
    _fails_cleanly(run(*cmd, cwd=tmp_path), ".jsonl:1: ")
    for rel in ("learner/observations.jsonl", "learner/links.jsonl", "graph/nodes.jsonl"):
        assert (tmp_path / ".learn" / rel).read_text() == line


def test_missing_store_file_names_it_and_init_recreates_it(tmp_path, obs):
    run("init", cwd=tmp_path)
    (tmp_path / ".learn/learner/links.jsonl").unlink()
    _fails_cleanly(run("state", cwd=tmp_path), "learner/links.jsonl", "learn.py init")
    _ok(run("init", cwd=tmp_path))
    assert _ok(run("state", cwd=tmp_path)) == []


def test_supplied_id_must_be_new_and_well_formed(tmp_path, obs):
    run("init", cwd=tmp_path)
    nid = _ok(run("node", "--json", _node(), cwd=tmp_path))["id"]
    _fails_cleanly(run("node", "--json", _node(id=nid, statement="Something else."), cwd=tmp_path), "id")
    _fails_cleanly(run("node", "--json", _node(id="n-xyz"), cwd=tmp_path), "id")
    _fails_cleanly(run("node", "--json", _node(id="c-00000001"), cwd=tmp_path), "id")
    oid = _ok(run("observe", "--json", json.dumps(obs()), cwd=tmp_path))["id"]
    _fails_cleanly(run("observe", "--json", json.dumps(obs(id=oid)), cwd=tmp_path), "id")
    n2 = _ok(run("node", "--json", _node(name="b", statement="B holds."), cwd=tmp_path))["id"]
    cid = _ok(run("chain", "--json", json.dumps({"premises": [nid], "conclusion": n2, "session": "s"}),
                  cwd=tmp_path))["id"]
    _fails_cleanly(run("chain", "--json", json.dumps({"id": cid, "premises": [nid], "conclusion": n2,
                                                      "session": "s"}), cwd=tmp_path), "id")
    assert len((tmp_path / ".learn/graph/nodes.jsonl").read_text().splitlines()) == 2


def test_misconception_id_must_already_exist(tmp_path):
    run("init", cwd=tmp_path)
    _fails_cleanly(run("misconception", "--json", json.dumps({**MIS, "id": "m-0000abcd"}), cwd=tmp_path), "id")
    _fails_cleanly(run("misconception", "--json", json.dumps({**MIS, "id": "m-bad"}), cwd=tmp_path), "id")
    assert (tmp_path / ".learn/learner/misconceptions.jsonl").read_text() == ""


def test_supersede_reversal_is_rejected(tmp_path):
    run("init", cwd=tmp_path)
    a = _ok(run("node", "--json", _node(), cwd=tmp_path))["id"]
    b = _ok(run("node", "--json", _node(name="b", statement="B holds."), cwd=tmp_path))["id"]
    sup = lambda t, by: run("edit", "--json", json.dumps({"op": "supersede", "target": t, "by": by,
                                                          "reason": "r", "session": "s"}), cwd=tmp_path)
    _ok(sup(a, b))
    _fails_cleanly(sup(b, a), "cycle")
    assert [n["id"] for n in _ok(run("graph", cwd=tmp_path))["nodes"]] == [b]


def test_root_wins_over_learn_root_and_init_honours_both(tmp_path, monkeypatch, obs):
    proj, env = tmp_path / "proj", tmp_path / "env"
    proj.mkdir(), env.mkdir()
    monkeypatch.setenv("LEARN_ROOT", str(env))
    _ok(run("init", cwd=tmp_path))
    assert (env / ".learn/learner/observations.jsonl").exists() and not (tmp_path / ".learn").exists()
    _ok(run("--root", str(proj), "init", cwd=tmp_path))
    _ok(run("--root", str(proj), "observe", "--json", json.dumps(obs()), cwd=tmp_path))
    assert (proj / ".learn/learner/observations.jsonl").read_text().strip()
    assert (env / ".learn/learner/observations.jsonl").read_text() == ""


def test_due_limit_below_one_is_rejected(tmp_path):
    run("init", cwd=tmp_path)
    for n in ("0", "-1"):
        _fails_cleanly(run("due", "--limit", n, cwd=tmp_path), "limit")


def test_show_cli_does_not_list_a_chain_whose_premise_was_retracted(tmp_path, obs):
    run("init", cwd=tmp_path)
    a = _ok(run("node", "--json", _node(), cwd=tmp_path))["id"]
    b = _ok(run("node", "--json", _node(name="b", statement="B holds."), cwd=tmp_path))["id"]
    c = _ok(run("chain", "--json", json.dumps({"premises": [a], "conclusion": b, "session": "s"}),
                cwd=tmp_path))["id"]
    run("--now", "2026-11-01T10:00:00Z", "observe", "--json",
        json.dumps(obs(target={"type": "chain", "id": c})), cwd=tmp_path)
    _ok(run("edit", "--json", json.dumps({"op": "retract", "target": a, "reason": "r", "session": "s"}),
            cwd=tmp_path))
    assert _ok(run("--now", "2026-11-20T00:00:00Z", "due", cwd=tmp_path)) == []
    assert _ok(run("state", "--target", c, cwd=tmp_path))[0]["status"] == "retracted"
    shown = run("--now", "2026-11-20T00:00:00Z", "show", cwd=tmp_path)
    assert shown.returncode == 0 and c not in shown.stdout


def test_link_none_on_an_already_linked_slug_is_rejected(tmp_path):
    run("init", cwd=tmp_path)
    nid = _ok(run("node", "--json", _node(), cwd=tmp_path))["id"]
    _ok(run("link", "--session", "20261109-demo", "--slug", "side", "--targets", nid, cwd=tmp_path))
    before = (tmp_path / ".learn/learner/links.jsonl").read_text()
    out = run("link", "--session", "20261109-demo", "--slug", "side", "--none",
              "--reason", "changed my mind", cwd=tmp_path)
    assert out.returncode == 2 and "already linked" in out.stderr
    assert (tmp_path / ".learn/learner/links.jsonl").read_text() == before
