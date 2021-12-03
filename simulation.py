import time
import create_scooters_functions as req_funs
import argparse

parser = argparse.ArgumentParser(description='For parsing scooter deets')
parser.add_argument('--number', nargs='?', default=0, const=0)
parser.add_argument('--start', nargs='?', default=0, const=0)
args = parser.parse_args()

# Checks if there is an input argument
how_many = args.number
start_no = args.start

max_runtime_in_seconds = 60
clock = 0
# how_many = input("Hur många scootrar? ")
# start_no = input("Var börjar vi? ")

# Gets selected number of scooters (from 1)
scooters = req_funs.get_scooters(how_many, start_no)

for scooter in scooters:
    scooter.start_scooter_rental()
while max_runtime_in_seconds > 0:
    # time.sleep(10 - clock)
    start = time.perf_counter()
    for scooter in scooters:
        if scooter.is_started():
            scooter.move_to_next_position()
    max_runtime_in_seconds -= 10
    # end = time.perf_counter()
    # clock = end - start
for scooter in scooters:
    if scooter.is_started():
        scooter.end_scooter_rental()