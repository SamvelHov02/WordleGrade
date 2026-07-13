"""This file defines functions that define a SQLite database"""
import sqlite3
from datetime import datetime, timezone
from contextlib import contextmanager

DB_PATH = "wordle.db"
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    current_streak INTEGER NOT NULL DEFAULT 0,
    best_streak INTEGER NOT NULL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    target_word TEXT NOT NULL,
    grade TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'defeat' CHECK (status IN ('victory', 'defeat')),
    played_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS guesses (
    guess_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    guess_number INTEGER NOT NULL,
    guess TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);
"""

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn
     

@contextmanager
def db_session():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Initialize the Database"""
    with db_session() as conn:
        conn.executescript(SCHEMA)


def _now():
    return datetime.now(timezone.utc).isoformat()

# ---------------------------------------------------------------------------
# User Operations
# ---------------------------------------------------------------------------

def add_user(username : str, password_hash : str):
    with db_session() as conn:
        cur = conn.execute(
            """INSERT INTO users (username, password_hash, current_streak, best_streak, created_at)
            VALUES (?, ?, 0, 0, ?)""",
            (username, password_hash, _now()),
        )

        row = conn.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (cur.lastrowid,) 
        ).fetchone()
        return dict(row)
    

def get_user_by_id(user_id : int):
    with db_session() as conn:
        row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return dict(row) if row else None
    
    
def get_user_by_username(username : str):
    with db_session() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return dict(row) if row else None


def create_game(user_id : int, target_word : str,  grade : str, status : str, guesses : list[str]):
    with db_session() as conn:
        cur = conn.execute(
            """INSERT INTO games (user_id, target_word, grade, status, played_at)
            VALUES (?, ?, ?, ?, ?)""",
            (user_id, target_word, grade, status, _now()),
        )

        game_id = cur.lastrowid
        row = conn.execute(
            "SELECT * FROM games WHERE game_id = ?", (game_id,)
        ).fetchone()

        for i, g in enumerate(guesses):
            conn.execute(
                "INSERT INTO guesses (game_id, guess_number, guess) VALUES (?,?,?)",
                (game_id, i, g),
            )

        if status == "victory":
            conn.execute(
                """UPDATE users
                SET current_streak = current_streak + 1,
                    best_streak = MAX(best_streak, current_streak + 1)
                WHERE user_id = ?""",
                (user_id,),
            )
        else:
            conn.execute(
                "UPDATE users SET current_streak = 0 WHERE user_id = ?",
                (user_id,),
            )

        return dict(row)
    

def get_game(game_id : int):
    with db_session() as conn:
        row = conn.execute(
            "SELECT * FROM games WHERE game_id = ?", (game_id,)
        ).fetchone()
        
        return dict(row) if row else None
    

def get_user_games(user_id : int):
    with db_session() as conn:
        rows = conn.execute(
            "SELECT * FROM games WHERE user_id = ? ORDER BY played_at DESC", (user_id, )
        ).fetchall()
        
        return [dict(r) for r in rows]

        
def get_user_games_by_username(username : str):
    user_row = get_user_by_username(username)
    if user_row is None:
        return []

    return get_user_games(user_row["user_id"])
        

def add_guess(game_id : int, guess_word : str):
    with db_session() as conn:
        count = conn.execute(
            "SELECT COUNT(*) AS c FROM guesses WHERE game_id = ?", (game_id,)
        ).fetchone()["c"]
        
        cur = conn.execute(
            """INSERT INTO guesses (game_id, guess_number, guess)
            VALUES (?,?,?)""",
            (game_id, count, guess_word)
        )
        
        row = conn.execute(
            "SELECT * FROM guesses WHERE guess_id = ?", (cur.lastrowid,)
        ).fetchone()
        
        return dict(row)
    
    
def get_game_guesses(game_id : int):
    with db_session() as conn:
        rows = conn.execute(
            "SELECT * FROM guesses WHERE game_id = ?", (game_id,)
        ).fetchall() 
        
        return [dict(r) for r in rows] 