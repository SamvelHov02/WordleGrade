from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
import sqlite3
import hashlib
import hmac
import secrets
from score import score_game, score_guess_AIG, score_guess_EIG
from grade import get_pattern
import utils
import db


@asynccontextmanager
async def lifespan(app : FastAPI):
    db.init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory='../client/public'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.nytimes.com"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

# Auth Helpers 
PBKDF2_ITERATIONS = 600_000

SESSIONS : dict[str, int] = {}

def hash_password(password : str) -> str:
    """Hashes a password with random salt and RBKDF2"""
    
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt, PBKDF2_ITERATIONS
    )
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password : str, hashed_password : str) -> bool:
    try:
        algorithm, iterations, salt, hash_hex = hashed_password.split('$')
        if algorithm != 'pbkdf2_sha256':
            return False
        digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            bytes.fromhex(salt),
            int(iterations)
        )
        return hmac.compare_digest(digest.hex(), hash_hex)
    except (ValueError, TypeError):
        return False 
    
    
def get_current_user(authorization : str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Not authenticated')
    
    token = authorization.removeprefix('Bearer ')
    user_id = SESSIONS.get(token)
    
    if user_id is None:
        raise HTTPException(status_code=401, detail='Invalid or expired session')
    
    user = db.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail='User no longer exists')
    
    return user


class Game(BaseModel):
    game : list[str]
    metric : str = 'expected'
    token : str | None = None

@app.post('/api/grade')
async def grade(game : Game, user : dict = Depends(get_current_user)):
    metric_fn = score_guess_EIG
    if game.metric != 'expected':
        metric_fn = score_guess_AIG

    answer = utils.get_todays_word();
    guesses = game.game
    guesses = list(map(lambda x : x.lower(), guesses))
    
    grade, _ = score_game(word=answer, game=guesses, metric_fn=metric_fn)
    
    # Update database
    if user is not None:
        db.create_game(
            user_id = user['user_id'],
            target_word=answer,
            grade=grade,
            guesses=guesses    
        )

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



class Credentials(BaseModel):
    username : str = Field(min_length=6, max_length=16)
    password : str = Field(min_length=6, max_length=64)
    

@app.post('/api/register', status_code=201)
async def register(credentials : Credentials):
    username = credentials.username.strip().lower()
    
    try:
        user = db.add_user(
            username=username,
            password_hash=hash_password(credentials.password)
        )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail='Username already taken')
    
    return {
        'user_id' : user['user_id'],
        'username' : user['username'],
        'created_at' : user['created_at'],
    } 


@app.post('/api/login')
async def login(credentials : Credentials):
    username = credentials.username.strip().lower()
    user = db.get_user_by_username(username=username)
    
    stored_hash = user['password_hash'] if user else hash_password('invalid')
    if user is None or not verify_password(credentials.password, stored_hash):
        raise HTTPException(status_code=401, detail='Invalid username or password')
    
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = user['user_id']
    
    return {
        'token' : token,
        'username' : user['username'],
        'created_at' : user['created_at']
    }
    

@app.post('/api/logout')
async def logout(authorization : str | None = Header(default=None)):
    user = get_current_user(authorization=authorization)
    token = authorization.removeprefix('Bearer ')
    SESSIONS.pop(token, None)
    return {'detail' : f'Logged out {user['username']}'}


@app.get('/api/me')
async def me(authorization : str | None = Header(default=None)):
    user = get_current_user(authorization=authorization)
    return {
        'user_id' : user['user_id'],
        'username' : user['username'],
        'created_at' : user['created_at']
    }