import argparse
import pandas as pd

def read_valid_words():
    '''Reads the posible wordle words
    
    Returns:
        The set of all possible wordle words
    '''
    words = set() 
    with open("valid_wordle_words.txt", "r") as file:
        for line in file.readlines():
            word = line.strip()
            words.add(word)

    return words


def remove_invalid_words(valid_words, grey_chars, yellow_chars, green_chars): 
    '''Removes words that have been invalidated
    
    Args:
        valid_words:previous words that were valid
        grey_chars : 
    '''
    for word in valid_words:
        valid = True
        i = 0
        # Check green chars
        while i < 5 and valid:
            if green_chars[i] != '' and green_chars[i] != word[i]:
                valid = False

            i += 1
        
        i = 0 

        # Check yellow chars
        while i < 5 and valid:
            if yellow_chars:
                pass
            
                
            


def information_gain(valid_words, word):
    '''Calculates information gain from a word, i.e. the entropy difference
    
    Args:
        valid_words : set of all valid words
        word : the guessed word
    
    Returns:
        An number for amount of information gain
    '''
    
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
