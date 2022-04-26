import datetime

import config
import firebase_admin
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials

from database import db

cred = credentials.Certificate(config.credentials["firebase"])
firebase_admin.initialize_app(cred)


async def authenticate(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
):
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
        )

    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
        )

    user = await db["user"].find_one({"user_id": decoded_token["user_id"]})
    if not user:
        user = {
            "user_id": decoded_token["user_id"],
            "email": decoded_token["email"],
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "friends": [],
            "friend_requests_sent": [],
            "friend_requests_received": [],
        }
        await db["user"].insert_one(user)
    return decoded_token
