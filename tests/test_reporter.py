"""Tests for Project Architecture Reporter."""

from pathlib import Path

from src.modules.reporter import generate_project_report


def test_generate_project_report(tmp_path: Path):
    # Setup mock project
    src = tmp_path / "src"
    src.mkdir()
    (src / "app.py").write_text(
        """
import os
import sys
from collections import Counter

def run_app():
    '''Start application main loop.'''
    print('Starting app...')
    return True
""",
        encoding="utf-8",
    )
    (src / "utils.py").write_text(
        """
import json

def helper():
    '''Helper utility.'''
    pass
""",
        encoding="utf-8",
    )

    # Ignored directory
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "index").write_text("binary blob data", encoding="utf-8")

    report = generate_project_report(tmp_path, include_skeletons=True)

    assert report["total_files"] == 2
    assert report["total_tokens"] > 0
    assert ".git/index" not in report["markdown"]
    assert "src/app.py" in report["markdown"]
    assert "collections" in report["markdown"]
    assert "API-Skelette zentraler Python-Komponenten" in report["markdown"]
    assert "def run_app():" in report["markdown"]
    assert "Starting app..." not in report["markdown"]  # Skeletonized body was removed!


def test_scan_prunes_ignored_dirs(tmp_path: Path, monkeypatch):
    from src.core.gitignore import GitIgnoreMatcher
    from src.modules.reporter import _scan_repository_files

    (tmp_path / "app.py").write_text("x = 1\n", encoding="utf-8")
    venv = tmp_path / ".venv" / "lib"
    venv.mkdir(parents=True)
    (venv / "huge.py").write_text("y = 2\n", encoding="utf-8")

    checked: list[Path] = []
    original = GitIgnoreMatcher.is_ignored
    monkeypatch.setattr(
        GitIgnoreMatcher, "is_ignored", lambda self, p: checked.append(p) or original(self, p)
    )

    stats = _scan_repository_files(tmp_path)
    assert [s.rel_path for s in stats] == ["app.py"]
    # The walk must never descend into .venv
    assert not any(".venv" in p.parts[:-1] for p in checked)
