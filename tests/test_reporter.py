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
