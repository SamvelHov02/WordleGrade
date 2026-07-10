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
        json={"game": ["SLATE", "CRANE"]},
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
