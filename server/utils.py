from datetime import date, datetime
from pathlib import Path
import json

def get_todays_word(day : str | None) -> str | None:
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
