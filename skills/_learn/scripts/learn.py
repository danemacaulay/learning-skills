#!/usr/bin/env python3
"""CLI over the append-only .learn store. Prints JSON on stdout; errors go to stderr, exit 2."""
import argparse
import dataclasses
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from learnlib import graph, schedule, schema, store, view  # noqa: E402

SUBCOMMANDS = ("init", "observe", "misconception", "misconceptions", "node", "chain", "edit", "candidates", "graph",
               "link", "observations", "state", "due", "show")


class CliError(Exception):
    pass


def _parse_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise CliError(f"--json: invalid JSON: {e.msg}")


def _locate(args):
    if args.root:  # an explicit --root wins over LEARN_ROOT
        return store.find_root(Path(args.root), use_env=False)
    return store.find_root(Path.cwd())


def cmd_init(args):
    base = Path(args.root) if args.root else (store.env_root() or Path.cwd())
    return {"root": str(store.init_store(base))}


def _known_ids(root):
    return {r["id"] for f in ("nodes", "chains") for r in store.read(root, f)}


def _check_id(rec, file, prefix, existing):
    """A supplied id must have the type's format; it updates only misconceptions."""
    if "id" not in rec:
        return
    rid = rec["id"]
    if not isinstance(rid, str) or not re.fullmatch(rf"{prefix}-[0-9a-f]{{8}}", rid):
        raise CliError(f"id: must be {prefix}- plus 8 lowercase hex characters")
    seen = {r["id"] for r in existing}
    if file == "misconceptions":
        if rid not in seen:
            raise CliError(f"id: no misconception {rid}; omit id to record a new one")
    elif rid in seen:
        raise CliError(f"id: {rid} already exists; omit id (use an edit to correct a node or chain)")


def _append_command(file, prefix, validate):
    """validate(rec, root, existing_lines) -> validated record."""
    def run(args):
        root = _locate(args)
        existing = store.read(root, file)  # a corrupt store blocks the write
        rec = validate(_parse_json(args.json), root, existing)
        if prefix:
            _check_id(rec, file, prefix, existing)
        return store.append(root, file, rec, prefix, now=args.now)
    return run


def _current(root):
    return graph.current(store.read(root, "nodes"), store.read(root, "chains"),
                         store.read(root, "edits"))


def cmd_misconceptions(args):
    latest = {}
    for r in store.read(_locate(args), "misconceptions"):
        latest[r["id"]] = r  # re-assigning keeps first-appearance order, latest line wins
    return [r for r in latest.values() if not args.status or r.get("status") == args.status]


def cmd_candidates(args):
    nodes, _ = _current(_locate(args))
    return [{"id": i, "score": round(s, 3)}
            for i, s in graph.candidates(args.statement, nodes.values())]


def cmd_graph(args):
    nodes, chains = _current(_locate(args))
    return {"nodes": list(nodes.values()), "chains": list(chains.values())}


def cmd_link(args):
    root = _locate(args)
    links = store.read(root, "links")
    if not args.session.strip() or not args.slug.strip():
        raise CliError("link: --session and --slug must be non-empty")
    if args.none:
        if args.targets is not None:
            raise CliError("--targets: not allowed with --none")
        if not (args.reason or "").strip():
            raise CliError("--reason: required with --none (say why the slug has no node)")
        if any(l.get("session") == args.session and l.get("slug") == args.slug and l.get("targets")
               for l in links):
            raise CliError("link: slug is already linked to targets, so --none would have no effect")
        rec = {"session": args.session, "slug": args.slug, "targets": [], "reason": args.reason}
        return store.append(root, "links", rec, None, now=args.now)
    if args.reason is not None:
        raise CliError("--reason: only with --none")
    targets = [t for t in (args.targets or "").split(",") if t]
    if not targets:
        raise CliError("--targets: required (or close the slug with --none --reason)")
    unknown = [t for t in targets if t not in _known_ids(root)]
    if unknown:
        raise CliError(f"link: unknown target id(s): {', '.join(unknown)}")
    rec = {"session": args.session, "slug": args.slug, "targets": targets}
    return store.append(root, "links", rec, None, now=args.now)


def cmd_observations(args):
    return [o for o in store.read(_locate(args), "observations")
            if (not args.session or o["session"] == args.session)
            and (not args.target or o["target"]["id"] == args.target)]


