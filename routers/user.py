import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from dependencies import auth
from schemas.user import UserRequestModel, UserModel, UserUpdateModel
from database import db

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.post('/', response_model=UserModel, status_code=201)
async def create_user(new_user: UserRequestModel, user=Depends(auth.authenticate)):
    user_data = await db["user"].find_one({'user_id': user["user_id"]})
    if user_data is not None:
        raise HTTPException(status_code=400, detail="User already exists. If you want to update your profile, use PUT")

    user_data = jsonable_encoder(new_user)
    user_data['created_at'] = datetime.datetime.now()
    user_data['updated_at'] = datetime.datetime.now()
    user_data['user_id'] = user["user_id"]
    user_data['email'] = user["email"]

    await db["user"].insert_one(user_data)
    return user_data


@router.put('/', response_model=UserModel, status_code=200)
async def update_user(user_data: UserUpdateModel, user=Depends(auth.authenticate)):
    old_user = await db["user"].find_one({'user_id': user["user_id"]}, {"_id": 0})
    if old_user is None:
        raise HTTPException(status_code=404, detail="Onboarding not completed")
    new_user = old_user

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
    user_data = await db["user"].find_one({'user_id': user["user_id"]})
    if user_data is not None:
        return user_data
    raise HTTPException(status_code=404, detail="Onboarding not completed")
