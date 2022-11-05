import os
import googlemaps
from googlemaps.client import directions
from datetime import datetime


from directions_route import DirectionsRoute


API_KEY = os.getenv("API_KEY")


def main(
    origin: str,
    destination: str,
    mode: str,
    transit_mode: str,
    departure_time: datetime = datetime.now(),
):
    gmaps = googlemaps.Client(key=API_KEY)

    directions_result = directions(
        gmaps,
        origin=origin,
        destination=destination,
        mode=mode,
        departure_time=datetime.timestamp(departure_time),
        transit_mode=transit_mode,
    )
    if directions_result:
        route_1 = DirectionsRoute(**directions_result[0])
        duration = route_1.legs[0].duration
        distance = route_1.legs[0].distance
        if duration is None or distance is None:
            return None
        print(distance.value // 1000, duration.value // 60)


if __name__ == "__main__":
    main("東京駅", "スカイツリー", "transit", "rail", datetime.now())
