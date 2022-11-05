from pydantic import BaseModel


class LatLngLiteral(BaseModel):
    lat: float
    lng: float


class Bounds(BaseModel):
    northeast: LatLngLiteral
    southwest: LatLngLiteral


class TextValueObject(BaseModel):
    text: str
    value: int
