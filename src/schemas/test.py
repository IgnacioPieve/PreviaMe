from pydantic import BaseModel, EmailStr


class UserRequestModel(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "test@test.com",
                "password": "password",
            }
        }
