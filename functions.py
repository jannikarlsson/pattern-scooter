import sqlite3
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
            selected.run(5)     
        else:
            print("Try again")

# Replace with http request
def get_scooter_by_id(inp, user):
    """
    Gets scooter from database
    """
    db = sqlite3.connect('scooters.sqlite')
    cursor = db.cursor()
    scooter = cursor.execute("SELECT * FROM scooter WHERE id=?", (inp))
    for row in scooter:
        id = row[0]
        battery = row[10]
        lat = row[5]
        lon = row[6]
        if id is not None and battery is not None:
            selected = Scooter(id, battery, user, lat, lon)
    db.close()
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
    