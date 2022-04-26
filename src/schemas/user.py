from typing import Optional

import datetime


from pydantic import BaseModel, EmailStr


class SimpleUserModel(BaseModel):
    user_id: str
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
    name: Optional[str]
    bio: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        schema_extra = {
            "example": {
                "user_id": "7TKUuX29JFhbT6t9mnVARy70tXS2",
                "email": "test@test.com",
                "picture": "google.com.ar",
                "name": "Ignacio Pieve Roiger",
                "bio": "Hola! Me llamo Ignacio",
                "created_at": "2022-04-12T03:31:19.122000",
                "updated_at": "2022-04-12T03:31:19.122000",
            }
        }
