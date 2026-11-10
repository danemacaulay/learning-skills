import json
import re

import pytest

from learnlib.store import CorruptStore, FILES, StoreNotFound, append, find_root, init_store, read


def test_init_is_idempotent_and_creates_all_files(tmp_path):
    r = init_store(tmp_path)
    init_store(tmp_path)
    assert all((r / p).exists() for p in FILES.values()) and (r / "sessions").is_dir()


def test_init_does_not_truncate_existing(tmp_path, obs):
    r = init_store(tmp_path)
    append(r, "observations", obs(), prefix="o")
    init_store(tmp_path)
    assert len(read(r, "observations")) == 1


def test_append_assigns_id_and_ts_and_never_rewrites(root, obs):
    a = append(root, "observations", obs(response="1"), prefix="o")
    append(root, "observations", obs(response="2"), prefix="o")
    assert re.fullmatch(r"o-[0-9a-f]{8}", a["id"]) and a["ts"].endswith("Z")
    assert [r["response"] for r in read(root, "observations")] == ["1", "2"]


def test_append_keeps_supplied_id_and_ts(root):
    rec = append(root, "observations", {"id": "o-00000001", "ts": "2026-11-09T22:19:00Z"}, prefix="o")
    assert rec["id"] == "o-00000001" and rec["ts"] == "2026-11-09T22:19:00Z"


def test_verbatim_text_round_trips(root, obs):
    text = 'line one\n"quoted" — 存在 🙂'
    append(root, "observations", obs(response=text), prefix="o")
    assert read(root, "observations")[0]["response"] == text


def test_corrupt_line_names_file_and_line(root, obs):
    append(root, "observations", obs(), prefix="o")
    with open(root / FILES["observations"], "a") as fh:
        fh.write("{broken\n")
    with pytest.raises(CorruptStore, match=r"learner/observations\.jsonl:2"):
        read(root, "observations")


def test_find_root_walks_up(root):
    deep = root.parent / "a" / "b"
    deep.mkdir(parents=True)
    assert find_root(deep) == root


def test_find_root_missing_raises(tmp_path):
    with pytest.raises(StoreNotFound):
        find_root(tmp_path)


def test_find_root_env_override(root, tmp_path_factory, monkeypatch):
    elsewhere = tmp_path_factory.mktemp("elsewhere")
    monkeypatch.setenv("LEARN_ROOT", str(root.parent))
    assert find_root(elsewhere) == root


def test_append_starts_a_new_line_when_the_file_lacks_a_trailing_newline(root, obs):
    f = root / FILES["observations"]
    first = append(root, "observations", obs(), prefix="o")
    f.write_text(f.read_text().rstrip("\n"))  # a hand edit dropped the final newline
    append(root, "observations", obs(response="second"), prefix="o")
    assert [r["id"] for r in read(root, "observations")][0] == first["id"]
    assert len(read(root, "observations")) == 2


def _line(**kw):
    return json.dumps(kw) + "\n"


@pytest.mark.parametrize("file,line,reason", [
    ("observations", _line(id="o-00000001", session="s", kind="check", target={"type": "slug", "id": "x"},
                           grade="took"), "ts"),
    ("observations", _line(id="o-00000001", ts="tomorrow", session="s", kind="check",
                           target={"type": "slug", "id": "x"}, grade="took"), "ts"),
    ("observations", _line(id="o-00000001", ts="2026-11-09T10:00:00Z", session="s", kind="check",
                           target="x", grade="took"), "target"),
    ("misconceptions", _line(ts="2026-11-09T10:00:00Z", statement="s"), "id"),
    ("links", _line(ts="2026-11-09T10:00:00Z", session="s", slug="x"), "targets"),
    ("nodes", _line(id="n-00000001", ts="2026-13-40T10:00:00Z"), "ts"),
    ("chains", _line(id="c-00000001", ts="2026-11-09T10:00:00Z", premises=["n-1"]), "conclusion"),
    ("edits", _line(ts="2026-11-09T10:00:00Z", op="supersede", target="n-1"), "by"),
])
def test_wrong_shape_line_names_file_line_and_field(root, file, line, reason):
    (root / FILES[file]).write_text(line)
    with pytest.raises(CorruptStore, match=rf"{re.escape(FILES[file])}:1: {reason}"):
        read(root, file)


def test_missing_file_is_corrupt_and_says_to_run_init(root):
    (root / FILES["links"]).unlink()
    with pytest.raises(CorruptStore, match=r"learner/links\.jsonl.*learn\.py init"):
        read(root, "links")
