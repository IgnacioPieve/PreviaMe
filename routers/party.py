from fastapi import APIRouter, Depends, status
from dependencies import auth

router = APIRouter(
    prefix="/party",
    tags=['Party']
)

