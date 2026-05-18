import pytest
from score import *
from grade import *

def test_perfect_guess_score():
    valid_words = {"crane", "crate", "trace", "react", "carer"}
    best_word = max(valid_words, key=lambda w : information_gain(valid_words, w))
    assert score_guess(valid_words, best_word) == 1.0
    

def test_no_score_guess_score():
    valid_words = {"crane", "crate", "trace", "react", "carer"}
    guess = "tests"
    assert score_guess(valid_words, guess) == 0.0

def test_suboptimal_guess_score_less():
    valid_words = {"crane", "crate", "trace", "react", "carer"}
    worst_word = min(valid_words, key=lambda w: information_gain(valid_words, w))
    best_word = max(valid_words, key=lambda w : information_gain(valid_words, w))
    
    if best_word != worst_word:
        assert score_guess(valid_words, worst_word) < score_guess(valid_words, best_word)
        
def test_score_is_bounded():
    valid_words = {"crane", "crate", "trace", "react", "carer"}
    for word in valid_words:
        word_score = score_guess(valid_words, word)
        assert 0.0 <= word_score <= 1.0 + 1e-9
        
def test_valid_game_grade():
    answer = ""
    game = [""]
    assert score_game(game, answer) in {"A", "B", "C", "D", "F"}
    
def test_first_guess_win():
    """Tests that the program doesn't crash"""
    answer = "crane"
    game = ["crane"]
    assert score_game(game, answer) in {"A", "B", "C", "D", "F"}

def test_optimal_game():
    valid_words = {"tares", "crane", "clean", "steal", "bills", "tiles", "eerie", "about", "truce", "alley"}
    answer = "bills"
    game = ["zzzzz"]
    # Setup find an optimal game, might be more than 6 guesses 
    updated_valid_words = valid_words.copy()
    updated_valid_words = remove_invalid_words(updated_valid_words, answer, game[0])
    while True:
        best_word = max(valid_words, key=lambda w : information_gain(updated_valid_words, w))
        game.append(best_word)
        
        if best_word == answer:
            break
        
        updated_valid_words = remove_invalid_words()

    assert score_game(game, answer) == 'A'