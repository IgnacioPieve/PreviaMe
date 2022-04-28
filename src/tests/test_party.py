import asyncio

from starlette.testclient import TestClient

from app import app
from dependencies import auth

examples = {
    "party": {
        "geopoint": [-31.442626, -64.192783],
        "name": "UPD La Salle 2022",
        "music": ["Rock", "Pop"],
        "price": 750,
        "alcohol": False,
        "description": "UPD Promo 22",
        "date": "2022-04-20T15:20:20.349Z",
    },
    "user": {
        "user_id": "test_id",
        "email": "example@test.com",
        "email_verified": False,
        "firebase": {
            "identities": {"email": ["test@test.com"]},
            "sign_in_provider": "password",
        },
        "uid": "test_id",
    },
}


def override_auth():
    return examples["user"]


app.dependency_overrides[auth.authenticate] = override_auth


def test_create_party():
    with TestClient(app) as client:
        params = {"top_lng": 40, "top_lat": 40, "bottom_lng": 0, "bottom_lat": 0}
        response = client.get("/party/", params=params)
        assert response.status_code == 200
        # assert response.json()['name'] == examples['party']['name']
