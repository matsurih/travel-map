from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel

from src.commons import Bounds, LatLngLiteral, TextValueObject


class DirectionsPolyline(BaseModel):
    """
    Polyline encoding is a lossy compression algorithm that allows you to store a series of coordinates as a single string.
    Point coordinates are encoded using signed values.
    If you only have a few static points, you may also wish to use the interactive polyline encoding utility.
    The encoding process converts a binary value into a series of character codes for ASCII characters using the familiar base64 encoding scheme:
    to ensure proper display of these characters, encoded values are summed with 63 (the ASCII character '?') before converting them into ASCII.
    The algorithm also checks for additional character codes for a given point by checking the least significant bit of each byte group;
    if this bit is set to 1, the point is not yet fully formed and additional data must follow.
    Additionally, to conserve space, points only include the offset from the previous point (except of course for the first point).
    All points are encoded in Base64 as signed integers, as latitudes and longitudes are signed values.
    The encoding format within a polyline needs to represent two coordinates representing latitude and longitude to a reasonable precision.
    Given a maximum longitude of +/- 180 degrees to a precision of 5 decimal places (180.00000 to -180.00000), this results in the need for a 32 bit signed binary integer value.
    """

    points: str


TravelMode = Literal["DRIVING", "BICYCLING", "TRANSIT", "WALKING"]


class DirectionsTransitStop(BaseModel):
    location: LatLngLiteral
    name: str


class TimeZoneTextValueObject(BaseModel):
    text: str
    time_zone: str
    value: int


class DirectionsTransitAgency(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    url: Optional[str] = None


class DirectionsTransitVehicle(BaseModel):
    name: str
    type: Literal[
        "BUS",
        "CABLE_CAR",
        "COMMUTER_TRAIN",
        "FERRY",
        "FUNICULAR",
        "GONDOLA_LIFT",
        "HEAVY_RAIL",
        "HIGH_SPEED_TRAIN",
        "INTERCITY_BUS",
        "LONG_DISTANCE_TRAIN",
        "METRO_RAIL",
        "MONORAIL",
        "OTHER",
        "RAIL",
        "SHARE_TAXI",
        "SUBWAY",
        "TRAM",
        "TROLLEYBUS",
    ]


class DirectionsTransitLine(BaseModel):
    agencies: list[DirectionsTransitAgency]
    name: str
    color: Optional[str] = None
    icon: Optional[str] = None
    short_name: Optional[str] = None
    text_color: Optional[str] = None
    url: Optional[str] = None
    vehicle: Optional[DirectionsTransitVehicle] = None


class DirectionsTransitDetails(BaseModel):
    arrival_stop: DirectionsTransitStop
    arrival_time: TimeZoneTextValueObject
    departure_stop: DirectionsTransitStop
    departure_time: TimeZoneTextValueObject
    headsign: str
    headway: int
    line: DirectionsTransitLine
    num_stops: int
    trip_short_name: Optional[str] = None


class DirectionsStep(BaseModel):
    duration: TextValueObject
    end_location: LatLngLiteral
    html_instructions: str
    polyline: DirectionsPolyline
    start_location: LatLngLiteral
    travel_mode: TravelMode
    distance: TextValueObject
    maneuver: Optional[str] = None
    steps: Optional[list] = None
    trainsit_details: Optional[DirectionsTransitDetails] = None


class DirectionsViaWaypoint(BaseModel):
    location: Optional[LatLngLiteral] = None
    step_index: Optional[int] = None
    step_interpolation: Optional[float] = None


class DirectionsLeg(BaseModel):
    end_address: str
    end_location: LatLngLiteral
    start_address: str
    start_location: LatLngLiteral
    steps: list[DirectionsStep]
    via_waypoint: list[DirectionsViaWaypoint]
    arrival_time: Optional[TimeZoneTextValueObject] = None
    departure_time: Optional[TimeZoneTextValueObject] = None
    distance: Optional[TextValueObject] = None
    duration: Optional[TextValueObject] = None
    duration_in_traffic: Optional[TextValueObject] = None


class Fare(BaseModel):
    currency: str
    text: str
    value: int


class DirectionsRoute(BaseModel):
    bounds: Bounds
    copyrights: str
    legs: list[DirectionsLeg]
    overview_polyline: DirectionsPolyline
    summary: str
    warnings: list[str]
    waypoint_order: list[int]
    fare: Optional[Fare] = None


class DirectionsRequest(BaseModel):
    origin: str
    destination: str
    target_time: datetime
    mode: Literal["driving", "walking", "bicycling", "transit"] = "transit"
    transit_mode: Literal[
        "bus", "subway", "train", "tram", "rail"
    ] = "rail"  # TODO: "train" cannot be used in Japan...
    time_mode: Literal["arrival", "departure"] = "departure"
    language: Literal[
        "ja", "en", "es", "fr", "de", "it", "pt", "ru", "zh-CN", "zh-TW"
    ] = "ja"  # see https://developers.google.com/maps/faq#languagesupport
