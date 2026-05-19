import argparse
import pandas as pd
from math import log2
import os

def read_valid_words():
    '''Reads the posible wordle words
    
    Returns:
        Set : All possible wordle words
    '''
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "valid-wordle-words.txt")
    words = set() 
    with open(path, "r") as file:
        for line in file.readlines():
            word = line.strip()
            words.add(word)

    return words


def green_valid(green_chars, word):
    """Checks if a word is invalidated by the green cells
    
    Args:
        green_chars (list) : list of 5 elements with the green cell information
        word (str) : The word examined for invalidation
        
    Returns:
        Boolean : A boolean whether or not the word is still possible
    """
    valid = True
    i = 0
    # Check green chars
    while i < 5 and valid:
        if green_chars[i] != '' and green_chars[i] != word[i]:
            valid = False

        i += 1

    return valid

def yellow_valid(yellow_chars, word):
    """Checks if a word is invalidated by the yellow cells
    
    Args:
        yellow_chars (dict) : positional keys and list of yellow characters
        word (str) : The word examined for invalidation
        
    Returns:
        Boolean : A boolean whether or not the word is still possible
    """
    for char, count in yellow_chars.items():
        char_in_word = len(list(filter(lambda x : x == char, word)))
        if count > char_in_word:
            return False 

    return True 

def grey_valid(grey_chars, word):
    """Checks if a word is invalidated by the grey cells

    Args:
        grey_chars (set) : All characters that are grey 
        word (str) : The word examined for invalidation

    Returns:
        Boolean : whether or not the word is valid
    """
    i = 0
    valid = True
    while valid and i < 5:
        char = word[i]
        if char in grey_chars:
            valid=False
        i+=1

    return valid

def remove_invalid_words(valid_words, word, guess): 
    '''Removes words that have been invalidated
    
    Args:
        valid_words (set) : previous words that were valid
        word (str)  : the actual word of the game 
        guess (str) : the word player has used  
         
    Returns:
        set : remaining valid words after word is guessed
    '''
    updated_valid_words = valid_words.copy()

    pattern = get_pattern(word, guess)
    green_chars = ["" for _ in range(5)]
    # Yellow chars a mapping between character in the word and number of occurence
    yellow_chars = {c : 0 for c in list(word)}
    black_chars = set()
    
    for i, p in enumerate(pattern):
        char = guess[i]
        if p == "G":
            green_chars[i] = char 
        elif p == "Y":
            yellow_chars[char] += 1
        # The guess word might have characters that are duplicates
        elif guess[i] not in yellow_chars:
            black_chars.add(char)
    
    for candidate in valid_words:
        valid_g = lambda : green_valid(green_chars, candidate)
        valid_y = lambda : yellow_valid(yellow_chars, candidate)
        valid_b = lambda : grey_valid(black_chars, candidate)
        
        if not valid_g() or not valid_y() or not valid_b():
            updated_valid_words.remove(candidate)
    
    return updated_valid_words


def get_pattern(word, guess):
    """Shows the pattern for guess word

    Args:
        word (str): Word of the day
        guess (str): Guessed word
    
    Returns:
        str : a string pattern e.g. GYBGB
    """
    pattern = ["" for _ in range(5)]
    # Check for green and black cells
    for i, char in enumerate(guess):
        if char == word[i]: pattern[i]  = 'G'
        elif char not in word : pattern[i] = 'B'
        
    guess_not_marked = [x for x, c in enumerate(pattern) if c == ""]
    unique_char_left_guess = {guess[j] : [] for j in guess_not_marked} 
    unique_char_left_word = {guess[j] : [] for j in guess_not_marked} 
    
    # Need mapping between (potential) yellow chars and indices in guess 
    for i in guess_not_marked:
        unique_char_left_guess[guess[i]].append(i)

    # Need mapping between chars and indicies in actual word
    for char in unique_char_left_guess.keys():
        indicies = [j for j, wc in enumerate(word) if wc == char and pattern[j] != 'G']
        unique_char_left_word[char] = indicies
    
    for char, indicies in unique_char_left_guess.items():
        mid = min(len(indicies), len(unique_char_left_word[char]))
        for idx in indicies[:mid]:
            pattern[idx] = 'Y'
        
        for idx in indicies[mid:]:
            pattern[idx] = 'B'
        
    return "".join(pattern)


def information_gain(valid_words, guess):
    '''Calculates information gain from a word, i.e. the entropy difference
    
    Args:
        valid_words (set) : All valid words
        guess (str): the guessed word
    
    Returns:
        float : Amount of information gain
    '''
    size = len(valid_words)
    buckets = {} 
    
    # Assuming word is the final word which pattern would guess word create
    for word in valid_words:
        pattern = get_pattern(word, guess)
        buckets[pattern] = buckets.get(pattern, 0) + 1
        
    # Calculate the information gain
    entropy_before = log2(size) 
    entropy_after = 0
    for pattern, count in buckets.items():
        prob = count / size
        entropy_after += prob * log2(count)
        
    return entropy_before - entropy_after