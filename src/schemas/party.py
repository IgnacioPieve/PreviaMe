import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from schemas.user import SimpleUserModel
from schemas.utils import PyObjectId


class PartyRequestModel(BaseModel):
    geopoint: list[float]
    music: list[str]
    price: float
    name: str
    alcohol: bool
    date: datetime.datetime
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "geopoint": [-31.442626, -64.192783],
                "name": "UPD La Salle 2022",
                "music": ["Rock", "Pop"],
                "price": 750,
                "alcohol": False,
                "description": "UPD Promo 22",
                "date": "2022-04-20T15:20:20.349Z",
            }
        }


class PartyModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    geopoint: list[float]
    created: datetime.datetime
    music: list[str]
    name: str
    price: float
    alcohol: bool
    date: datetime.datetime
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class PartyOwnerModel(PartyModel):
    members: list[SimpleUserModel]
