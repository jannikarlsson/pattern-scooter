import requests
from scooter import Scooter

def print_menu(selected):
    """
    Prints menu and handles input
    """
    print("MENU: see, start, stop, faster, slower, move, charge, run, return")
    while True:
        choice = input("--> ")
        if choice == "return":
            print("Thank you for riding sctr")
            break
        if choice == "start":
            selected.start()
        elif choice == "stop":
            selected.stop()
        elif choice == "see":
            selected.print_nice()
        elif choice == "faster":
            selected.faster()
        elif choice == "slower":
            selected.slower()
        elif choice == "charge":
            selected.fill_battery()
        elif choice == "move":
            lat = input('Lat: ')
            lon = input('Lon: ')
            selected.move(lat, lon)
        elif choice == "run":
            selected.run(20)     
        else:
            print("Try again")

# Replace with http request
def get_scooter_by_id(inp, user):
    """
    Gets scooter from database
    """
    url = 'http://localhost:8000/api/scooters/' + inp
    r = requests.get(url)
    scooter = r.json()[0]
    battery = scooter["battery_level"]
    lat = scooter["lat_pos"]
    lon = scooter["lon_pos"]
    selected = Scooter(inp, battery, user, lat, lon)

    return selected

def simulate(inp, user, runtime, delay=0, menu=0):
    """
    Run simulation
    """
    selected = get_scooter_by_id(inp, user)
    if menu != 0:
        print_menu(selected)
    else:
        selected.run(runtime, delay)
    