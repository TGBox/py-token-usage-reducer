"""Tests for Log & Stacktrace Compressor."""

from pathlib import Path

from src.modules.log_compressor import compress_log_file, compress_logs, strip_ansi_codes


def test_strip_ansi_codes():
    raw = "\x1b[31m[ERROR]\x1b[0m Failed to connect to server"
    cleaned = strip_ansi_codes(raw)
    assert cleaned == "[ERROR] Failed to connect to server"


def test_compress_repetitive_lines():
    raw = "\n".join(["2026-10-13 12:00:00 INFO Polling endpoint..."] * 25)
    compressed = compress_logs(raw)
    assert "Zeile 23x wiederholt ausgelassen" in compressed


def test_compress_python_traceback():
    raw = """
Traceback (most recent call last):
  File "C:\\Python311\\lib\\site-packages\\urllib3\\connectionpool.py", line 400, in _make_request
    six.reraise(type(e), e)
  File "C:\\Python311\\lib\\site-packages\\requests\\adapters.py", line 450, in send
    raise ConnectionError(err, request=request)
  File "C:\\Users\\Dev\\myproject\\src\\client.py", line 42, in fetch_user
    return api.get("/users/1")
requests.exceptions.ConnectionError: Failed to establish a new connection
"""
    compressed = compress_logs(raw)
    assert "Traceback (most recent call last):" in compressed
    assert "src\\client.py" in compressed
    assert "ConnectionError: Failed to establish a new connection" in compressed
    assert "interne Framework-/Bibliotheks-Frames ausgelassen" in compressed


def test_compress_log_file(tmp_path: Path):
    f = tmp_path / "server.log"
    f.write_text("\x1b[32mOK\x1b[0m\n" * 100, encoding="utf-8")
    res = compress_log_file(f)
    assert res["file_name"] == "server.log"
    assert res["percentage_saved"] > 0.0


def test_skipped_frames_drop_their_code_lines():
    raw = """Traceback (most recent call last):
  File "/app/main.py", line 3, in <module>
    run()
  File "/venv/lib/python3.11/site-packages/flask/app.py", line 10, in run
    return self.wsgi_app(environ)
  File "/venv/lib/python3.11/site-packages/flask/app.py", line 20, in wsgi_app
    response = self.handle_exception(e)
ValueError: boom"""
    out = compress_logs(raw)
    assert "run()" in out
    assert "wsgi_app(environ)" not in out
    assert "handle_exception" not in out
    assert "2 interne" in out
    assert "ValueError: boom" in out
