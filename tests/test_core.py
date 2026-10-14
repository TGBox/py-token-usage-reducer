"""Tests for core utilities: tokenizer, gitignore, text_utils."""

from pathlib import Path

from src.core.gitignore import GitIgnoreMatcher
from src.core.text_utils import clean_markdown, format_token_savings, truncate_text
from src.core.tokenizer import count_tokens, estimate_token_cost


def test_tokenizer_basic():
    assert count_tokens("") == 0
    tokens = count_tokens("Hello world, this is a test string for token counting.")
    assert tokens > 0
    assert count_tokens("def foo():\n    return 42\n") > 0


def test_estimate_token_cost():
    cost = estimate_token_cost(1_000_000, "claude-sonnet-5.5")
    assert cost == 2.00
    cost_cheap = estimate_token_cost(1_000_000, "gemini-2.5-flash")
    assert cost_cheap == 0.30
    # Unknown model falls back to the default model's price
    assert estimate_token_cost(1_000_000, "unknown") == cost


def test_clean_markdown():
    raw = (
        "# Title\n\n\n\n"
        "Some text with trailing spaces   \n"
        "<!-- This is a comment -->\n"
        "![Icon](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=)\n\n\n"
        "End of document."
    )
    cleaned = clean_markdown(raw)
    assert "<!-- This is a comment -->" not in cleaned
    assert "Base64-Daten entfernt" in cleaned
    assert "\n\n\n\n" not in cleaned
    assert "Some text with trailing spaces\n" in cleaned


def test_truncate_text():
    text = "A" * 100
    truncated = truncate_text(text, max_chars=10)
    assert len(truncated) < 100
    assert "[Gekürzt]" in truncated


def test_format_token_savings():
    stats = format_token_savings(1000, 200)
    assert stats["original_tokens"] == 1000
    assert stats["reduced_tokens"] == 200
    assert stats["tokens_saved"] == 800
    assert stats["percentage_saved"] == 80.0


def test_gitignore_matching(tmp_path: Path):
    # Setup test directory structure
    (tmp_path / ".git").mkdir()
    (tmp_path / ".venv").mkdir()
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hi')", encoding="utf-8")
    (tmp_path / "build").mkdir()
    (tmp_path / "secret.key").write_text("secret", encoding="utf-8")

    gitignore_file = tmp_path / ".gitignore"
    gitignore_file.write_text("*.key\n/build/\n!build/keep.txt\n", encoding="utf-8")

    matcher = GitIgnoreMatcher(tmp_path)

    assert matcher.is_ignored(tmp_path / ".git")
    assert matcher.is_ignored(tmp_path / ".venv")
    assert matcher.is_ignored(tmp_path / "node_modules")
    assert matcher.is_ignored(tmp_path / "secret.key")
    assert matcher.is_ignored(tmp_path / "build")
    assert not matcher.is_ignored(tmp_path / "src" / "main.py")
