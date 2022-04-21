import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from schemas.utils import PyObjectId
from schemas.user import SimpleUserModel



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
                "date": "2022-04-20T15:20:20.349Z"
            }
        }


class PartyModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    geopoint: list[float]
    created: datetime.datetime
    user_id: str
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
        schema_extra = {
            "example": {
                "id": "624c7d0eab0ac6f86b69c33e",
                "geopoint": [-31.442626, -64.192783],
                "created": "2020-04-01T00:00:00",
                "name": "UPD La Salle 2022",
                "music": ["Cachengue"],
                "price": 750,
                "alcohol": False,
                "description": "UPD Promo 22",
                "date": "2022-04-20T15:20:20.349Z"
            }
        }


class PartyOwnerModel(PartyModel):
    members: list[SimpleUserModel]

    class Config:
        schema_extra = {
            "example": {
                "id": "624c7d0eab0ac6f86b69c33e",
                "geopoint": [-31.442626, -64.192783],
                "created": "2020-04-01T00:00:00",
                "name": "UPD La Salle 2022",
                "music": ["Trap"],
                "price": 750,
                "alcohol": False,
                "description": "UPD Promo 22",
                "date": "2022-04-20T15:20:20.349Z"
            }
        }
