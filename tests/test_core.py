import pytest
from textutils import slugify, word_count, is_palindrome


@pytest.mark.parametrize("raw, expected", [
    ("Hello World", "hello-world"),
    ("  Jenkins -- Rocks!  ", "jenkins-rocks"),
    ("Multiple   spaces", "multiple-spaces"),
])
def test_slugify(raw, expected):
    assert slugify(raw) == expected


def test_word_count():
    assert word_count("one two  three") == 3
    assert word_count("") == 0


def test_is_palindrome():
    assert is_palindrome("A man, a plan, a canal: Panama")
    assert not is_palindrome("Jenkins")
