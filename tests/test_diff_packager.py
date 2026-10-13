"""Tests for Git Diff Context Packager."""

from pathlib import Path

from src.modules.diff_packager import package_git_diff


def test_package_git_diff_with_raw_diff(tmp_path: Path):
    # Create the affected file on disk so skeletonizer can extract its interface
    src_file = tmp_path / "calc.py"
    src_file.write_text(
        """
def add(a: int, b: int) -> int:
    '''Add two integers.'''
    result = a + b
    return result
""",
        encoding="utf-8",
    )

    diff = """
diff --git a/calc.py b/calc.py
--- a/calc.py
+++ b/calc.py
@@ -1,3 +1,3 @@
-def add(a: int, b: int) -> int:
+def add(a: int, b: int, c: int = 0) -> int:
"""
    res = package_git_diff(tmp_path, raw_diff=diff, include_skeletons=True)
    assert "calc.py" in res["diff_files"]
    assert "`calc.py` (Schnittstelle)" in res["packaged_markdown"]
    assert "Add two integers." in res["packaged_markdown"]
    assert "Vollständiger Git-Diff" in res["packaged_markdown"]


def test_package_git_diff_empty(tmp_path: Path):
    res = package_git_diff(tmp_path, raw_diff="")
    assert res["diff_files"] == []
    assert (
        "Keine ungespeicherten oder geänderten Git-Änderungen gefunden" in res["packaged_markdown"]
    )
