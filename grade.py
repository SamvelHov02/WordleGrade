import argparse
import pandas as pd

def read_valid_words():
    '''Reads the posible wordle words
    
    Returns:
        Set : All possible wordle words
    '''
    words = set() 
    with open("valid_wordle_words.txt", "r") as file:
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
    valid = True

    for i in list(yellow_chars.keys()): 
        for char in yellow_chars[i]:
            if char not in word:
                valid = False

    return valid

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

def remove_invalid_words(valid_words, grey_chars, yellow_chars, green_chars): 
    '''Removes words that have been invalidated
    
    Args:
        valid_words (set) : previous words that were valid
        grey_chars (set) : the accumalted grey characters
        yellow_chars (dict) : Yellow characters per position
        green_chars (list) : Contains correctly revealed characters
    
    Returns:
        set : remaining valid words after word is guessed
    '''
    updated_valid_words = valid_words.copy()
    
    for word in valid_words:
        valid_green = lambda : green_valid(green_chars, word)
        valid_yellow = lambda : yellow_valid(yellow_chars, word)
        valid_grey = lambda : grey_valid(grey_chars, word)
        
        if not valid_green() and not  valid_yellow() and not valid_grey():
            updated_valid_words.remove(word)     
    
    return updated_valid_words

def information_gain(valid_words, guess):
    '''Calculates information gain from a word, i.e. the entropy difference
    
    Args:
        valid_words (set) : All valid words
        guess (str): the guessed word
    
    Returns:
        float : Amount of information gain
    '''
    buckets = {} 
    
    # Assuming word is the final word which pattern would guess word create
    for word in valid_words:
        pass 
    
    
def main():
    # Define the parser
    parser = argparse.ArgumentParser(description="Wordle Calculator")
    parser.add_argument('-i', '--id', type=int, default=-1, help="The id of game to calculate, -1 for last game played")
    args = parser.parse_args()

    games_df = pd.read_csv("games.csv")
    game_calc = games_df.iloc[args.id]
    word, guesses = game_calc["guesses"]
    guesses = guesses.split('-')
    valid_words = read_valid_words()
    
    grey_chars = set()
    yellow_chars = {i:[] for i in range(5)}
    green_chars = ['' for _ in range(5)]
    
    for i, guess in enumerate(guesses):
        for j, char in enumerate(list(guess)):
            if char == word[j]:
                green_chars[j] = char
            elif char in word[j:]:
                yellow_chars[j].append(char)
            else:
                grey_chars.add(char)
                
        new_valid_words = remove_invalid_words()
        # Treat all first guesses as equal 
        if i != 0:
            # Calculate how good the guess was
            pass 
        
        valid_words = new_valid_words 
            
            
    

if __name__ == "__main__":
    main()
