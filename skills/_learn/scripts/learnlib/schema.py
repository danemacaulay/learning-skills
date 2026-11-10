"""Record validation. Messages start with the offending field name."""
import re

from .store import is_timestamp

KINDS = ("probe", "check", "review", "final")
FORMS = ("mc", "free", "predict", "explain-why", "apply", "reconstruct",
         "counterfactual", "discriminate", "teach-back", "transfer")
CONFIDENCE = ("low", "med", "high", "not_given")
GRADES = ("took", "missed", "dont_know")
TARGET_TYPES = ("slug", "node", "chain")
STABILITY = ("stable", "shifting", "one-off")
MISCONCEPTION_KINDS = ("category-error", "missing-distinction", "overgeneralized-fragment")
STATUSES = ("suspected", "confirmed", "addressed", "resolved")

_OBS_REQUIRED = ("session", "kind", "form", "target", "prompt", "expected",
                 "response", "confidence", "grade", "produced")
_OBS_OPTIONAL = ("hinted", "lowEffort", "misconception", "id", "ts")
_MIS_REQUIRED = ("statement", "counterpart", "contradicts", "evidence",
                 "stability", "kind", "status", "session")
_MIS_OPTIONAL = ("id", "ts")

CLAIM_TYPES = ("definition", "result", "attribution", "consensus", "interpretation")
NODE_STATUS = ("source-verified", "tutor-asserted", "contested")
EDIT_OPS = ("supersede", "retract", "contradicts")
COMPOUND_MARKERS = (" because ", " therefore ", " hence ", " which means ")

_NODE_REQUIRED = ("name", "statement", "claimType", "status", "source", "scope", "session")
_CHAIN_REQUIRED = ("premises", "conclusion", "session")
_EDIT_FIELDS = {"supersede": ("target", "by", "reason", "session"),
                "retract": ("target", "reason", "session"),
                "contradicts": ("a", "b", "reason", "session")}
_KEBAB = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")

_O_ID = re.compile(r"o-[0-9a-f]{8}")
_M_ID = re.compile(r"m-[0-9a-f]{8}")


class ValidationError(ValueError):
    pass


def _check_keys(rec, required, optional):
    if not isinstance(rec, dict):
        raise ValidationError("record: must be a JSON object")
    for f in required:
        if f not in rec:
            raise ValidationError(f"{f}: required")
    for f in rec:
        if f not in required and f not in optional:
            raise ValidationError(f"{f}: unknown field")
    if "ts" in rec and not is_timestamp(rec["ts"]):
        raise ValidationError("ts: must be a YYYY-MM-DDTHH:MM:SSZ timestamp")


def _nonempty_str(rec, f):
    if not isinstance(rec[f], str) or not rec[f].strip():
        raise ValidationError(f"{f}: must be a non-empty string")


def _one_of(rec, f, allowed):
    if rec[f] not in allowed:
        raise ValidationError(f"{f}: must be one of {', '.join(allowed)}")


def _str_list(rec, f, min_len=0):
    v = rec[f]
    if not isinstance(v, list) or not all(isinstance(x, str) and x for x in v):
        raise ValidationError(f"{f}: must be a list of non-empty strings")
    if len(v) < min_len:
        raise ValidationError(f"{f}: needs at least {min_len} entries")


def validate_observation(rec: dict) -> dict:
    _check_keys(rec, _OBS_REQUIRED, _OBS_OPTIONAL)
    out = dict(rec)
    _nonempty_str(out, "session")
    _one_of(out, "kind", KINDS)
    _one_of(out, "form", FORMS)
    t = out["target"]
    if (not isinstance(t, dict) or set(t) != {"type", "id"}
            or t["type"] not in TARGET_TYPES
            or not isinstance(t["id"], str) or not t["id"]):
        raise ValidationError("target: must be {type: slug|node|chain, id: str}")
    _nonempty_str(out, "prompt")
    if out["expected"] is not None and not isinstance(out["expected"], str):
        raise ValidationError("expected: must be a string or null")
    if out["kind"] in ("check", "review", "final") and not (
            isinstance(out["expected"], str) and out["expected"].strip()):
        raise ValidationError(f"expected: required (pre-committed answer) for kind {out['kind']}")
    if not isinstance(out["response"], str):
        raise ValidationError("response: must be a string")
    _one_of(out, "confidence", CONFIDENCE)
    _one_of(out, "grade", GRADES)
    out.setdefault("hinted", False)
    out.setdefault("lowEffort", False)
    for f in ("produced", "hinted", "lowEffort"):
        if not isinstance(out[f], bool):
            raise ValidationError(f"{f}: must be a boolean")
    if "misconception" in out and not (
            isinstance(out["misconception"], str) and _M_ID.fullmatch(out["misconception"])):
        raise ValidationError("misconception: must be an m- id")
    return out


