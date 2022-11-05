import os
from datetime import datetime, timedelta, timezone
from typing import Literal, Optional

import googlemaps
from fastapi import Body, FastAPI
from googlemaps.client import directions, places

from src.directions import DirectionsRequest, DirectionsRoute
from src.places import PlacesRequest, PlacesResult

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


app = FastAPI()
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/places/", response_model=PlacesResult)
async def get_places(request: PlacesRequest) -> Optional[PlacesResult]:
    places_result = places(gmaps, query=request.query, language=request.language)
    if places_result:
        place_1 = PlacesResult(**places_result)
        return place_1
    else:
        return None


@app.post("/api/directions/", response_model=list[DirectionsRoute])
async def get_directions(request: DirectionsRequest) -> list[DirectionsRoute]:
    directions_result = directions(
        gmaps,
        origin=request.origin,
        destination=request.destination,
        mode=request.mode,
        waypoints=None,
        alternatives=False,
        avoid=None,
        language=request.language,
        units=None,
        region=None,
        departure_time=datetime.timestamp(request.target_time)
        if request.time_mode == "departure" and request.target_time is not None
        else None,
        arrival_time=datetime.timestamp(request.target_time)
        if request.time_mode == "arrival" and request.target_time is not None
        else None,
        optimize_waypoints=False,
        transit_mode=request.transit_mode,
        transit_routing_preference=None,
        traffic_model=None,
    )
    if directions_result:
        route_1 = [DirectionsRoute(**d) for d in directions_result]
        # duration = route_1.legs[0].duration
        # distance = route_1.legs[0].distance
        # if duration is None or distance is None:
        #     return None
        # print(distance.value // 1000, "km", duration.value // 60, "min")
        # for idx, step in enumerate(route_1.legs[0].steps):
        #     if idx == 0:
        #         print(route_1.legs[0].start_address)
        #     print(f"|{step.distance.text, step.duration.text}")
        #     print(f"|{step.html_instructions}")
        #     print("●")
        #     if idx == len(route_1.legs[0].steps) - 1:
        #         print(route_1.legs[0].end_address)
        # print(route_1.fare)
        return route_1
    else:
        return []
