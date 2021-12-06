from dotenv import load_dotenv

# load environment variables from .env.
# (this must be done before importing from
# create_scooters_functions and simulation_flow_functions)
load_dotenv()

import create_scooters_functions as req_funs

def interactive_mode(selected):
    """
    Prints menu and handles input
    """
    print("MENU: see, start, move, stop, charge, return")
    while True:
        choice = input("--> ")
        if choice == "return":
            print("Thank you for riding sctr")
            break
        if choice == "start":
            selected.start_scooter_rental()
        elif choice == "move":
            selected.move_to_next_position()
        elif choice == "stop":
            selected.end_scooter_rental()
        elif choice == "see":
            selected.print_nice()
        elif choice == "charge":
            selected.fill_battery()   
        else:
            print("Try again")

if __name__ == "__main__":
    inp = input('Enter id: ')
    user = int(input('Enter user id: '))

    selected = req_funs.single(inp, user)
    interactive_mode(selected)

