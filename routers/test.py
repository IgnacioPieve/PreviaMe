from fastapi import APIRouter, Depends, status
from dependencies import auth

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
