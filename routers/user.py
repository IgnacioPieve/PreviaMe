import datetime
from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from dependencies import auth
from schemas.user import UserRequestModel, UserModel
from database import db

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.post('/', response_model=UserModel, status_code=201)
def create_user(new_user: UserRequestModel, user=Depends(auth.authenticate)):
    user_data = jsonable_encoder(new_user)
    user_data['created_at'] = datetime.datetime.now()
    user_data['updated_at'] = datetime.datetime.now()
    user_data['user_id'] = user["user_id"]
    user_data['email'] = user["email"]

    db["user"].insert_one(user_data)
    return user_data


@router.put('/', response_model=UserModel, status_code=200)
def update_user(user_data: UserRequestModel, user=Depends(auth.authenticate)):
    user_data = jsonable_encoder(user_data)
    user_data['updated_at'] = datetime.datetime.now()
    user_data['user_id'] = user["user_id"]
    user_data['email'] = user["email"]

    db["user"].update_one(
        {'user_id': user["user_id"]},
        {'$set': user_data}
    )
    return user_data


@router.get('/', response_model=UserModel, status_code=200)
def get_user(user=Depends(auth.authenticate)):
    user_data = db["user"].find_one({'user_id': user["user_id"]})
    return user_data
