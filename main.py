import argparse
import pandas as pd
from score import * 

def main():
    # Define the parser
    parser = argparse.ArgumentParser(description="Wordle Calculator")
    parser.add_argument('-i', '--id', type=int, default=-1, help="The id of game to calculate, -1 for last game played")
    args = parser.parse_args()

    games_df = pd.read_csv("games.csv")
    game_calc = games_df.iloc[args.id]
    word, guesses = game_calc
    game = guesses.split('-')
    
    grade = score_game(game, word)
    
    print(f"The performance is graded as {grade}")
    

if __name__ == "__main__":
    main()