def validate_misconception(rec: dict) -> dict:
    _check_keys(rec, _MIS_REQUIRED, _MIS_OPTIONAL)
    out = dict(rec)
    for f in ("statement", "counterpart", "session"):
        _nonempty_str(out, f)
    _str_list(out, "contradicts")
    _str_list(out, "evidence", min_len=1)
    if not all(_O_ID.fullmatch(e) for e in out["evidence"]):
        raise ValidationError("evidence: entries must be o- ids")
    _one_of(out, "stability", STABILITY)
    _one_of(out, "kind", MISCONCEPTION_KINDS)
    _one_of(out, "status", STATUSES)
    if out["status"] != "suspected" and len(set(out["evidence"])) < 2:
        raise ValidationError(f"evidence: status {out['status']} needs at least two evidence ids")
    return out


def _str_or_null(rec, f):
    if rec[f] is not None and not (isinstance(rec[f], str) and rec[f].strip()):
        raise ValidationError(f"{f}: must be a non-empty string or null")


def validate_node(rec: dict) -> dict:
    _check_keys(rec, _NODE_REQUIRED, ("id", "ts"))
    out = dict(rec)
    for f in ("name", "statement", "session"):
        _nonempty_str(out, f)
    if not _KEBAB.fullmatch(out["name"]):
        raise ValidationError("name: must be kebab-case")
    _one_of(out, "claimType", CLAIM_TYPES)
    _one_of(out, "status", NODE_STATUS)
    _str_or_null(out, "source")
    _str_or_null(out, "scope")
    padded = f" {out['statement'].lower()} "
    if any(m in padded for m in COMPOUND_MARKERS):
        raise ValidationError("statement: compound claim; split it into premise nodes and a chain")
    if out["source"] is None and (out["status"] == "source-verified"
                                  or out["claimType"] == "attribution"):
        raise ValidationError("source: required when status is source-verified or claimType is attribution")
    if out["scope"] is None and out["claimType"] == "interpretation":
        raise ValidationError("scope: required for an interpretation (according to which text or reading)")
    return out


def _known_id(rec, f, known):
    if not isinstance(rec[f], str) or rec[f] not in known:
        raise ValidationError(f"{f}: unknown id {rec[f]!r}")


def validate_chain(rec: dict, known: set) -> dict:
    _check_keys(rec, _CHAIN_REQUIRED, ("id", "ts"))
    out = dict(rec)
    _nonempty_str(out, "session")
    _str_list(out, "premises", min_len=1)
    if len(set(out["premises"])) != len(out["premises"]):
        raise ValidationError("premises: duplicate ids")
    for p in out["premises"]:
        if not p.startswith("n-"):
            raise ValidationError(f"premises: {p!r} is not a node id; premises are n- ids")
        if p not in known:
            raise ValidationError(f"premises: unknown id {p!r}")
    _nonempty_str(out, "conclusion")
    if out["conclusion"] in out["premises"]:
        raise ValidationError("conclusion: must not be one of the premises")
    if not out["conclusion"].startswith("n-"):
        raise ValidationError(f"conclusion: {out['conclusion']!r} is not a node id")
    _known_id(out, "conclusion", known)
    return out


def _closes_cycle(target, by, edits):
    """True when following the existing supersedes from `by` leads back to `target`."""
    sup = {e["target"]: e["by"] for e in edits if e.get("op") == "supersede"}
    seen, cur = set(), by
    while cur in sup and cur not in seen:
        seen.add(cur)
        cur = sup[cur]
        if cur == target:
            return True
    return False


def validate_edit(rec: dict, known: set, edits: list = ()) -> dict:
    if not isinstance(rec, dict):
        raise ValidationError("record: must be a JSON object")
    if rec.get("op") not in EDIT_OPS:
        raise ValidationError(f"op: must be one of {', '.join(EDIT_OPS)}")
    fields = _EDIT_FIELDS[rec["op"]]
    _check_keys(rec, ("op", *fields), ("id", "ts"))
    out = dict(rec)
    for f in fields:
        _nonempty_str(out, f)
    for f in ("target", "by", "a", "b"):
        if f in out:
            _known_id(out, f, known)
    if out["op"] == "supersede":
        if out["by"] == out["target"]:
            raise ValidationError("by: must differ from target")
        if out["by"][:2] != out["target"][:2]:
            raise ValidationError("by: a node is superseded by a node, a chain by a chain")
        if _closes_cycle(out["target"], out["by"], edits):
            raise ValidationError(f"by: {out['by']} already leads back to {out['target']}; "
                                  "this supersede would close a cycle")
    if out["op"] == "contradicts" and out["a"] == out["b"]:
        raise ValidationError("b: must differ from a")
    return out
