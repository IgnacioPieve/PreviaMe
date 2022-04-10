from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from firebase_admin import auth, credentials
import firebase_admin
import config

cred = credentials.Certificate(config.credentials["firebase"])
firebase_admin.initialize_app(cred)


def authenticate(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required"
        )

    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}"
        )

    return decoded_token
