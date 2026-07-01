from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from score import score_game, score_guess_AIG, score_guess_EIG
from grade import get_pattern
import utils


app = FastAPI()
app.mount('/static', StaticFiles(directory='../client/public'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.nytimes.com"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

class Game(BaseModel):
    game : list[str]
    metric : str = 'expected'

@app.post('/api/grade')
async def grade(game : Game):
    metric_fn = score_guess_EIG
    if game.metric != 'expected':
        metric_fn = score_guess_AIG

    answer = utils.get_todays_word();
    guesses = game.game
    guesses = list(map(lambda x : x.lower(), guesses))
    
    grade, _ = score_game(word=answer, game=guesses, metric_fn=metric_fn)
    return {
        'grade' : grade
    }

@app.get('/api/pattern')
async def pattern(guess : str):
    guess = guess.lower()
    word = utils.get_todays_word() 
    pattern = get_pattern(word=word, guess=guess) 
    
    return_json = {'pattern' :{}} 
    
    for i, color in enumerate(pattern):
        match color:
            case 'G':
                return_json['pattern'][i] = 'green'
            case 'Y':
                return_json['pattern'][i] = 'yellow'
            case 'B':
                return_json['pattern'][i] = 'black'
    
    return return_json