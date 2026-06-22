import pytest
import utils

@pytest.mark.parametrize("date, expected", [
    ("2026-06-21", "areas"),
    ("2026-07-01", "penis"),
    ("2026-06-29", "cocks"),
    ("2026-07-02", "skate")
])
def test_get_todays_word(date : str, expected : str):
    actual = utils.get_todays_word(date)
    assert actual == expected

