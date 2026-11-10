import pytest

from learnlib.schema import (ValidationError, validate_chain, validate_edit, validate_misconception,
                             validate_node, validate_observation)


def test_valid_observation_gets_defaults(obs):
    out = validate_observation(obs())
    assert out["hinted"] is False and out["lowEffort"] is False


@pytest.mark.parametrize("field,value", [
    ("kind", "quiz"), ("form", "cloze"), ("confidence", "sure"),
    ("grade", "partial"), ("prompt", ""), ("target", {"type": "card", "id": "x"}),
])
def test_bad_observation_field_rejected(obs, field, value):
    with pytest.raises(ValidationError, match=field):
        validate_observation(obs(**{field: value}))


def test_check_without_precommitted_expected_rejected(obs):
    with pytest.raises(ValidationError, match="expected"):
        validate_observation(obs(expected=None))


def test_probe_may_omit_expected(obs):
    validate_observation(obs(kind="probe", expected=None))


def test_unknown_field_rejected(obs):
    with pytest.raises(ValidationError, match="surprise"):
        validate_observation(obs(surprise=1))


def test_missing_field_rejected(obs):
    rec = obs()
    del rec["response"]
    with pytest.raises(ValidationError, match="response"):
        validate_observation(rec)


def test_bool_fields_must_be_bool(obs):
    with pytest.raises(ValidationError, match="produced"):
        validate_observation(obs(produced="yes"))


def test_misconception_link_must_be_m_id(obs):
    with pytest.raises(ValidationError, match="misconception"):
        validate_observation(obs(misconception="o-00000001"))
    validate_observation(obs(misconception="m-0123abcd"))


def test_confirmed_misconception_needs_two_evidence():
    rec = {"statement": "s", "counterpart": "c", "contradicts": [], "evidence": ["o-00000001"],
           "stability": "stable", "kind": "category-error", "status": "confirmed", "session": "s1"}
    with pytest.raises(ValidationError, match="evidence"):
        validate_misconception(rec)
    validate_misconception({**rec, "status": "suspected"})
    validate_misconception({**rec, "evidence": ["o-00000001", "o-00000002"]})


def test_misconception_bad_enum_and_empty_evidence():
    rec = {"statement": "s", "counterpart": "c", "contradicts": [], "evidence": [],
           "stability": "stable", "kind": "category-error", "status": "suspected", "session": "s1"}
    with pytest.raises(ValidationError, match="evidence"):
        validate_misconception(rec)
    with pytest.raises(ValidationError, match="stability"):
        validate_misconception({**rec, "evidence": ["o-00000001"], "stability": "odd"})


def test_supplied_ts_must_be_a_z_timestamp(obs):
    for bad in ("tomorrow", "2026-11-09", "2026-11-09T10:00:00", "2026-11-31T10:00:00Z"):
        with pytest.raises(ValidationError, match="ts"):
            validate_observation(obs(ts=bad))
    assert validate_observation(obs(ts="2026-11-09T10:00:00Z"))["ts"] == "2026-11-09T10:00:00Z"


def test_supplied_ts_checked_on_every_record_type():
    mis = {"statement": "s", "counterpart": "c", "contradicts": [], "evidence": ["o-00000001"],
           "stability": "one-off", "kind": "category-error", "status": "suspected", "session": "s1",
           "ts": "soon"}
    node = {"name": "a", "statement": "A holds.", "claimType": "definition", "status": "tutor-asserted",
            "source": None, "scope": None, "session": "s", "ts": "soon"}
    with pytest.raises(ValidationError, match="ts"):
        validate_misconception(mis)
    with pytest.raises(ValidationError, match="ts"):
        validate_node(node)
    with pytest.raises(ValidationError, match="ts"):
        validate_chain({"premises": ["n-1"], "conclusion": "n-2", "session": "s", "ts": "soon"},
                       known={"n-1", "n-2"})
    with pytest.raises(ValidationError, match="ts"):
        validate_edit({"op": "retract", "target": "n-1", "reason": "r", "session": "s", "ts": "soon"},
                      known={"n-1"})


def test_chain_premises_and_conclusion_must_be_node_ids():
    known = {"n-1", "n-2", "c-1"}
    with pytest.raises(ValidationError, match="premises"):
        validate_chain({"premises": ["c-1"], "conclusion": "n-2", "session": "s"}, known)
    with pytest.raises(ValidationError, match="conclusion"):
        validate_chain({"premises": ["n-1"], "conclusion": "c-1", "session": "s"}, known)
    validate_chain({"premises": ["n-1"], "conclusion": "n-2", "session": "s"}, known)


def _sup(target, by):
    return {"op": "supersede", "target": target, "by": by, "reason": "r", "session": "s"}


def test_validate_edit_rejects_unknown_ids_self_supersede_and_bad_op():
    with pytest.raises(ValidationError, match="target"):
        validate_edit(_sup("n-9", "n-1"), known={"n-1"})
    with pytest.raises(ValidationError, match="by"):
        validate_edit(_sup("n-1", "n-1"), known={"n-1"})
    with pytest.raises(ValidationError, match="op"):
        validate_edit({"op": "delete", "target": "n-1"}, known={"n-1"})
    with pytest.raises(ValidationError, match="b"):
        validate_edit({"op": "contradicts", "a": "n-1", "b": "n-1", "reason": "r", "session": "s"},
                      known={"n-1"})


def test_supersede_must_keep_the_type():
    known = {"n-1", "n-2", "c-1", "c-2"}
    with pytest.raises(ValidationError, match="by"):
        validate_edit(_sup("n-1", "c-1"), known)
    with pytest.raises(ValidationError, match="by"):
        validate_edit(_sup("c-1", "n-1"), known)
    validate_edit(_sup("c-1", "c-2"), known)
    validate_edit(_sup("n-1", "n-2"), known)


def test_supersede_that_closes_a_cycle_is_rejected():
    known = {"n-1", "n-2", "n-3"}
    with pytest.raises(ValidationError, match="cycle"):
        validate_edit(_sup("n-2", "n-1"), known, edits=[_sup("n-1", "n-2")])
    with pytest.raises(ValidationError, match="cycle"):
        validate_edit(_sup("n-3", "n-1"), known, edits=[_sup("n-1", "n-2"), _sup("n-2", "n-3")])
    validate_edit(_sup("n-1", "n-3"), known, edits=[_sup("n-1", "n-2")])  # re-pointing is fine
