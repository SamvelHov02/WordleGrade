"""Tests Database operations with a temporary database"""
import sqlite3
import pytest
import db

@pytest.fixture
def fresh_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db")) 
    db.init_db()

@pytest.fixture
def alice(fresh_db):
    return db.add_user("alice", "fakehash")


def test_add_user(fresh_db):
    user = db.add_user("bob", "fakehash")
    assert user["username"] == "bob"
    assert user["password_hash"] == "fakehash"
    assert user["user_id"] == 1
    

def test_get_user_by_id(alice):
    user = db.get_user_by_id(alice["user_id"])
    assert user == alice

    
def test_get_user_by_username(alice):
    assert alice == db.get_user_by_username("alice")

    
def test_missing_user_returns_none(fresh_db):
    assert db.get_user_by_id(999) is None
    assert db.get_user_by_username("nobody") is None
    
    
def test_duplicate_username_rejected(alice):
    with pytest.raises(sqlite3.IntegrityError):
        db.add_user("alice", "otherhash")
        

def test_failed_insert_leaves_no_row(alice):
    with pytest.raises(sqlite3.IntegrityError):
        db.add_user("alice", "otherhash")
    assert db.get_user_by_username("alice")["password_hash"] == "fakehash"
    

def test_create_game_returns_game_with_guesses(alice):
    game = db.create_game(alice["user_id"], "CRANE", "F", [])
    assert game["target_word"] == "CRANE"
    assert game["grade"] == "F"


def test_missing_game_returns_none(fresh_db):
    assert db.get_game(999) is None


def test_get_user_games_newest_first(alice):
    first = db.create_game(alice["user_id"], "CRANE", "F", [])
    second = db.create_game(alice["user_id"], "PLUMB", "C", [])
    games = db.get_user_games(alice["user_id"])
    assert [g["game_id"] for g in games] == [second["game_id"], first["game_id"]]


def test_get_user_games_by_username(alice):
    db.create_game(alice["user_id"], "CRANE", "A", [])
    games = db.get_user_games_by_username("alice")
    assert len(games) == 1
    assert games[0]["target_word"] == "CRANE"
    
    
def test_games_by_unknown_username_returns_empty_list(fresh_db):
    assert db.get_user_games_by_username("nobody") == []


# ---------------------------------------------------------------------------
# Guesses
# ---------------------------------------------------------------------------

def test_add_guess_returns_correct_fields(alice):
    game = db.create_game(alice["user_id"], "CRANE", "A", [])
    g = db.add_guess(game["game_id"], "SLATE")
    assert g["guess"] == "SLATE"
    assert g["game_id"] == game["game_id"]
    assert "guess_id" in g
    assert "guess_number" in g


def test_add_guess_numbers_are_sequential(alice):
    game = db.create_game(alice["user_id"], "CRANE", "A", [])
    g0 = db.add_guess(game["game_id"], "SLATE")
    g1 = db.add_guess(game["game_id"], "CRANE")
    assert g1["guess_number"] == g0["guess_number"] + 1


def test_get_game_guesses_returns_all(alice):
    game = db.create_game(alice["user_id"], "CRANE", "B", [])
    db.add_guess(game["game_id"], "SLATE")
    db.add_guess(game["game_id"], "CRANE")
    guesses = db.get_game_guesses(game["game_id"])
    assert len(guesses) == 2
    assert [g["guess"] for g in guesses] == ["SLATE", "CRANE"]


def test_get_game_guesses_empty_returns_empty_list(alice):
    game = db.create_game(alice["user_id"], "CRANE", "B", [])
    assert db.get_game_guesses(game["game_id"]) == []


def test_guesses_are_scoped_to_game(alice):
    game1 = db.create_game(alice["user_id"], "CRANE", "A", [])
    game2 = db.create_game(alice["user_id"], "PLUMB", "B", [])
    db.add_guess(game1["game_id"], "SLATE")
    assert db.get_game_guesses(game2["game_id"]) == []


def test_add_guess_invalid_game_id_raises(fresh_db):
    with pytest.raises(sqlite3.IntegrityError):
        db.add_guess(9999, "SLATE")


def test_create_game_stores_guesses(alice):
    db.create_game(alice["user_id"], "CRANE", "B", ["SLATE", "CRANE"])
    games = db.get_user_games(alice["user_id"])
    guesses = db.get_game_guesses(games[0]["game_id"])
    assert [g["guess"] for g in guesses] == ["SLATE", "CRANE"]