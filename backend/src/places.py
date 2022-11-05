from typing import Literal, Optional

from pydantic import BaseModel

from src.commons import Bounds, LatLngLiteral


class AddressComponent(BaseModel):
    long_name: str
    short_name: str
    types: list[str]


class PlaceOpeningHoursPeriodDetail(BaseModel):
    day: int
    time: str
    date: Optional[str]
    truncated: Optional[bool]


class PlaceOpeningHoursPeriod(BaseModel):
    open: PlaceOpeningHoursPeriodDetail
    close: PlaceOpeningHoursPeriodDetail


class PlaceSpecialDay(BaseModel):
    date: Optional[str]  # RFC3339
    exceptional_hours: Optional[bool]


class PlaceOpeningHours(BaseModel):
    open_now: Optional[bool]
    periods: Optional[list[PlaceOpeningHoursPeriod]]
    special_days: Optional[list[PlaceSpecialDay]]
    type: Optional[str]
    weekday_text: Optional[list[str]]


class PlaceEditorialSummary(BaseModel):
    language: Optional[str]
    overview: Optional[str]


class Geometry(BaseModel):
    location: LatLngLiteral
    viewport: Bounds


class PlacePhoto(BaseModel):
    height: int
    html_attributions: list[str]
    photo_reference: str
    width: int


class PlusCode(BaseModel):
    global_code: str
    compound_code: Optional[str]


class PlaceReview(BaseModel):
    author_name: str
    rating: int
    relative_time_description: str
    time: int
    author_url: Optional[str]
    language: Optional[str]
    original_language: Optional[str]
    profile_photo_url: Optional[str]
    text: Optional[str]
    translated: Optional[bool]


class Place(BaseModel):
    address_components: Optional[list[AddressComponent]]
    adr_address: Optional[str]
    business_status: Optional[str]
    curbside_pickup: Optional[bool]
    current_opening_hours: Optional[PlaceOpeningHours]
    delivery: Optional[bool]
    dine_in: Optional[bool]
    editorial_summary: Optional[PlaceEditorialSummary]
    formatted_address: Optional[str]
    formatted_phone_number: Optional[str]
    geometry: Optional[Geometry]
    icon: Optional[str]
    icon_background_color: Optional[str]
    icon_mask_base_uri: Optional[str]
    international_phone_number: Optional[str]
    name: Optional[str]
    opening_hours: Optional[PlaceOpeningHours]
    photos: Optional[list[PlacePhoto]]
    place_id: Optional[str]
    plus_code: Optional[PlusCode]
    price_level: Optional[
        int
    ]  # 0: Free, 1: Inexpensive, 2: Moderate, 3: Expensive, 4: Very Expensive
    rating: Optional[float]
    reviews: Optional[list[PlaceReview]]
    secondary_opening_hours: Optional[PlaceOpeningHours]
    takeout: Optional[bool]
    types: Optional[list[str]]
    url: Optional[str]
    user_ratings_total: Optional[int]
    utc_offset: Optional[int]
    vicinity: Optional[str]
    website: Optional[str]


class PlacesResult(BaseModel):
    html_attributions: list
    results: list[Place]


class PlacesRequest(BaseModel):
    query: str
    language: Optional[
        Literal["ja", "en", "es", "fr", "de", "it", "pt", "ru", "zh-CN", "zh-TW"]
    ] = "ja"
