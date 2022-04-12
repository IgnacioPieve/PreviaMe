import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class SimpleUserModel(BaseModel):
    user_id: str
    name: str
    picture: Optional[str]
    bio: Optional[str]


class UserRequestModel(BaseModel):
    name: str
    picture: Optional[str]
    bio: Optional[str]


class UserUpdateModel(BaseModel):
    name: Optional[str]
    picture: Optional[str]
    bio: Optional[str]


class UserModel(BaseModel):
    user_id: str
    email: EmailStr
    picture: Optional[str]
    name: str
    bio: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
