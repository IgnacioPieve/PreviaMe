import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from dependencies import auth
from schemas.user import UserModel, UserUpdateModel
from database import db

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.post('/', response_model=UserModel, status_code=201)
async def create_user(user_data: UserUpdateModel, user=Depends(auth.authenticate)):
    user_data = jsonable_encoder(user_data)
    new_user = {
        'user_id': user["user_id"],
        'email': user["email"],
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now(),
        'friends': [],
        'friend_requests_sent': [],
        'friend_requests_received': [],
    }

    for data in user_data:
        if user_data[data] is not None:
            new_user[data] = user_data[data]

    await db["user"].update_one(
        {'user_id': user["user_id"]},
        {'$set': new_user}
    )
    return new_user


@router.put('/', response_model=UserModel, status_code=200)
async def update_user(user_data: UserUpdateModel, user=Depends(auth.authenticate)):
    new_user = await db["user"].find_one({'user_id': user["user_id"]}, {"_id": 0})

    new_user_data = jsonable_encoder(user_data)

    for data in new_user_data:
        if new_user_data[data] is not None:
            new_user[data] = new_user_data[data]

    new_user['updated_at'] = datetime.datetime.now()

    await db["user"].update_one(
        {'user_id': user["user_id"]},
        {'$set': new_user}
    )
    return new_user


@router.get('/', response_model=UserModel, status_code=200)
async def get_user(user=Depends(auth.authenticate)):
    return await db["user"].find_one({'user_id': user["user_id"]})
