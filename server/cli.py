import argparse
import pandas as pd
from score import * 

def main():
    # Define the parser
    parser = argparse.ArgumentParser(description="Wordle Calculator")
    parser.add_argument('-i', '--id', type=int, default=-1, help="The id of game to calculate, -1 for last game played")
    parser.add_argument('-v', '--verbose', action='store_true', help='Enables verbose output')
    parser.add_argument('-m', '--metric', type=str, default='EIG', help="Grader metric to be used for grading")
    args = parser.parse_args()

    games_df = pd.read_csv("games.csv")
    game_calc = games_df.iloc[args.id]
    word, guesses = game_calc
    game = guesses.split('-')

    metric = args.metric

    if metric == "EIG":
        grade, opt_game = score_game(game, word, score_guess_EIG)
    elif metric == "AIG":
        grade, opt_game = score_game(game, word, score_guess_AIG)
    
    grade, opt_game = score_game(game, word)
    
    if args.verbose:
        for i, guess in enumerate(game[1:]):
            print(f"Guess was : {guess : <30} Opt word : {opt_game[i][1] : <5}  Opt E[IG] : {opt_game[i][2] : <5}")
    
    print(f"The performence gets a {grade}") 

if __name__ == "__main__":
    main()