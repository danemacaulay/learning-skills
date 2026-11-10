import pytest

from learnlib.graph import candidates, current, resolve
from learnlib.schema import ValidationError, validate_chain, validate_node


def N(**kw):
    base = {"name": "equipment-is-ready-to-hand", "statement": "Equipment in use is ready-to-hand.",
            "claimType": "attribution", "status": "source-verified",
            "source": "Being and Time §15", "scope": None, "session": "s1"}
    base.update(kw)
    return base


def test_valid_node_passes():
    assert validate_node(N())["name"] == "equipment-is-ready-to-hand"


def test_compound_statement_rejected():
    with pytest.raises(ValidationError, match="chain"):
        validate_node(N(statement="Tools withdraw because we attend to the work."))


def test_attribution_requires_source():
    with pytest.raises(ValidationError, match="source"):
        validate_node(N(source=None, status="tutor-asserted"))


def test_source_verified_requires_source():
    with pytest.raises(ValidationError, match="source"):
        validate_node(N(source=None, claimType="definition"))


def test_interpretation_requires_scope():
    with pytest.raises(ValidationError, match="scope"):
        validate_node(N(claimType="interpretation", scope=None))


def test_name_must_be_kebab_case():
    with pytest.raises(ValidationError, match="name"):
        validate_node(N(name="Not Kebab"))


def test_chain_ids_must_exist_and_conclusion_not_a_premise():
    with pytest.raises(ValidationError, match="premises"):
        validate_chain({"premises": ["n-1"], "conclusion": "n-2", "session": "s"}, known={"n-2"})
    with pytest.raises(ValidationError, match="conclusion"):
        validate_chain({"premises": ["n-1"], "conclusion": "n-1", "session": "s"}, known={"n-1"})


def test_chain_rejects_duplicate_premises():
    with pytest.raises(ValidationError, match="premises"):
        validate_chain({"premises": ["n-1", "n-1"], "conclusion": "n-2", "session": "s"},
                       known={"n-1", "n-2"})


def test_supersede_replaces_and_chains_follow():
    nodes = [{"id": "n-1"}, {"id": "n-2"}, {"id": "n-3"}]
    chains = [{"id": "c-1", "premises": ["n-1"], "conclusion": "n-2"}]
    edits = [{"op": "supersede", "target": "n-1", "by": "n-3"}]
    active_nodes, active_chains = current(nodes, chains, edits)
    assert set(active_nodes) == {"n-2", "n-3"} and active_chains["c-1"]["premises"] == ["n-3"]
    assert resolve("n-1", edits) == "n-3"


def test_retract_deactivates_dependent_chains():
    nodes = [{"id": "n-1"}, {"id": "n-2"}]
    chains = [{"id": "c-1", "premises": ["n-1"], "conclusion": "n-2"}]
    edits = [{"op": "retract", "target": "n-1", "reason": "tutor error"}]
    active_nodes, active_chains = current(nodes, chains, edits)
    assert set(active_nodes) == {"n-2"} and active_chains == {} and resolve("n-1", edits) is None


def test_retracted_chain_is_inactive_and_contradicts_changes_nothing():
    nodes = [{"id": "n-1"}, {"id": "n-2"}]
    chains = [{"id": "c-1", "premises": ["n-1"], "conclusion": "n-2"}]
    edits = [{"op": "contradicts", "a": "n-1", "b": "n-2", "reason": "r"}]
    active_nodes, active_chains = current(nodes, chains, edits)
    assert set(active_nodes) == {"n-1", "n-2"} and set(active_chains) == {"c-1"}
    _, active_chains = current(nodes, chains, edits + [{"op": "retract", "target": "c-1", "reason": "r"}])
    assert active_chains == {}


def test_candidates_rank_similar_statement_first_and_skip_unrelated():
    nodes = [N(id="n-1"), N(id="n-2", name="primary-key", statement="A primary key identifies a row.")]
    got = candidates("Equipment being used is ready-to-hand", nodes)
    assert [i for i, _ in got] == ["n-1"]
