"""Replay nodes, chains and edits into the current graph view."""
import re
from typing import Iterable


def _latest_supersedes(edits):
    return {e["target"]: e["by"] for e in edits if e.get("op") == "supersede"}


def _retracted(edits):
    return {e["target"] for e in edits if e.get("op") == "retract"}


def _resolve(target_id, supersedes, retracted):
    seen = set()
    while True:
        if target_id in retracted:
            return None
        nxt = supersedes.get(target_id)
        if nxt is None or target_id in seen:
            return target_id
        seen.add(target_id)
        target_id = nxt


def resolve(target_id: str, edits: list) -> str | None:
    """Follow supersede edits to the live id; None when it (or its replacement) is retracted."""
    return _resolve(target_id, _latest_supersedes(edits), _retracted(edits))


def current(nodes: list, chains: list, edits: list) -> tuple:
    sup, ret = _latest_supersedes(edits), _retracted(edits)
    active_nodes = {n["id"]: n for n in nodes
                    if n["id"] not in sup and n["id"] not in ret}
    active_chains = {}
    for c in chains:
        if c["id"] in sup or c["id"] in ret:
            continue
        prem = [_resolve(p, sup, ret) for p in c["premises"]]
        concl = _resolve(c["conclusion"], sup, ret)
        if concl is None or None in prem:
            continue
        prem = list(dict.fromkeys(prem))
        active_chains[c["id"]] = {**c, "premises": prem, "conclusion": concl}
    return active_nodes, active_chains


def _words(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 3}


def candidates(statement: str, nodes: Iterable, k: int = 5, threshold: float = 0.2) -> list:
    query = _words(statement)
    scored = []
    for n in nodes:
        words = _words(f"{n.get('name', '')} {n.get('statement', '')}")
        union = query | words
        score = len(query & words) / len(union) if union else 0.0
        if score >= threshold:
            scored.append((n["id"], score))
    scored.sort(key=lambda t: -t[1])
    return scored[:k]
