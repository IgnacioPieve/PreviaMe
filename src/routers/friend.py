from fastapi import APIRouter, Depends, HTTPException
from dependencies import auth
from database import db
from schemas.utils import StatusMessage

router = APIRouter(prefix="/friend", tags=["Friends"])


@router.post("/{user_id}", summary="Add user as friend", response_model=StatusMessage)
async def add_friend(




        user_id: str, user=Depends(auth.authenticate)




):
    """
    Envía una solicitud de amistad a un usuario o se agrega como amigo si ya se ha recibido la solicitud.
    Si ya se ha recibido una solicitud, se agrega como amigo.
    Si la otra parte no ha enviado una solicitud de amistad, se le enviará una solicitud de amistad.

    - **user_id**: id del usuario que se desea agregar como amigo.
    """
    self_user = await db["user"].find_one({"user_id": user["user_id"]})
    target_user = await db["user"].find_one({"user_id": user_id})

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    if self_user["user_id"] == target_user["user_id"]:
        raise HTTPException(status_code=400, detail="You can't add yourself")
    if user["user_id"] in target_user["friend_requests_received"]:
        raise HTTPException(status_code=409, detail="Friend request already sent")
    if user["user_id"] in target_user["friends"]:
        raise HTTPException(status_code=409, detail="Already friends")

    if target_user["user_id"] in self_user["friend_requests_received"]:
        self_user["friends"].append(target_user["user_id"])
        target_user["friends"].append(self_user["user_id"])
        self_user["friend_requests_received"].remove(target_user["user_id"])
        target_user["friend_requests_sent"].remove(self_user["user_id"])

        await db["user"].update_one(
            {"user_id": self_user["user_id"]}, {"$set": self_user}
        )
        await db["user"].update_one(
            {"user_id": target_user["user_id"]}, {"$set": target_user}
        )

        return {"status": "ok", "message": "Friend request accepted"}

    else:
        target_user["friend_requests_received"].append(self_user["user_id"])
        self_user["friend_requests_sent"].append(target_user["user_id"])

        await db["user"].update_one({"user_id": user_id}, {"$set": target_user})
        await db["user"].update_one({"user_id": user["user_id"]}, {"$set": self_user})

        return {"status": "ok", "message": "Friend request sent"}
