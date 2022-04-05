import datetime
from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from dependencies import auth
from schemas.party import PartyRequestModel, PartyModel
from database import db

router = APIRouter(
    prefix="/party",
    tags=['Party']
)


@router.post('/', response_description="Add a new party", response_model=PartyModel)
async def add_party(party: PartyRequestModel, user=Depends(auth.authenticate)):
    party = jsonable_encoder(party)
    party = {
        **party,
        'user_id': user['user_id'],
        'created': int(datetime.datetime.now().timestamp())
    }
    new_party = await db["parties"].insert_one(party)
    created_party = await db["parties"].find_one({"_id": new_party.inserted_id})
    return created_party


@router.get("/", response_description="List all parties", response_model=List[PartyModel])
async def list_parties():
    parties = await db["parties"].find().to_list(1000)
    return parties

# TODO: Añadir para retornar una sola party
