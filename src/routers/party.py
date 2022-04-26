import datetime
import math
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from database import db
from dependencies import auth
from schemas.party import PartyModel, PartyRequestModel

router = APIRouter(prefix="/party", tags=["Party"])


@router.get("/", response_model=List[PartyModel])
async def get_parties(
    top_lat: float, top_lng: float, bottom_lat: float, bottom_lng: float
):
    """
    Obtiene todas las fiestas que se encuentran dentro de un rectángulo (top_coords, bottom_coords): Area de búsqueda

    Las fiestas tienen que estar dentro del area de busqueda y estar dentro de un rango de 10 horas.
    TODO: Rango de tiempo
    """

    x = (top_lat + bottom_lat) / 2
    y = (top_lng + bottom_lng) / 2
    distance = math.sqrt((top_lat - bottom_lat) ** 2 + (top_lng - bottom_lng) ** 2) / 2

    parties = (
        await db["party"]
        .find({"geopoint": {"$near": [x, y], "$maxDistance": distance}})
        .to_list(1000)
    )

    return parties


@router.get("/{party_id}", response_model=PartyModel, summary="Get a party data")
async def get_party(party_id: str):
    """
    Obtiene los datos de una fiesta
    """

    if not ObjectId.is_valid(party_id):
        raise HTTPException(status_code=400, detail="Party Id not valid (check length)")
    party = await db["party"].find_one({"_id": ObjectId(party_id)})
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party


@router.post("/", response_model=PartyModel, summary="Create a new party")
async def create_party(party: PartyRequestModel, user=Depends(auth.authenticate)):
    """
    Envía una solicitud de unirse a una fiesta:

    - **geopoint**: json de coordenadas {lat, lon}
    - **music**: integer que representa la música que se va a tocar
    - **price**: float que representa el precio de la fiesta
    - **alcohol**: boolean que representa si la fiesta tiene alcohol
    - **description**: string que representa la descripción de la fiesta
    """

    party = jsonable_encoder(party)
    party = {
        **party,
        "user_id": user["user_id"],
        "created": int(datetime.datetime.now().timestamp()),
        "members": [],
        "pending": [],
    }
    new_party = await db["party"].insert_one(party)
    created_party = await db["party"].find_one({"_id": new_party.inserted_id})
    return created_party


@router.post("/{party_id}/join", summary="Request to join a party")
async def join_party(party_id: str, user=Depends(auth.authenticate)):
    """
    Envía una solicitud de unirse a una fiesta:

    - **party_id**: id de la fiesta a la que se desea asistir
    """
    if not ObjectId.is_valid(party_id):
        raise HTTPException(status_code=400, detail="Party Id not valid (check length)")
    party = await db["party"].find_one({"_id": ObjectId(party_id)})
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if party["user_id"] == user["user_id"]:
        raise HTTPException(status_code=401, detail="You're the party owner!")

    if user["user_id"] in party["pending"]:
        raise HTTPException(
            status_code=400, detail="You're already on the pending list!"
        )

    if user["user_id"] in party["members"]:
        raise HTTPException(
            status_code=400, detail="You're already on the members list!"
        )

    party["pending"].append(user["user_id"])

    await db["party"].update_one({"_id": ObjectId(party_id)}, {"$set": party})

    return {"status": "ok"}


@router.post("/{party_id}/{user_id}", summary="Accept a request to join a party")
async def accept_member(party_id: str, user_id: str, user=Depends(auth.authenticate)):
    """
    Acepta a un miembro de la lista de pendientes:

    - **party_id**: id de la fiesta a la que pertenece el usuario
    - **user_id**: id del usuario que se quiere aceptar
    """

    if not ObjectId.is_valid(party_id):
        raise HTTPException(status_code=400, detail="Party Id not valid (check length)")
    party = await db["party"].find_one({"_id": ObjectId(party_id)})
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if party["user_id"] != user["user_id"]:
        raise HTTPException(status_code=401, detail="You're not the party owner!")

    if user_id not in party["pending"]:
        raise HTTPException(
            status_code=409, detail=f"User ({user_id}) is not on the pending list!"
        )

    party["pending"].remove(user_id)
    party["members"].append(user_id)

    await db["party"].update_one({"_id": ObjectId(party_id)}, {"$set": party})

    return {"status": "ok"}
