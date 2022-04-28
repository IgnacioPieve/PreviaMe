import datetime

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from database import Database
from dependencies import auth
from schemas.user import UserModel, UserUpdateModel

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=UserModel, status_code=200, summary="Get user data")
async def get_user(user=Depends(auth.authenticate), db=Depends(Database.get_db)):
    """
    Obtener la información de un usuario
    """
    return await db["user"].find_one({"user_id": user["user_id"]})


@router.post("/", response_model=UserModel, status_code=201, summary="Update user data")
async def create_user(
    user_data: UserUpdateModel,
    user=Depends(auth.authenticate),
    db=Depends(Database.get_db),
):
    """
    Actualiza los datos de un usuario (sobreecribiendo el objeto completo):

    - **picture**: Link a la imagen del usuario
    - **name**: Nombre del usuario
    - **bio**: Biografía del usuario
    """

    user_data = jsonable_encoder(user_data)
    new_user = {
        "user_id": user["user_id"],
        "email": user["email"],
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "friends": [],
        "friend_requests_sent": [],
        "friend_requests_received": [],
    }

    for data in user_data:
        if user_data[data] is not None:
            new_user[data] = user_data[data]

    await db["user"].update_one({"user_id": user["user_id"]}, {"$set": new_user})
    return new_user


@router.patch(
    "/", response_model=UserModel, status_code=200, summary="Update user data"
)
async def update_user(
    user_data: UserUpdateModel,
    user=Depends(auth.authenticate),
    db=Depends(Database.get_db),
):
    """
    Actualiza los datos de un usuario (sin sobreescribirlos):

    - **picture**: Link a la imagen del usuario
    - **name**: Nombre del usuario
    - **bio**: Biografía del usuario
    """

    new_user = await db["user"].find_one({"user_id": user["user_id"]}, {"_id": 0})

    new_user_data = jsonable_encoder(user_data)

    for data in new_user_data:
        if new_user_data[data] is not None:
            new_user[data] = new_user_data[data]

    new_user["updated_at"] = datetime.datetime.now()

    await db["user"].update_one({"user_id": user["user_id"]}, {"$set": new_user})
    return new_user
