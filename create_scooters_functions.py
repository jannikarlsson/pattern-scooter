import requests
from scooter import Scooter
import os

scooters_base_url = os.environ['REQUEST_ROOT_URL'] + '/api/scooters/'

def get_scooters(n):
    scooters = []
    r = requests.get(scooters_base_url).json()

    for i in range(n):
        data = {
            "id": r[i]["id"],
            "battery": float(r[i]["battery_level"]),
            "user": 2,
            "lat": r[i]["lat_pos"],
            "lon": r[i]["lon_pos"],
            "city": r[i]["city_id"]
        }
        if r[i]["status"] == "active" and float(r[i]["battery_level"]) > 5.0:
            scooters.append(Scooter(data))
    return scooters


def single(inp, user):
    """
    Gets scooter from database
    """
    url = scooters_base_url + inp
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