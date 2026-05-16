import pytest
import grade

def test_all_green():
    assert grade.get_pattern('crane', 'crane') == 'GGGGG'


def test_all_black():
    assert grade.get_pattern('crane', 'bults') == 'BBBBB'


@pytest.mark.parametize("word, guess, expected", [
    ("could", "cooks", "GGBBB"),
    ("above", "books", "YYBBB"),
    ("llama", "alone", "YBBBY"),
    ("eerie", "geese", "YYBBY"),
    ("lulls", "lolls", "GBBGG"),
])
def test_duplicate_letters():
    assert grade.get_pattern('eerie', 'stern') == 'BBYYB'