"""Append-only JSONL store under a `.learn` directory."""
import json
import os
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

FILES = {
    "observations": "learner/observations.jsonl",
    "misconceptions": "learner/misconceptions.jsonl",
    "links": "learner/links.jsonl",
    "nodes": "graph/nodes.jsonl",
    "chains": "graph/chains.jsonl",
    "edits": "graph/edits.jsonl",
}


# Keys each line must carry to be replayable. Full field rules live in schema.py and apply on write.
_SHAPE = {
    "observations": ("id", "ts", "session", "kind", "target", "grade"),
    "misconceptions": ("id", "ts"),
    "links": ("ts", "session", "slug", "targets"),
    "nodes": ("id", "ts"),
    "chains": ("id", "ts", "premises", "conclusion"),
    "edits": ("ts", "op"),
}
_EDIT_IDS = {"supersede": ("target", "by"), "retract": ("target",), "contradicts": ("a", "b")}
TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
_TS = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


class StoreNotFound(Exception):
    pass


class CorruptStore(Exception):
    pass


def now_ts() -> str:
    return datetime.now(timezone.utc).strftime(TS_FORMAT)


def is_timestamp(value) -> bool:
    """True for an ISO 8601 UTC timestamp with a Z suffix and second precision."""
    if not isinstance(value, str) or not _TS.fullmatch(value):
        return False
    try:
        datetime.strptime(value, TS_FORMAT)
    except ValueError:
        return False
    return True


def init_store(cwd: Path) -> Path:
    root = Path(cwd) / ".learn"
    for rel in FILES.values():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
    (root / "sessions").mkdir(exist_ok=True)
    return root


def _as_store(p: Path) -> Path | None:
    if p.name == ".learn" and p.is_dir():
        return p
    if (p / ".learn").is_dir():
        return p / ".learn"
    return None


def env_root() -> Path | None:
    """The project directory LEARN_ROOT names (it may name the project or its .learn)."""
    env = os.environ.get("LEARN_ROOT")
    if not env:
        return None
    p = Path(env)
    return p.parent if p.name == ".learn" else p


def find_root(start: Path, use_env: bool = True) -> Path:
    """Return the `.learn` directory, searching upward from `start`.

    LEARN_ROOT (project dir or .learn dir) overrides the search unless use_env is False,
    which the CLI passes when --root is given.
    """
    env = os.environ.get("LEARN_ROOT") if use_env else None
    if env:
        found = _as_store(Path(env))
        if found is None:
            raise StoreNotFound(f"no .learn store at LEARN_ROOT={env}")
        return found
    start = Path(start).resolve()
    for d in (start, *start.parents):
        found = _as_store(d)
        if found is not None:
            return found
    raise StoreNotFound(f"no .learn store found from {start}; run `learn.py init`")


def _path(root: Path, file: str) -> Path:
    return Path(root) / FILES[file]


def _shape_error(file: str, rec: dict) -> str | None:
    """Return '<field>: <reason>' when a line cannot be replayed, else None."""
    for f in _SHAPE[file]:
        if f not in rec:
            return f"{f}: required"
    if not is_timestamp(rec["ts"]):
        return "ts: must be a YYYY-MM-DDTHH:MM:SSZ timestamp"
    if file == "observations":
        t = rec["target"]
        if not (isinstance(t, dict) and isinstance(t.get("type"), str) and isinstance(t.get("id"), str)):
            return "target: must be {type, id}"
    if file == "links" and not isinstance(rec["targets"], list):
        return "targets: must be a list"
    if file == "chains" and not isinstance(rec["premises"], list):
        return "premises: must be a list"
    if file == "edits":
        for f in _EDIT_IDS.get(rec["op"], ()):
            if f not in rec:
                return f"{f}: required for op {rec['op']}"
    return None


def read(root: Path, file: str) -> list[dict]:
    path = _path(root, file)
    recs = []
    try:
        fh = open(path, encoding="utf-8")
    except FileNotFoundError:
        raise CorruptStore(f"{FILES[file]}: missing; run `learn.py init` (safe to repeat) to recreate it") from None
    with fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                raise CorruptStore(f"{FILES[file]}:{n}: {e.msg}") from None
            if not isinstance(rec, dict):
                raise CorruptStore(f"{FILES[file]}:{n}: not a JSON object")
            problem = _shape_error(file, rec)
            if problem:
                raise CorruptStore(f"{FILES[file]}:{n}: {problem}")
            recs.append(rec)
    return recs


def append(root: Path, file: str, rec: dict, prefix: str | None,
           now: str | None = None) -> dict:
    out = dict(rec)
    if prefix and "id" not in out:
        out["id"] = f"{prefix}-{secrets.token_hex(4)}"
    out.setdefault("ts", now or now_ts())
    line = json.dumps(out, ensure_ascii=False) + "\n"
    path = _path(root, file)
    with open(path, "ab+") as fh:  # a hand edit may have dropped the last newline
        fh.seek(0, os.SEEK_END)
        if fh.tell():
            fh.seek(-1, os.SEEK_END)
            if fh.read(1) != b"\n":
                line = "\n" + line
        fh.write(line.encode("utf-8"))
    return out
