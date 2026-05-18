from grade import *  
from math import ceil

def score_guess(valid_words, guess):
    """Scores a guess relative to best possible guess
    
    Args : 
        valid_words (set) : Still possible words
        guess (str) : Guess word to be evalauted
        
    Returns :
        str : A grade from A - F
    """
    word_to_inf_gain = {} # mapping between word and inforamtion gain
    # Need to get information gain of all possible guesses
    for word in valid_words:
        word_to_inf_gain[word] = information_gain(valid_words, word)
    
    
    sorted_inf_gain = sorted(word_to_inf_gain.items(), key=lambda x : x[1], reverse=True)     
    
    _, most_gain = sorted_inf_gain[0]
    guess_gain = word_to_inf_gain.get(guess, 0)
    
    return guess_gain / most_gain


def score_game(game, word):
    """Scores a game based on words
    
    Args :
        game (list) : The guesses player made in the game
    
    Returns :
        str : A grade from A - F
    """
    valid_words = read_valid_words()
    total_score = 0
    for i, guess in enumerate(game):
        # Treat the first guess as "free"
        if i != 0: 
            total_score += score_guess(valid_words, guess)

        valid_words = remove_invalid_words(valid_words, word, guess)
        
    # Translate numeric score to a character grade
    avg_score = total_score / (len(word) - 1)
    
    if avg_score >= 0.90: return "A"
    if avg_score >= 0.75: return "B"
    if avg_score >= 0.60: return "C"
    if avg_score >= 0.45: return "D"
    return "F"