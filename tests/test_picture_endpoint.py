from src.app import app
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def client():
    client = TestClient(app)
    return client


def test_check_photo_upload(client):
    fpath = "tests/test_photos/Lenna.jpg"
    with open(fpath, "rb") as f:
        response = client.post(
            "/picture/invert", files={"image": ("filename", f, "image/jpeg")})
    assert response.status_code == 200
