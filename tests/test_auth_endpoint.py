from src.app import app
from fastapi.testclient import TestClient
from datetime import datetime
import pytest

TOKEN = ""


@pytest.fixture
def client():
    client = TestClient(app)
    return client


def test_login(client):
    global TOKEN
    user = {
        'username': 'Kamil',
        'password': 'Dupa8'
    }
    resp = client.post(f"auth/login", json=user)
    assert resp.status_code == 200
    print(resp.json())
    temp = resp.json()
    TOKEN = temp['token']
    # expected = {"token": True}
    # assert resp.json() == expected


def test_invalid_login(client):
    user = {
        'username': 'Kamil',
        'password': 'Dupa7'
    }
    resp = client.post(f"auth/login", json=user)
    assert resp.status_code == 401
    expected = {'detail': 'Invalid username and/or password'}
    assert resp.json() == expected


def test_get_datetime_auth(client):
    resp = client.get(f"auth/protected", headers={"Authorization": f"Bearer {TOKEN}"})
    assert resp.status_code == 200
    expected = {'Current time': datetime.now().replace(microsecond=0).isoformat()}
    assert resp.json() == expected


def test_get_datetime_without_auth(client):
    invalid_token = TOKEN
    invalid_token = invalid_token.replace('a', 'x')
    resp = client.get(f"auth/protected", headers={"Authorization": f"Bearer {invalid_token}"})
    assert resp.status_code == 401
