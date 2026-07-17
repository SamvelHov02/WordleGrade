from datetime import date, datetime
from pathlib import Path
import json
import db 

def get_todays_word(day : str | None = None) -> str | None:
    """Retrieves the word for today's Wordle
    
    Args:
        day (str) : A specific date for retrieving word
        
    Returns:
        str : Wordle word of today
    """
    HERE = Path(__file__).resolve().parent

    with open(HERE / 'answers.json', 'r') as file:
        answers = json.load(file)

    if day is None:
        today = date.today()
    else:
        today = datetime.strptime(day, "%Y-%m-%d").date()

    return answers.get(today.strftime('%Y-%m-%d'))


def most_recent_k_games(games : list, k=5, verbose=False):
    """Retrieves the k most recent games"""
    sorted_games =  sorted(games, key= lambda g : g['played_at'], reverse=True)
    if  verbose : return sorted_games[:k] 
    
    relevant_games = sorted_games[:k]
    short_games = []
    for game in relevant_games:
        game_id = game['game_id']
        tot_guesses = len(db.get_game_guesses(game_id))
        grade = game['grade']
        short_games.append({
            'total_guesses' : tot_guesses if game['status'] == 'victory' else 'X',
            'grade' : grade
        });

    return short_games

    
def get_won_games(games : list):
    """Filters out games that were lost"""
    return list(filter(lambda g : g['status'] == 'victory', games))

    
def grade_distribution(games : list):
    """Gets the grade distribution"""
    grades = {
        'A' : 0, 'B' : 0, 'C' : 0, 'D' : 0, 'E' : 0, 'F' : 0
    }
    
    for game in games:
        grade = game['grade']
        grades[grade] += 1
    
    return grades