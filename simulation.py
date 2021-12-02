import time
import create_scooters_functions as req_funs

max_runtime_in_seconds = 60
clock = 0

# Gets selected number of scooters (from 1)
scooters = req_funs.get_scooters(10)

for scooter in scooters:
    scooter.start_scooter_rental()
while max_runtime_in_seconds > 0:
    time.sleep(10 - clock)
    start = time.perf_counter()
    for scooter in scooters:
        if scooter.is_started():
            scooter.move_to_next_position()
    max_runtime_in_seconds -= 10
    end = time.perf_counter()
    clock = end - start
for scooter in scooters:
    if scooter.is_started():
        scooter.end_scooter_rental()