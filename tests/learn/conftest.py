import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "skills" / "_learn" / "scripts"))

from learnlib.store import init_store  # noqa: E402


@pytest.fixture
def root(tmp_path):
    return init_store(tmp_path)


@pytest.fixture
def obs():
    def make(**overrides):
        base = {"session": "20261109-demo", "kind": "check", "form": "apply",
                "target": {"type": "slug", "id": "ready-to-hand"},
                "prompt": "What would this predict when the hammer breaks?",
                "expected": "The tool becomes conspicuous", "response": "you notice it",
                "confidence": "med", "grade": "took", "produced": True}
        base.update(overrides)
        return base
    return make
