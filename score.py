from grade import *  
from math import ceil

def score_guess_EIG(valid_words, guess):
    """Scores a guess relative to best possible guess, according to Expected Information Gain
    
    Args : 
        valid_words (set) : Still possible words
        guess (str) : Guess word to be evalauted
        
    Returns :
        tuple(float, str, float) : A tuple with ratio of quality of the guess, best possible word and information_gain of hte best word
    """
    # If only one possible word left, return 1.0 if its the word otherwise 0
    if len(valid_words) == 1:
        return (1.0, guess, 0.0) if guess in valid_words else (0.0, valid_words[0], 0.0)
    
    word_to_inf_gain = {} # mapping between word and inforamtion gain
    # Need to get information gain of all possible guesses
    for word in valid_words:
        word_to_inf_gain[word] = information_gain_EIG(valid_words, word)
    
    
    sorted_inf_gain = sorted(word_to_inf_gain.items(), key=lambda x : x[1], reverse=True)     
    
    best_word, most_gain = sorted_inf_gain[0]
    guess_gain = word_to_inf_gain.get(guess, 0)
    
    return (guess_gain / most_gain, best_word, most_gain)


def score_guess_AIG(valid_words, guess, word):
    '''Scores a guess relative to best possible guess, according to Actual information gain
    
    Args:
        valid_words (set) : All valid words
        guess (str) : the guess word
        word (str) : Actual wordle word
        
    Returns:
        float : Relative information gain 
    '''
    if len(valid_words) == 1:
        return 0.0
    elif guess == word:
        return 1.0
    else:
        ig = information_gain_AIG(valid_words, guess, word)

def score_game(game, word, metric_fn, *args):
    """Scores a game based on words
    
    Args :
        game (list) : The guesses player made in the game
        word (str) : The answer for the wordle game
    
    Returns :
        tuple(str, list(tuple(float, str, float))) : A grade from A - F and a list of information for each guess 
    """
    valid_words = read_valid_words()
    total_score = 0
    # stores the information about each guess
    optimal_game = []
    for i, guess in enumerate(game):
        # Treat the first guess as "free"
        if i != 0: 
            # print(metric_fn(valid_words, guess))
            score, b_word, b_gain = metric_fn(valid_words, guess, *args)
            total_score += score 
            optimal_game.append((score, b_word, b_gain))

        valid_words = remove_invalid_words(valid_words, word, guess)
        
    # Translate numeric score to a character grade
    avg_score = total_score / (len(word) - 1)
    
    if avg_score >= 0.90: return ("A", optimal_game)
    if avg_score >= 0.75: return ("B", optimal_game)
    if avg_score >= 0.60: return ("C", optimal_game)
    if avg_score >= 0.45: return ("D", optimal_game)
    return ("F", optimal_game)