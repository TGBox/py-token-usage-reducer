"""Tests for Data & Schema Reducer (JSON, CSV, SQL)."""

import json
from pathlib import Path

from src.modules.data_reducer import reduce_csv, reduce_data_file, reduce_json, reduce_sql


def test_reduce_json():
    # Large list of 100 items
    data = [{"id": i, "name": f"User_{i}", "active": True, "score": 95.5} for i in range(100)]
    raw = json.dumps(data)
    reduced = reduce_json(raw, max_samples=2)

    assert "Erkanntes Schema:" in reduced
    assert "| `id` | `integer` |" in reduced
    assert "| `name` | `string` |" in reduced
    assert "User_0" in reduced
    assert "User_1" in reduced
    assert "User_99" not in reduced
    assert "weitere Elemente ausgelassen" in reduced


def test_reduce_csv():
    lines = ["id,first_name,salary,employed"]
    for i in range(50):
        lines.append(f"{i},Person_{i},50000.0,true")
    raw = "\n".join(lines)
    reduced = reduce_csv(raw, max_rows=2)

    assert "**first_name** (str)" in reduced
    assert "**salary** (float)" in reduced
    assert "Person_0" in reduced
    assert "Person_1" in reduced
    assert "Person_49" not in reduced
    assert "48 weitere Datenzeilen für Token-Ersparnis ausgelassen" in reduced


def test_reduce_sql():
    sql = """
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

INSERT INTO users VALUES (1, 'Alice');
INSERT INTO users VALUES (2, 'Bob');
INSERT INTO users VALUES (3, 'Charlie');
INSERT INTO users VALUES (4, 'Dave');
"""
    reduced = reduce_sql(sql, max_inserts=2)
    assert "CREATE TABLE users" in reduced
    assert "INSERT INTO users VALUES (1, 'Alice');" in reduced
    assert "INSERT INTO users VALUES (2, 'Bob');" in reduced
    assert "INSERT INTO users VALUES (3, 'Charlie');" not in reduced
    assert "Weitere INSERT-Statements ausgelassen" in reduced


def test_reduce_data_file(tmp_path: Path):
    f = tmp_path / "big_data.json"
    f.write_text(json.dumps([{"x": 1}] * 200), encoding="utf-8")

    res = reduce_data_file(f, max_samples=2)
    assert res["file_name"] == "big_data.json"
    assert res["percentage_saved"] > 50.0


def test_reduce_tsv(tmp_path: Path):
    f = tmp_path / "data.tsv"
    f.write_text("a\tb\tc\n1\t2\t3\n", encoding="utf-8")
    md = reduce_data_file(f)["reduced_markdown"]
    assert "**b** (int)" in md
    assert "| 1 | 2 | 3 |" in md
