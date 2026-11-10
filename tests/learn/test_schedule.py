import pytest

from learnlib.schedule import due, replay


def ev(ts, target="n-1", ttype="node", **kw):
    base = {"ts": ts, "session": "20261109-demo", "kind": "check", "form": "apply",
            "target": {"type": ttype, "id": target}, "prompt": "p", "expected": "e",
            "response": "r", "confidence": "med", "grade": "took", "produced": True,
            "hinted": False, "lowEffort": False}
    base.update(kw)
    return base


def test_in_session_check_is_taught_and_due_next_day():
    s = replay([ev("2026-11-09T10:00:00Z")], [], [])["n-1"]
    assert (s.status, s.rung, s.due_at) == ("taught", 0, "2026-11-10T10:00:00Z")


def test_delayed_success_becomes_retained_and_climbs():
    s = replay([ev("2026-11-09T10:00:00Z"),
                ev("2026-11-10T10:00:00Z", kind="review", form="reconstruct")], [], [])["n-1"]
    assert (s.status, s.rung, s.due_at) == ("retained", 1, "2026-11-13T10:00:00Z")


def test_same_sitting_reask_does_not_climb():
    s = replay([ev("2026-11-09T10:00:00Z"), ev("2026-11-09T10:20:00Z"),
                ev("2026-11-09T10:40:00Z")], [], [])["n-1"]
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
    s = replay([ev("2026-11-09T10:00:00Z"), ev("2026-11-10T10:00:00Z", lowEffort=True)],
               [], [])["n-1"]
    assert (s.status, s.events) == ("taught", 2)


def test_slug_events_follow_links_and_unlinked_are_flagged():
    evs = [ev("2026-11-09T10:00:00Z", target="tool-use", ttype="slug", session="s1")]
    assert replay(evs, [], [])["s1/tool-use"].status == "unlinked"
    linked = replay(evs, [{"session": "s1", "slug": "tool-use", "targets": ["n-1", "c-1"]}], [])
    assert set(linked) == {"n-1", "c-1"} and linked["c-1"].target_type == "chain"


def test_superseded_history_carries_over_and_retracted_is_never_due():
    evs = [ev("2026-11-09T10:00:00Z"), ev("2026-11-10T10:00:00Z", kind="review")]
    before = replay(evs, [], [])["n-1"]
    after = replay(evs, [], [{"op": "supersede", "target": "n-1", "by": "n-2"}])
    assert set(after) == {"n-2"}
    carried = after["n-2"]
    assert (carried.status, carried.rung, carried.due_at, carried.events) == \
        (before.status, before.rung, before.due_at, before.events) == ("retained", 1, "2026-11-13T10:00:00Z", 2)
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


def test_low_effort_event_resets_the_delay_clock():
    evs = [ev("2026-11-09T10:00:00Z"), ev("2026-11-10T10:00:00Z", lowEffort=True),
           ev("2026-11-10T10:05:00Z")]
    s = replay(evs, [], [])["n-1"]
    assert (s.status, s.rung) == ("taught", 0)


def test_low_effort_first_event_does_not_establish_state():
    evs = [ev("2026-11-09T10:00:00Z", lowEffort=True),
           ev("2026-11-12T10:00:00Z", kind="probe", form="free")]
    s = replay(evs, [], [])["n-1"]
    assert (s.status, s.rung, s.events) == ("retained", 1, 2)


def test_due_never_lists_unlinked_slugs():
    evs = [ev("2026-11-01T10:00:00Z", target="tool-use", ttype="slug", session="s1"),
           ev("2026-11-01T10:00:00Z", target="n-1")]
    states = replay(evs, [], [])
    assert states["s1/tool-use"].status == "unlinked"
    assert [s.target_id for s in due(states, "2027-01-01T00:00:00Z")] == ["n-1"]


def test_due_lists_oldest_due_first_within_a_type():
    evs = [ev("2026-11-05T10:00:00Z", target="n-new"), ev("2026-11-01T10:00:00Z", target="n-old"),
           ev("2026-11-03T10:00:00Z", target="n-mid")]
    assert [s.target_id for s in due(replay(evs, [], []), "2026-12-01T00:00:00Z")] == ["n-old", "n-mid", "n-new"]


def test_slug_closed_by_an_empty_link_is_never_due_and_reopens_with_targets():
    evs = [ev("2026-11-01T10:00:00Z", target="side-topic", ttype="slug", session="s1")]
    closed = [{"session": "s1", "slug": "side-topic", "targets": [], "reason": "probed, never taught"}]
    states = replay(evs, closed, [])
    assert states["s1/side-topic"].status == "closed" and states["s1/side-topic"].due_at is None
    assert due(states, "2027-01-01T00:00:00Z") == []
    reopened = replay(evs, closed + [{"session": "s1", "slug": "side-topic", "targets": ["n-1"]}], [])
    assert set(reopened) == {"n-1"} and reopened["n-1"].status == "taught"
