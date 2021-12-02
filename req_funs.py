import requests
from scooter import Scooter

def get_scooters():
    scooters = []
    url = 'http://localhost:8000/api/scooters/'
    r = requests.get(url).json()

    x = 0
    for i in r:
        if x > 5:
            break
        data = {
            "id": i["id"],
            "battery": float(i["battery_level"]),
            "user": 2,
            "lat": i["lat_pos"],
            "lon": i["lon_pos"],
            "city": i["city_id"]
        }
        scooters.append(Scooter(data))
        x += 1
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