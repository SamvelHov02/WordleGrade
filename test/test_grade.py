import pytest
import grade

def test_all_green():
    assert grade.get_pattern('crane', 'crane') == 'GGGGG'


def test_all_black():
    assert grade.get_pattern('crane', 'bults') == 'BBBBB'


@pytest.mark.parametrize("word, guess, expected", [
    ("could", "cooks", "GGBBB"),
    ("above", "books", "YBGBB"),
    ("llama", "alone", "YGBBB"),
    ("eerie", "geese", "BGYBG"),
    ("lulls", "lolls", "GBGGG"),
    ("steel", "eerie", "YYBBB")
])
def test_duplicate_letters(word, guess, expected):
    assert grade.get_pattern(word, guess) == expected
    

def test_no_information_gain():
    words = {"aaaaa", "bbbbb", "ccccc", "ddddd", "eeeee"}
    assert grade.information_gain(words, "zzzzz") == pytest.approx(0.0)
    

def test_perfect_split_information_gain():
    words = {"aaaaa", "bbbbb", "ccccc", "ddddd", "eeeee"}
    assert grade.information_gain(words, "abcde") == pytest.approx(2.0)
    

# def test_uneven_split_information_gain():
#     pass