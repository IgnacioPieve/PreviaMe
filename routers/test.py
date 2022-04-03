from fastapi import APIRouter, Depends, status
from dependencies import auth

router = APIRouter(
    prefix="/test",
    tags=['Test']
)


@router.post('/auth')
def create_user(user=Depends(auth.authenticate)):
    print(user)
    return {"status": "ok", "email": user['email']}

