from datetime import datetime
from pydantic import BaseModel, Field


class TravelPrice(BaseModel):
    price: float = Field(gt=0, le=10_000, examples=[125.15])


class NewTravel(TravelPrice):
    title: str
    description: str
    place: str


class SavedTravel(NewTravel):
    id: int
    created_at: datetime


class DeletedTravel(BaseModel):
    id: int
    deleted: bool = True
