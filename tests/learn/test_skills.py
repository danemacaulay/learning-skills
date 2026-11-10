import re
from pathlib import Path

import pytest

import learn

SKILLS = Path(__file__).parents[2] / "skills"
REQUIRED: dict[str, list[str]] = {   # filled by Tasks 6-10
    "learn-ground": ["learn.py init", "learn.py due", "learn.py observe", "learn.py misconception",
                     "Success criteria", "3–5", "12–20", "stop and plan from here",
                     "theory.md#T1", "theory.md#T5", "theory.md#T7", "theory.md#T12",
                     "stop following this skill", "from its first step before sending the learner anything else", "probe.md", "never quote it in a message",
                     "different question that the suspected idea would also get wrong",
                     "only the returned items whose id is in your list", '"lowEffort":true'],
    "learn-plan": ["learn.py graph", "learn.py candidates", "Unverified", "contrasting case", "refut",
                   "expected answer", "wrong models", "theory.md#T2", "theory.md#T4", "theory.md#T7",
                   "theory.md#T10", "theory.md#T11",
                   "stop following this skill", "from its first step before sending the learner anything else", "single sink", "use that probe slug as the landmark slug",
                   "held (retrieve, do not re-teach)"],
    "learn-teach": ["learn.py observe", "Expected:", "Wrong models:", "before the learner replies",
                    "closed transcript", "taught", "retained", "theory.md#T2", "theory.md#T3",
                    "theory.md#T4", "theory.md#T5", "theory.md#T6", "theory.md#T8",
                    "stop following this skill", "from its first step before sending the learner anything else", "`Explanation:` on every step that is started",
                    "`o-` id that `observe` printed", "Hand off to learn-record in the same sitting",
                    "nothing is reviewable until `learn-record` runs", "one cold check and no teaching",
                    "the learner's attempt is the step's check", "learn.py observations"],
    "learn-record": ["learn.py candidates", "learn.py node", "learn.py chain", "learn.py edit",
                     "learn.py link", "tutor-asserted", "source-verified", "one claim",
                     "Link decisions", "theory.md#T10",
                     "row by row", "Held and passed cold", "--none --reason", "learn.py observations",
                     "never rewrite an earlier section", "Do not start it now and do not offer it in this sitting",
                     "look up each returned id in `learn.py graph`"],
    "learn-review": ["learn.py due", "learn.py observe", "reconstruct", "counterfactual", "discriminate",
                     "hinted", "at most 8", "theory.md#T4", "theory.md#T5", "theory.md#T8", "theory.md#T9",
                     "stop following this skill", "from its first step before sending the learner anything else", "review.md", "never quote it in a message", "Only after the review",
                     "Nothing recorded in this sitting is reviewed in this sitting", "offer `learn-ground`",
                     "correct answer given at low confidence", "`resolved`"],
}


def test_theory_has_all_rules_each_with_a_basis():
    text = (SKILLS / "_learn/theory.md").read_text()
    for n in range(1, 13):
        section = re.search(rf"### T{n}:.*?(?=### T\d+:|\Z)", text, re.S)
        assert section and "Basis:" in section.group(0), f"T{n}"


def test_store_doc_shows_every_subcommand():
    text = (SKILLS / "_learn/store.md").read_text()
    assert all(re.search(rf"learn\.py (--\S+ \S+ )*{c}\b", text) for c in learn.SUBCOMMANDS)


@pytest.mark.parametrize("skill", sorted(REQUIRED))
def test_skill_file(skill):
    text = (SKILLS / skill / "SKILL.md").read_text()
    front, body = text.split("---", 2)[1:]
    assert re.search(rf"^name: {skill}$", front, re.M)
    assert re.search(r"^description: Use when", front, re.M)
    assert len(body.splitlines()) <= 200
    assert all(p in body for p in REQUIRED[skill]), [p for p in REQUIRED[skill] if p not in body]
    for cmd in re.findall(r"learn\.py (?:--\S+ \S+ )*([a-z-]+)", body):
        assert cmd in learn.SUBCOMMANDS, cmd
    for ref in re.findall(r"\((\.\./_learn/[^)#]+)", body):
        assert (SKILLS / skill / ref).exists(), ref
    for rule in re.findall(r"theory\.md#T(\d+)", body):
        assert 1 <= int(rule) <= 12
