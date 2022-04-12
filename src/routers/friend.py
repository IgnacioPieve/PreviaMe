from fastapi import APIRouter, Depends, HTTPException
from dependencies import auth
from database import db

router = APIRouter(
    prefix="/friend",
    tags=['Friends']
)


@router.post('/{user_id}')
async def add_friend(user_id: str, user=Depends(auth.authenticate)):
    self_user = await db["user"].find_one({"user_id": user['user_id']})
    target_user = await db["user"].find_one({"user_id": user_id})

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    if self_user["user_id"] == target_user["user_id"]:
        raise HTTPException(status_code=400, detail="You can't add yourself")
    if user['user_id'] in target_user['friend_requests_received']:
        raise HTTPException(status_code=409, detail="Friend request already sent")
    if user['user_id'] in target_user['friends']:
        raise HTTPException(status_code=409, detail="Already friends")


    if target_user['user_id'] in self_user['friend_requests_received']:
        self_user['friends'].append(target_user['user_id'])
        target_user['friends'].append(self_user['user_id'])
        self_user['friend_requests_received'].remove(target_user['user_id'])
        target_user['friend_requests_sent'].remove(self_user['user_id'])

        await db["user"].update_one({"user_id": self_user['user_id']}, {"$set": self_user})
        await db["user"].update_one({"user_id": target_user['user_id']}, {"$set": target_user})

        return {"status": "ok", "message": "Friend request accepted"}

    else:
        target_user['friend_requests_received'].append(self_user['user_id'])
        self_user['friend_requests_sent'].append(target_user['user_id'])

        await db["user"].update_one({"user_id": user_id}, {"$set": target_user})
        await db["user"].update_one({"user_id": user['user_id']}, {"$set": self_user})

        return {"status": "ok", "message": "Friend request sent"}



