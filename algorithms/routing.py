import requests


def get_route(
    start_lat,
    start_lon,
    end_lat,
    end_lon,
):
    """
    Get a road route using the OSRM public routing service.

    Returns:
        Distance in km
        Duration in minutes
        Route geometry
    """

    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};"
        f"{end_lon},{end_lat}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson",
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if data["code"] != "Ok":
        return None

    route = data["routes"][0]

    return {
        "distance_km": route["distance"] / 1000,
        "duration_minutes": route["duration"] / 60,
        "geometry": route["geometry"],
    }