"""Tiny text utilities used as a demo app for the Jenkins pipeline."""
import re


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[-\s]+", "-", text)


def word_count(text: str) -> int:
    """Count words in a string."""
    return len(text.split())


def is_palindrome(text: str) -> bool:
    """Check whether text reads the same forwards and backwards (letters/digits only)."""
    cleaned = re.sub(r"[^a-z0-9]", "", text.lower())
    return cleaned == cleaned[::-1]
