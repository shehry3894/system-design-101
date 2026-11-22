"""Every example must run to the end, fast, with its asserts passing."""
import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES = sorted(p for p in Path(__file__).parent.rglob("*.py") if p.name != "test_examples.py")


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: str(p.relative_to(Path(__file__).parent)))
def test_example_runs(path):
    result = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
