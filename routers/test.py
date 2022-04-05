from config import firestore_key
import requests
from fastapi import APIRouter, Depends, status
from dependencies import auth
from schemas.test import UserRequestModel

router = APIRouter(
    prefix="/test",
    tags=['Test']
)


@router.post('/auth')
def test_auth(user=Depends(auth.authenticate)):
    return {"status": "ok", "email": user['email']}


@router.get("/status")
def get_status():
    """Get status of messaging server."""
    return {"status": "running"}


@router.post("/login")
def login(user: UserRequestModel):

    user = {
        **user.dict(),
        "returnSecureToken": True
    }
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={firestore_key}"
    response = requests.post(url, json=user)
    return {"status": "ok", "token": response.json()['idToken']}

# Endpoint to register user
@router.post("/register")
def register(user: UserRequestModel):

    user = {
        **user.dict(),
        "returnSecureToken": True
    }
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={firestore_key}"
    response = requests.post(url, json=user)
    return {"status": "ok", "token": response.json()['idToken']}
