import pytest
from score import *
from grade import *

def test_perfect_guess_score_EIG():
    valid_words = {"crane", "crate", "trace", "react", "carer"}
    best_word = max(valid_words, key=lambda w : information_gain_EIG(valid_words, w))
    score, _, _ = score_guess_EIG(valid_words, best_word)
    assert score == 1.0
    

def test_no_score_guess_score_EIG():
    valid_words = {"crane", "crate", "trace", "react", "carer"}
    guess = "tests"
    score, _, _ = score_guess_EIG(valid_words, guess)
    assert score == 0.0

def test_suboptimal_guess_score_less_EIG():
    valid_words = {"crane", "crate", "trace", "react", "carer"}
    worst_word = min(valid_words, key=lambda w: information_gain_EIG(valid_words, w))
    best_word = max(valid_words, key=lambda w : information_gain_EIG(valid_words, w))
    
    if best_word != worst_word:
        score_less, _, _ = score_guess_EIG(valid_words, worst_word)
        score_more, _, _ = score_guess_EIG(valid_words, best_word)
        assert score_less < score_more 
        
def test_score_is_bounded_EIG():
    valid_words = {"crane", "crate", "trace", "react", "carer"}
    for word in valid_words:
        word_score, _, _= score_guess_EIG(valid_words, word)
        assert 0.0 <= word_score <= 1.0 + 1e-9
        
def test_valid_game_grade_EIG():
    answer = "crane"
    game = ["stain", "drops", "clean", "crane"]
    grade, _ = score_game(game, answer, score_guess_EIG)
    assert grade in {"A", "B", "C", "D", "F"}
    
def test_first_guess_win_EIG():
    """Tests that the program doesn't crash"""
    answer = "crane"
    game = ["crane"]
    grade, _ = score_game(game, answer, score_guess_EIG)
    assert grade in {"A", "B", "C", "D", "F"}

# def test_optimal_game():
#     valid_words = {"tares", "crane", "clean", "steal", "bills", "tiles", "eerie", "about", "truce", "alley"}
#     answer = "bills"
#     game = ["zzzzz"]
#     # Setup find an optimal game, might be more than 6 guesses 
#     updated_valid_words = valid_words.copy()
#     updated_valid_words = remove_invalid_words(updated_valid_words, answer, game[0])
#     while True:
#         print("Does it get here")
#         best_word = max(valid_words, key=lambda w : information_gain(updated_valid_words, w))
#         game.append(best_word)
        
#         if best_word == answer:
#             break
        
#         updated_valid_words = remove_invalid_words(updated_valid_words, answer, best_word)

#     assert score_game(game, answer) == 'A'