from fastapi import FastAPI
from pydantic import BaseModel
from score import score_game, score_guess_AIG, score_guess_EIG


app = FastAPI()

class Game(BaseModel):
    word : str
    game : list[str]
    metric : str = 'expected'

@app.post('/grade')
async def grade(game : Game):
    metric_fn = score_guess_EIG
    if game.metric != 'expected':
        metric_fn = score_guess_AIG

    answer = game.word
    guesses = game.game
    
    grade, _ = score_game(word=answer, game=guesses, metric_fn=metric_fn)
    return {
        'grade' : grade
    }
    