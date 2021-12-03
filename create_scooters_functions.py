import requests
from scooter import Scooter

def get_scooters(n, start):
    scooters = []
    url = 'http://localhost:8000/api/scooters/'
    r = requests.get(url).json()

    n = int(n)
    start = int(start)

    for i in range(n):
        data = {
            "id": r[i+start]["id"],
            "battery": float(r[i+start]["battery_level"]),
            "user": r[i+start]["id"],
            "lat": r[i+start]["lat_pos"],
            "lon": r[i+start]["lon_pos"],
            "city": r[i+start]["city_id"]
        }
        if r[i+start]["status"] == "active" and float(r[i+start]["battery_level"]) > 5.0:
            scooters.append(Scooter(data))
    return scooters


def single(inp, user):
    """
    Gets scooter from database
    """
    url = 'http://localhost:8000/api/scooters/' + inp
    r = requests.get(url)
    scooter = r.json()[0]
    # battery = scooter["battery_level"]
    # pos = [scooter["lat_pos"], scooter["lon_pos"]]
    data = {
        "id": inp,
        "battery": float(scooter["battery_level"]),
        "user": user,
        "lat": scooter["lat_pos"],
        "lon": scooter["lon_pos"],
        "city": scooter["city_id"]
    }
    selected = Scooter(data)

    return selected