"""Render the store as a markdown learner-model page. Everything is derived by replay."""
from datetime import datetime, timezone
from pathlib import Path

from . import graph, schedule, store

_CONF = ("high", "med", "low")
_GRADES = ("took", "missed", "dont_know")
_MIS_ORDER = ("suspected", "confirmed", "addressed", "resolved")


def _label(state, nodes, chains):
    """Text naming a target: node statement, chain conclusion statement, else the id."""
    rec = nodes.get(state.target_id)
    if rec is None and state.target_id in chains:
        concl = chains[state.target_id].get("conclusion")
        rec = nodes.get(concl)
        if rec is None:
            return f"{state.target_id} (chain to {concl})"
    if rec is None:
        return state.target_id
    return rec.get("statement") or rec.get("name") or state.target_id


def _days_overdue(due_at, now):
    fmt = store.TS_FORMAT
    delta = datetime.strptime(now, fmt) - datetime.strptime(due_at, fmt)
    return max(delta.days, 0)


def _status_section(title, states, nodes, chains):
    if not states:
        return []
    out = [f"## {title}", ""]
    for s in states:
        out.append(f"- {_label(s, nodes, chains)} ({s.target_id})")
    return out + [""]


def _misconceptions(records):
    latest = {}
    for i, m in enumerate(records):
        latest[m.get("id") or f"_line{i}"] = m  # later lines replace earlier ones
    groups = {}
    for m in latest.values():
        groups.setdefault(m.get("status", "suspected"), []).append(m)
    if not groups:
        return []
    order = [s for s in _MIS_ORDER if s in groups]
    order = [s for s in order if s != "resolved"] + \
        [s for s in groups if s not in _MIS_ORDER] + \
        (["resolved"] if "resolved" in groups else [])
    out = ["## Misconceptions", ""]
    for status in order:
        out.append(f"### {status}")
        for m in groups[status]:
            out.append(f"- {m.get('statement', '(no statement)')}")
        out.append("")
    return out


def _calibration(observations):
    scored = [o for o in observations if not o.get("lowEffort")]
    if not scored:
        return []
    counts = {}
    for o in scored:
        key = (o.get("confidence"), o.get("grade"))
        counts[key] = counts.get(key, 0) + 1
    out = ["## Calibration", "", "| confidence | " + " | ".join(_GRADES) + " |",
           "|---|" + "---|" * len(_GRADES)]
    for c in _CONF:
        out.append(f"| {c} | " + " | ".join(str(counts.get((c, g), 0)) for g in _GRADES) + " |")
    n = counts.get(("high", "missed"), 0)  # a confident "I don't know" is accurate monitoring
    misses = f"{n} high-confidence miss" + ("" if n == 1 else "es")
    return out + ["", f"You gave {misses} (answers marked high confidence that were missed).", ""]


def render(root: Path, now: str) -> str:
    observations = store.read(root, "observations")
    misconceptions = store.read(root, "misconceptions")
    if not observations and not misconceptions:
        return "Nothing recorded yet.\n"
    all_chains, edits = store.read(root, "chains"), store.read(root, "edits")
    nodes, chains = graph.current(store.read(root, "nodes"), all_chains, edits)
    # replay needs every chain, not only active ones, to see a chain whose premise was retracted
    states = schedule.replay(observations, store.read(root, "links"), edits, all_chains)
    out = ["# Learner model", ""]
    due = schedule.due(states, now, limit=len(states))
    if due:
        out += ["## Due now", ""]
        for s in due:
            out.append(f"- {_label(s, nodes, chains)} ({s.target_type} {s.target_id}), "
                       f"{_days_overdue(s.due_at, now)} days overdue")
        out.append("")
    for title, status in (("Retained", "retained"), ("Taught, not yet retained", "taught"),
                          ("Lapsed", "lapsed")):
        out += _status_section(title, [s for s in states.values() if s.status == status],
                               nodes, chains)
    out += _misconceptions(misconceptions)
    out += _calibration(observations)
    unlinked = sorted({s.session for s in states.values() if s.status == "unlinked"})
    if unlinked:
        out += ["## Not yet recorded", "",
                "Observations on these sessions are not linked to graph nodes; "
                "run learn-record for this session:", ""]
        out += [f"- {s}" for s in unlinked] + [""]
    return "\n".join(out).rstrip() + "\n"
