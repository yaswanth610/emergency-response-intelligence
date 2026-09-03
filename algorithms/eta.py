def calculate_eta(distance_km, speed_kmh):
    """
    Calculate estimated travel time.

    Returns:
        ETA in minutes.
    """

    if speed_kmh <= 0:
        return float("inf")

    time_hours = distance_km / speed_kmh

    time_minutes = time_hours * 60

    return time_minutes