import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing_extensions import TypedDict
from schemas.utils import PyObjectId


class GeoPoint(TypedDict):
    lat: float
    long: float


class PartyRequestModel(BaseModel):
    geopoint: GeoPoint

    class Config:
        schema_extra = {
            "geopoint": {
                "lat": 0,
                "long": 0
            }
        }


class PartyModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    geopoint: GeoPoint
    created: datetime.date
    user_id: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
