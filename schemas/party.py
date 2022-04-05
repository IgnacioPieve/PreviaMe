import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing_extensions import TypedDict
from schemas.utils import PyObjectId


class GeoPoint(TypedDict):
    lat: float
    lng: float


class PartyRequestModel(BaseModel):
    geopoint: GeoPoint
    music: int
    price: float
    alcohol: bool
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "geopoint": {
                    "lat": -31.442626,
                    "lng": -64.192783
                },
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
    price: float
    alcohol: bool
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
