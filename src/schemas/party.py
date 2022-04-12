import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from schemas.utils import PyObjectId
from schemas.user import SimpleUserModel


class GeoPoint(TypedDict):
    lat: float
    lng: float


class PartyRequestModel(BaseModel):
    geopoint: GeoPoint
    music: int
    price: float
    name: str
    alcohol: bool
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "geopoint": {
                    "lat": -31.442626,
                    "lng": -64.192783
                },
                "name": "UPD La Salle 2022",
                "music": 5,
                "price": 750,
                "alcohol": False,
                "description": "UPD Promo 22"
            }
        }


class PartyModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    geopoint: GeoPoint
    created: datetime.datetime
    user_id: str
    music: int
    name: str
    price: float
    alcohol: bool
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "624c7d0eab0ac6f86b69c33e",
                "geopoint": {
                    "lat": -31.442626,
                    "lng": -64.192783
                },
                "created": "2020-04-01T00:00:00",
                "name": "UPD La Salle 2022",
                "music": 5,
                "price": 750,
                "alcohol": False,
                "description": "UPD Promo 22"
            }
        }


class PartyOwnerModel(PartyModel):
    members: list[SimpleUserModel]

    class Config:
        schema_extra = {
            "example": {
                "id": "624c7d0eab0ac6f86b69c33e",
                "geopoint": {
                    "lat": -31.442626,
                    "lng": -64.192783
                },
                "created": "2020-04-01T00:00:00",
                "name": "UPD La Salle 2022",
                "music": 5,
                "price": 750,
                "alcohol": False,
                "description": "UPD Promo 22"
            }
        }
