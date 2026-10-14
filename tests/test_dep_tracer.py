"""Tests for Dependency Context Tracer."""

from pathlib import Path

from src.modules.dep_tracer import trace_dependencies


def test_trace_dependencies(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir()

    # module c: leaf
    (src / "c.py").write_text("def c_func(): return 100\n", encoding="utf-8")

    # module b: imports c
    (src / "b.py").write_text(
        "from src.c import c_func\ndef b_func(): return c_func() * 2\n", encoding="utf-8"
    )

    # module a (entrypoint): imports b
    (src / "a.py").write_text(
        "from src.b import b_func\ndef main(): return b_func()\n", encoding="utf-8"
    )

    # unreferenced module
    (src / "unused.py").write_text("def unused_thing(): pass\n", encoding="utf-8")

    result = trace_dependencies(src / "a.py", project_root=tmp_path)
    deps = [Path(p).name for p in result["dependency_files"]]

    assert "a.py" in deps
    assert "b.py" in deps
    assert "c.py" in deps
    assert "unused.py" not in deps
    assert "b_func" in result["bundled_markdown"]
    assert "unused_thing" not in result["bundled_markdown"]


def test_default_root_is_project_root(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    pkg = tmp_path / "src"
    pkg.mkdir()
    (pkg / "util.py").write_text("X = 1\n", encoding="utf-8")
    (pkg / "main.py").write_text("from src.util import X\n", encoding="utf-8")

    res = trace_dependencies(pkg / "main.py")
    assert len(res["dependency_files"]) == 2
