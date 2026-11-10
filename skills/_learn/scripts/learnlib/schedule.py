"""Replay observations into per-target status and a spaced review queue.

The ladder and the delay threshold are design defaults, not research findings.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Sequence

from . import graph

LADDER_DAYS = (1, 3, 7, 21, 60)
MIN_DELAY_HOURS = 8
_FMT = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class TargetState:
    target_id: str
    target_type: str  # slug | node | chain
    status: str  # taught | retained | lapsed | retracted | unlinked | closed
    rung: int
    due_at: str | None
    last_ts: str
    last_grade: str
    events: int
    session: str  # session of the first event


def _parse(ts: str) -> datetime:
    return datetime.strptime(ts, _FMT).replace(tzinfo=timezone.utc)


def _type_of(target_id: str, declared: str) -> str:
    if target_id.startswith("n-"):
        return "node"
    if target_id.startswith("c-"):
        return "chain"
    return declared


def _keys(ob, links, edits, chains):
    """Yield (key, type, fixed) for each target an observation counts toward.

    `fixed` is None for a schedulable target, else the status that holds it off the
    queue: `retracted`, `unlinked` (slug with no link) or `closed` (slug whose links
    all have empty targets).
    """
    t = ob["target"]
    if t["type"] == "slug":
        matched = [l for l in links if l["session"] == ob["session"] and l["slug"] == t["id"]]
        ids = list(dict.fromkeys(i for l in matched for i in l["targets"]))
        if not ids:
            yield f"{ob['session']}/{t['id']}", "slug", "closed" if matched else "unlinked"
            return
    else:
        ids = [t["id"]]
    for raw in ids:
        live = graph.resolve(raw, edits)
        ttype = _type_of(raw, t["type"])
        if live is None:
            yield raw, ttype, "retracted"
            continue
        dead = ttype == "chain" and live in chains and any(
            graph.resolve(m, edits) is None
            for m in [*chains[live]["premises"], chains[live]["conclusion"]])
        yield live, ttype, "retracted" if dead else None


def replay(observations: list, links: list, edits: list,
           chains: Sequence = ()) -> dict:
    chain_by_id = {c["id"]: c for c in chains}
    states: dict = {}
    last_dt: dict = {}
    scored: set = set()
    for ob in sorted(observations, key=lambda o: o["ts"]):  # stable: ties keep file order
        for key, ttype, fixed in _keys(ob, links, edits, chain_by_id):
            st = states.get(key)
            if st is None:
                st = states[key] = TargetState(key, ttype, fixed or "taught", 0, None,
                                               ob["ts"], ob["grade"], 0, ob["session"])
            st.events += 1
            if fixed:  # counted, never scheduled
                st.status = fixed
                continue
            now = _parse(ob["ts"])
            prev = last_dt.get(key)  # the delay clock counts every event, low-effort included
            last_dt[key] = now
            if ob.get("lowEffort"):
                continue
            first = key not in scored  # first non-low-effort event establishes state
            scored.add(key)
            delayed = prev is None or now - prev >= timedelta(hours=MIN_DELAY_HOURS)
            good = ob["grade"] == "took" and ob.get("produced") and not ob.get("hinted")
            if first:
                if good and ob["kind"] in ("probe", "review"):
                    st.status, st.rung = "retained", 1
                else:
                    st.status, st.rung = "taught", 0
            elif delayed:
                if good:
                    st.status, st.rung = "retained", min(st.rung + 1, 4)
                elif ob["grade"] in ("missed", "dont_know"):
                    if st.status == "retained":
                        st.status = "lapsed"
                    st.rung = max(st.rung - 1, 0)
            st.last_ts, st.last_grade = ob["ts"], ob["grade"]
            st.due_at = (now + timedelta(days=LADDER_DAYS[st.rung])).strftime(_FMT)
    return states


def due(states: dict, now: str, limit: int = 8, prefer: Sequence = ()) -> list:
    order = {t: i for i, t in enumerate(prefer)}
    live = [s for s in states.values()
            if s.due_at and s.due_at <= now and s.status not in ("unlinked", "retracted", "closed")]
    live.sort(key=lambda s: (order.get(s.target_id, len(order)),
                             s.target_type != "chain", s.due_at))
    return live[:limit]
