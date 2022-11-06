from src.app import app
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def client():
    client = TestClient(app)
    return client


def test_check_prime(client):
    numbers = {
        4: False,
        7: True,
        85: False,
        938: False,
        3109: True
    }
    for n in numbers:
        resp = client.get(f"/prime/{n}")
        assert resp.status_code == 200
        expected = {"Is number prime": numbers.get(n)}
        assert resp.json() == expected


def test_check_max_prime(client):
    number = 2147483647
    resp = client.get(f"prime/{number}")
    assert resp.status_code == 200
    expected = {"Is number prime": True}
    assert resp.json() == expected


def test_check_non_valid(client):
    number = -43
    resp = client.get(f"prime/{number}")
    assert resp.status_code == 200
    expected = {"Error handler": "Not valid input number"}
    assert resp.json() == expected


def test_check_not_found_endpoint(client):
    resp = client.get(f"primee")
    assert resp.status_code == 404
