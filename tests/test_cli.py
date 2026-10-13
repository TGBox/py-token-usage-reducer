"""Tests for CLI argument parsing and execution."""

import json
from pathlib import Path

from src.cli.parser import run_cli


def test_cli_guide():
    # Calling guide should return code 0
    assert run_cli(["guide", "convert"]) == 0
    assert run_cli(["guide"]) == 0


def test_cli_convert(tmp_path: Path):
    html_file = tmp_path / "test.html"
    html_file.write_text("<h1>Doc</h1><p>Content</p>", encoding="utf-8")
    out_file = tmp_path / "out.md"

    code = run_cli(["convert", str(html_file), "-o", str(out_file)])
    assert code == 0
    assert out_file.is_file()
    assert "# Doc" in out_file.read_text(encoding="utf-8")


def test_cli_skeleton(tmp_path: Path):
    py_file = tmp_path / "code.py"
    py_file.write_text("def my_func():\n    return 42\n", encoding="utf-8")
    out_file = tmp_path / "out_skel.py"

    code = run_cli(["skeleton", str(py_file), "-o", str(out_file)])
    assert code == 0
    assert "..." in out_file.read_text(encoding="utf-8")


def test_cli_schema(tmp_path: Path):
    json_file = tmp_path / "test.json"
    json_file.write_text(
        json.dumps([{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]), encoding="utf-8"
    )
    out_file = tmp_path / "out_schema.md"

    code = run_cli(["schema", str(json_file), "-o", str(out_file)])
    assert code == 0
    assert "Erkanntes Schema" in out_file.read_text(encoding="utf-8")


def test_cli_gui_signal():
    # Running without arguments signals to launch the GUI (code 100)
    assert run_cli([]) == 100
    assert run_cli(["--gui"]) == 100
