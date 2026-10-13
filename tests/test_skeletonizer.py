"""Tests for Python AST Code Skeletonizer."""

from pathlib import Path

from src.modules.skeletonizer import skeletonize_code, skeletonize_file


def test_skeletonize_functions():
    code = """
def calculate_metrics(values: list[float], factor: float = 1.0) -> dict[str, float]:
    '''Calculate sum, mean and standard deviation.'''
    total = sum(values) * factor
    mean = total / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std_dev = variance ** 0.5
    return {'total': total, 'mean': mean, 'std_dev': std_dev}
"""
    skeleton = skeletonize_code(code)
    assert "def calculate_metrics(" in skeleton
    assert "-> dict[str, float]:" in skeleton
    assert "Calculate sum, mean and standard deviation." in skeleton
    assert "total = sum(values)" not in skeleton
    assert "..." in skeleton


def test_skeletonize_classes():
    code = """
class DataService:
    '''Service for handling queries.'''
    db_url: str

    def __init__(self, db_url: str):
        '''Initialize connection.'''
        self.db_url = db_url
        self._connect()

    def query(self, sql: str) -> list[dict]:
        # Expensive query logic
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
"""
    skeleton = skeletonize_code(code)
    assert "class DataService:" in skeleton
    assert "def __init__(self, db_url: str):" in skeleton
    assert "def query(self, sql: str) -> list[dict]:" in skeleton
    assert "self._connect()" not in skeleton
    assert "cursor = self.db.cursor()" not in skeleton


def test_skeletonize_file(tmp_path: Path):
    file_path = tmp_path / "service.py"
    file_path.write_text(
        """
import math

def complex_algorithm(x: int) -> int:
    '''Performs intense computation.'''
    res = 0
    for i in range(100):
        res += math.sin(x + i)
    return int(res)
""",
        encoding="utf-8",
    )
    res = skeletonize_file(file_path)
    assert res["file_name"] == "service.py"
    assert res["percentage_saved"] > 0
    assert "def complex_algorithm(x: int) -> int:" in res["skeleton"]
    assert "for i in range(100):" not in res["skeleton"]
