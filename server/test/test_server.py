"""Tests the FastAPI endpoints in main.py with a temporary database"""
import pytest
from fastapi.testclient import TestClient
import db
import main

CREDENTIALS = {"username": "alice123", "password": "secret-pass"}


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.setattr(main, "SESSIONS", {})
    # Keep password hashing fast in tests
    monkeypatch.setattr(main, "PBKDF2_ITERATIONS", 1000)
    # Fixed answer so tests don't depend on the calendar
    monkeypatch.setattr(main.utils, "get_todays_word", lambda day=None: "crane")
    # score_game is expensive, endpoint tests only care about the HTTP layer
    monkeypatch.setattr(main, "score_game", lambda word, game, metric_fn: ("A", []))
    # played_at is UNIQUE and date-only, so each call must yield a fresh date
    fake_dates = (f"2026-07-{day:02d}" for day in range(1, 29))
    monkeypatch.setattr(db, "_now", lambda: next(fake_dates))
    with TestClient(main.app) as test_client:
        yield test_client


@pytest.fixture
def registered(client):
    response = client.post("/api/register", json=CREDENTIALS)
    assert response.status_code == 201
    return client


@pytest.fixture
def token(registered):
    response = registered.post("/api/login", json=CREDENTIALS)
    return response.json()["token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Password helpers
# ---------------------------------------------------------------------------

def test_hash_and_verify_password_roundtrip(monkeypatch):
    monkeypatch.setattr(main, "PBKDF2_ITERATIONS", 1000)
    hashed = main.hash_password("secret-pass")
    assert main.verify_password("secret-pass", hashed)


def test_verify_password_rejects_wrong_password(monkeypatch):
    monkeypatch.setattr(main, "PBKDF2_ITERATIONS", 1000)
    hashed = main.hash_password("secret-pass")
    assert not main.verify_password("wrong-pass", hashed)


def test_hashes_are_salted(monkeypatch):
    monkeypatch.setattr(main, "PBKDF2_ITERATIONS", 1000)
    assert main.hash_password("secret-pass") != main.hash_password("secret-pass")


def test_verify_password_rejects_malformed_hash():
    assert not main.verify_password("secret-pass", "not-a-real-hash")
    assert not main.verify_password("secret-pass", "md5$1000$aa$bb")


# ---------------------------------------------------------------------------
# /api/register
# ---------------------------------------------------------------------------

def test_register_creates_user(client):
    response = client.post("/api/register", json=CREDENTIALS)
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "alice123"
    assert "user_id" in body
    assert "created_at" in body


def test_register_does_not_leak_password(client):
    body = client.post("/api/register", json=CREDENTIALS).json()
    assert "password" not in body
    assert "password_hash" not in body


def test_register_normalizes_username(client):
    response = client.post(
        "/api/register",
        json={"username": "  ALICE123 ", "password": "secret-pass"},
    )
    assert response.json()["username"] == "alice123"


def test_register_duplicate_username_rejected(registered):
    response = registered.post("/api/register", json=CREDENTIALS)
    assert response.status_code == 409


def test_register_validates_credential_lengths(client):
    short_name = client.post(
        "/api/register", json={"username": "abc", "password": "secret-pass"}
    )
    short_pass = client.post(
        "/api/register", json={"username": "alice123", "password": "abc"}
    )
    assert short_name.status_code == 422
    assert short_pass.status_code == 422


# ---------------------------------------------------------------------------
# /api/login
# ---------------------------------------------------------------------------

def test_login_returns_usable_token(registered):
    response = registered.post("/api/login", json=CREDENTIALS)
    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "alice123"

    me = registered.get("/api/me", headers=auth_header(body["token"]))
    assert me.status_code == 200
    assert me.json()["username"] == "alice123"


def test_login_wrong_password_rejected(registered):
    response = registered.post(
        "/api/login", json={"username": "alice123", "password": "wrong-pass"}
    )
    assert response.status_code == 401


def test_login_unknown_user_rejected(client):
    response = client.post("/api/login", json=CREDENTIALS)
    assert response.status_code == 401


def test_login_normalizes_username(registered):
    response = registered.post(
        "/api/login", json={"username": "  ALICE123 ", "password": "secret-pass"}
    )
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# /api/me
# ---------------------------------------------------------------------------

def test_me_requires_auth(client):
    assert client.get("/api/me").status_code == 401


def test_me_rejects_invalid_token(client):
    response = client.get("/api/me", headers=auth_header("bogus-token"))
    assert response.status_code == 401


def test_me_rejects_non_bearer_scheme(token, registered):
    response = registered.get("/api/me", headers={"Authorization": f"Basic {token}"})
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# /api/logout
# ---------------------------------------------------------------------------

def test_logout_invalidates_token(token, registered):
    response = registered.post("/api/logout", headers=auth_header(token))
    assert response.status_code == 200
    assert registered.get("/api/me", headers=auth_header(token)).status_code == 401


def test_logout_requires_auth(client):
    assert client.post("/api/logout").status_code == 401


# ---------------------------------------------------------------------------
# /api/grade
# ---------------------------------------------------------------------------

def test_grade_requires_auth(client):
    response = client.post("/api/grade", json={"game": ["slate", "crane"]})
    assert response.status_code == 401


def test_grade_returns_grade(token, registered):
    response = registered.post(
        "/api/grade",
        json={"game": ["slate", "crane"]},
        headers=auth_header(token),
    )
    assert response.status_code == 200
    assert response.json() == {"grade": "A"}


def test_grade_persists_game_for_user(token, registered):
    registered.post(
        "/api/grade",
        json={"game": ["SLATE", "CRANE"], "status": "victory"},
        headers=auth_header(token),
    )
    games = db.get_user_games_by_username("alice123")
    assert len(games) == 1
    assert games[0]["target_word"] == "crane"
    assert games[0]["grade"] == "A"
    # Guesses are lowercased before being stored
    guesses = db.get_game_guesses(games[0]["game_id"])
    assert [g["guess"] for g in guesses] == ["slate", "crane"]


# ---------------------------------------------------------------------------
# /api/pattern
# ---------------------------------------------------------------------------

def test_pattern_greens_and_blacks(client):
    response = client.get("/api/pattern", params={"guess": "slate"})
    assert response.status_code == 200
    assert response.json() == {
        "pattern": {"0": "black", "1": "black", "2": "green", "3": "black", "4": "green"}
    }


def test_pattern_yellows(client):
    response = client.get("/api/pattern", params={"guess": "enact"})
    assert response.json() == {
        "pattern": {"0": "yellow", "1": "yellow", "2": "green", "3": "yellow", "4": "black"}
    }


def test_pattern_is_case_insensitive(client):
    upper = client.get("/api/pattern", params={"guess": "SLATE"}).json()
    lower = client.get("/api/pattern", params={"guess": "slate"}).json()
    assert upper == lower


# ---------------------------------------------------------------------------
# /api/profile
# ---------------------------------------------------------------------------

def play_game(client, token, won):
    """Plays one game; the last guess decides victory ('crane') or defeat"""
    guesses = ["slate", "crane"] if won else ["slate", "audio"]
    status = "victory" if won else "defeat"
    response = client.post(
        "/api/grade",
        json={"game": guesses, "status": status},
        headers=auth_header(token),
    )
    assert response.status_code == 200


def test_profile_requires_auth(client):
    assert client.get("/api/profile").status_code == 401


def test_profile_new_user_has_empty_stats(token, registered):
    response = registered.get("/api/profile", headers=auth_header(token))
    assert response.status_code == 200
    body = response.json()
    assert body["games_played"] == 0
    assert body["win_rate"] == 0.0
    assert body["current_streak"] == 0
    assert body["best_streak"] == 0
    assert body["last_five_games"] == []
    assert all(count == 0 for count in body["grade_dist"].values())


def test_profile_aggregates_games(token, registered):
    play_game(registered, token, won=True)
    play_game(registered, token, won=True)
    play_game(registered, token, won=False)

    body = registered.get("/api/profile", headers=auth_header(token)).json()
    assert body["games_played"] == 3
    # win_rate is an integer percentage, truncated
    assert body["win_rate"] == 66
    # score_game is stubbed to always grade "A"
    assert body["grade_dist"]["A"] == 3
    # The defeat reset the streak of two wins
    assert body["current_streak"] == 0
    assert body["best_streak"] == 2


def test_profile_win_updates_streaks(token, registered):
    play_game(registered, token, won=True)
    body = registered.get("/api/profile", headers=auth_header(token)).json()
    assert body["current_streak"] == 1
    assert body["best_streak"] == 1


def test_profile_limits_recent_games_to_five(token, registered):
    for _ in range(6):
        play_game(registered, token, won=True)

    body = registered.get("/api/profile", headers=auth_header(token)).json()
    recent = body["last_five_games"]
    assert len(recent) == 5

    all_games = db.get_user_games_by_username("alice123")
    assert len(all_games) == 6
    # The five most recent games, newest first; the oldest game is dropped
    ordered = main.utils.most_recent_k_games(all_games, verbose=True)
    ordered_ids = [g["game_id"] for g in ordered]
    oldest_id = min(g["game_id"] for g in all_games)
    assert oldest_id not in ordered_ids
    assert ordered_ids == sorted(ordered_ids, reverse=True)


def test_profile_recent_games_expose_expected_fields(token, registered):
    play_game(registered, token, won=True)
    play_game(registered, token, won=False)
    body = registered.get("/api/profile", headers=auth_header(token)).json()
    newest, older = body["last_five_games"][:2]
    # Defeats hide the guess count behind an 'X'
    assert newest["total_guesses"] == "X"
    assert older["total_guesses"] == 2
    assert newest["grade"] == "A"
