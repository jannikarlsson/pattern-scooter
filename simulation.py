import requests
import time
from scooter import Scooter

scooters = []

url = 'http://localhost:8000/api/scooters/'
r = requests.get(url).json()

x = 0
for i in r:
    if x > 4:
        break
    scooters.append(Scooter(i["id"]+30, i["battery_level"], 2, i["lat_pos"], i["lon_pos"]))
    x += 1

runtime = 60
for scooter in scooters:
    scooter.start()
while runtime > 0:
    time.sleep(5)
    for scooter in scooters:
        scooter.random_pos()
        scooter.position()
        scooter.lower_battery()
        scooter.write_checkpoint_to_db()
        if scooter._battery == 0:
                scooter.stop()
    runtime -= 5
for scooter in scooters:
    scooter.stop()