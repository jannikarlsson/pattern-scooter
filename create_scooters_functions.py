"""
Create scooters functions
"""

import os
import requests
from scooter import Scooter

scooters_base_url = os.environ['REQUEST_ROOT_URL'] + '/scooter-client/scooters/'

def get_scooters(number_of_scooters):
    """
    Get all scooters from database
    """
    scooters = []
    res = requests.get(scooters_base_url).json()

    for i in range(number_of_scooters):
        data = {
            "id": res[i]["id"],
            "battery": float(res[i]["battery_level"]),
            "user": i+1,
            "lat": res[i]["lat_pos"],
            "lon": res[i]["lon_pos"],
            "city": res[i]["city_id"]
        }
        if res[i]["status"] == "active" and float(res[i]["battery_level"]) > 5.0:
            scooters.append(Scooter(data))
    return scooters


def single(inp, user):
    """
    Gets scooter from database
    """
    url = scooters_base_url + inp
    res = requests.get(url)
    scooter = res.json()[0]
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
