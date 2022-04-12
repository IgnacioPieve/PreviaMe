import datetime
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from dependencies import auth
from schemas.party import PartyRequestModel, PartyModel
from database import db

router = APIRouter(
    prefix="/party",
    tags=['Party']
)


class Party:
    def __init__(self, party):
        self.party = party


@router.post('/', response_model=PartyModel)
async def create_party(party: PartyRequestModel, user=Depends(auth.authenticate)):
    party = jsonable_encoder(party)
    party = {
        **party,
        'user_id': user['user_id'],
        'created': int(datetime.datetime.now().timestamp()),
        'members': [],
        'pending': []
    }
    new_party = await db["parties"].insert_one(party)
    created_party = await db["parties"].find_one({"_id": new_party.inserted_id})
    return created_party


@router.get("/", response_model=List[PartyModel])
async def get_parties():
    parties = await db["parties"].find().to_list(1000)
    return parties


@router.get("/{party_id}", response_model=PartyModel)
async def get_party(party_id: str):
    if not ObjectId.is_valid(party_id):
        raise HTTPException(status_code=400, detail="Party Id not valid (check length)")
    party = await db["parties"].find_one({"_id": ObjectId(party_id)})
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party


@router.post("/{party_id}/join")
async def join_party(party_id: str, user=Depends(auth.authenticate)):
    if not ObjectId.is_valid(party_id):
        raise HTTPException(status_code=400, detail="Party Id not valid (check length)")
    party = await db["parties"].find_one({"_id": ObjectId(party_id)})
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if party['user_id'] == user['user_id']:
        raise HTTPException(status_code=401, detail="You're the party owner!")

    if user['user_id'] in party['pending']:
        raise HTTPException(status_code=400, detail="You're already on the pending list!")

    if user['user_id'] in party['members']:
        raise HTTPException(status_code=400, detail="You're already on the members list!")

    party['pending'].append(user['user_id'])

    await db["parties"].update_one({"_id": ObjectId(party_id)}, {"$set": party})

    return {'status': 'ok'}


@router.post("/{party_id}/{user_id}")
async def accept_member(party_id: str, user_id: str, user=Depends(auth.authenticate)):
    if not ObjectId.is_valid(party_id):
        raise HTTPException(status_code=400, detail="Party Id not valid (check length)")
    party = await db["parties"].find_one({"_id": ObjectId(party_id)})
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if party['user_id'] != user['user_id']:
        raise HTTPException(status_code=401, detail="You're not the party owner!")

    if user_id not in party['pending']:
        raise HTTPException(status_code=400, detail=f"User ({user_id}) is not on the pending list!")

    party['pending'].remove(user_id)
    party['members'].append(user_id)

    await db["parties"].update_one({"_id": ObjectId(party_id)}, {"$set": party})

    return {'status': 'ok'}
