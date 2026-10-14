"""Token estimation using tiktoken with robust heuristic fallback."""

import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

# Approximate standard input prices per 1,000,000 tokens (USD). ESTIMATES ONLY:
# taken from third-party price trackers as of 2026-10-13 (benchlm.ai, mem0.ai), not from the
# vendors; promotional/introductory rates deliberately avoided. Re-check when models change.
PRICES_AS_OF = "2026-10-13"
DEFAULT_MODEL = "claude-sonnet-5.5"
MODEL_PRICING: dict[str, float] = {
    "claude-opus-5.5": 4.00,
    "claude-sonnet-5.5": 2.00,
    "gpt-5.5": 5.00,
    "gpt-5.4-mini": 0.75,
    "gemini-3.1-pro": 2.00,
    "gemini-2.5-flash": 0.30,
}


@lru_cache(maxsize=4)
def _get_tiktoken_encoding(encoding_name: str = "cl100k_base"):
    """Cache tiktoken encoding to avoid repeated initialization."""
    try:
        import tiktoken

        return tiktoken.get_encoding(encoding_name)
    except (ImportError, ValueError, KeyError) as exc:
        logger.debug("Failed to load tiktoken encoding '%s': %s", encoding_name, exc)
        return None


def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """Count tokens in text using tiktoken, falling back to a 4-char heuristic.

    Args:
        text: The string content to measure.
        encoding_name: tiktoken encoding identifier (e.g. 'cl100k_base' or 'o200k_base').

    Returns:
        Estimated or exact number of tokens.
    """
    if not text:
        return 0

    encoding = _get_tiktoken_encoding(encoding_name)
    if encoding is not None:
        try:
            return len(encoding.encode(text, disallowed_special=()))
        except (ValueError, TypeError) as exc:
            logger.debug("Encoding error during token calculation: %s", exc)

    # Heuristic fallback: roughly 1 token per 3.7 - 4 characters for code/text
    return max(1, int(len(text) / 3.8))


def estimate_token_cost(token_count: int, model_name: str = DEFAULT_MODEL) -> float:
    """Calculate the estimated input cost in USD for the given token count."""
    price_per_million = MODEL_PRICING.get(model_name.lower(), MODEL_PRICING[DEFAULT_MODEL])
    return (token_count / 1_000_000.0) * price_per_million