def _replay(root):
    return schedule.replay(store.read(root, "observations"), store.read(root, "links"),
                           store.read(root, "edits"), store.read(root, "chains"))


def cmd_state(args):
    states = _replay(_locate(args))
    if args.target:
        states = {k: v for k, v in states.items() if k == args.target}
    return [dataclasses.asdict(s) for s in states.values()]


def cmd_due(args):
    if args.limit < 1:
        raise CliError("--limit: must be at least 1")
    prefer = [t for t in (args.prefer or "").split(",") if t]
    now = args.now or store.now_ts()
    return [dataclasses.asdict(s)
            for s in schedule.due(_replay(_locate(args)), now, args.limit, prefer)]


def cmd_show(args):
    return view.render(_locate(args), args.now or store.now_ts())


def build_parser():
    p = argparse.ArgumentParser(prog="learn.py")
    p.add_argument("--root", help="project directory containing .learn")
    p.add_argument("--now", help="ISO 8601 UTC timestamp replacing the wall clock")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create the .learn store")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("observe", help="append an observation")
    s.add_argument("--json", required=True)
    s.set_defaults(func=_append_command("observations", "o", lambda r, _, __: schema.validate_observation(r)))

    s = sub.add_parser("misconception", help="append or update a misconception")
    s.add_argument("--json", required=True)
    s.set_defaults(func=_append_command("misconceptions", "m", lambda r, _, __: schema.validate_misconception(r)))

    s = sub.add_parser("misconceptions", help="print the latest record per misconception")
    s.add_argument("--status", choices=["suspected", "confirmed", "addressed", "resolved"])
    s.set_defaults(func=cmd_misconceptions)

    s = sub.add_parser("node", help="append a graph node")
    s.add_argument("--json", required=True)
    s.set_defaults(func=_append_command("nodes", "n", lambda r, _, __: schema.validate_node(r)))

    s = sub.add_parser("chain", help="append a reasoning chain over existing nodes")
    s.add_argument("--json", required=True)
    s.set_defaults(func=_append_command("chains", "c", lambda r, root, _: schema.validate_chain(r, _known_ids(root))))

    s = sub.add_parser("edit", help="append a supersede, retract or contradicts edit")
    s.add_argument("--json", required=True)
    s.set_defaults(func=_append_command(
        "edits", None, lambda r, root, edits: schema.validate_edit(r, _known_ids(root), edits)))

    s = sub.add_parser("candidates", help="rank active nodes similar to a statement")
    s.add_argument("--statement", required=True)
    s.set_defaults(func=cmd_candidates)

    s = sub.add_parser("graph", help="print the current graph view")
    s.set_defaults(func=cmd_graph)

    s = sub.add_parser("link", help="link a session slug to node or chain ids")
    s.add_argument("--session", required=True)
    s.add_argument("--slug", required=True)
    s.add_argument("--targets", help="comma-separated n-/c- ids")
    s.add_argument("--none", action="store_true", help="close the slug: it has no node")
    s.add_argument("--reason", help="why the slug is closed (with --none)")
    s.set_defaults(func=cmd_link)

    s = sub.add_parser("observations", help="print observations, optionally filtered")
    s.add_argument("--session")
    s.add_argument("--target", help="a slug, n- or c- id")
    s.set_defaults(func=cmd_observations)

    s = sub.add_parser("state", help="print replayed status per target")
    s.add_argument("--target")
    s.set_defaults(func=cmd_state)

    s = sub.add_parser("due", help="print targets due for review")
    s.add_argument("--limit", type=int, default=8)
    s.add_argument("--prefer", help="comma-separated ids to list first")
    s.set_defaults(func=cmd_due)

    s = sub.add_parser("show", help="print the learner model as markdown (not JSON)")
    s.set_defaults(func=cmd_show, raw=True)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.now is not None and not store.is_timestamp(args.now):
        print("--now: must be a YYYY-MM-DDTHH:MM:SSZ timestamp", file=sys.stderr)
        return 2
    try:
        result = args.func(args)
    except (CliError, schema.ValidationError, store.StoreNotFound, store.CorruptStore) as e:
        print(str(e), file=sys.stderr)
        return 2
    except (KeyError, ValueError, TypeError) as e:  # last resort: a record shape nothing else caught
        print(f"store: unexpected record shape ({type(e).__name__}: {e})", file=sys.stderr)
        return 2
    if getattr(args, "raw", False):
        print(result, end="")
    else:
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
