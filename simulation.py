from dotenv import load_dotenv

# load environment variables from .env.
# (this must be done before importing from
# create_scooters_functions)
load_dotenv()  

import time
import os

import requests

import create_scooters_functions as req_funs

NUM_SCOOTERS = 100
UPDATE_INTERVAL = 10
TOTAL_RUNTIME = 20
# number of requests to do in rapid succession, before doing a 'sleep()' call
# to give the backend room to breathe
REQUESTS_PER_BURST = 100

num_bursts = NUM_SCOOTERS / REQUESTS_PER_BURST
time_to_wait_between_bursts = UPDATE_INTERVAL / num_bursts

# Gets selected number of scooters (from 1)
scooters = req_funs.get_scooters(NUM_SCOOTERS)

for scooter in scooters:
    scooter.start_scooter_rental()

start_time = time.perf_counter()
while (time.perf_counter() - start_time) < TOTAL_RUNTIME:
    for s_num, scooter in enumerate(scooters):
        if s_num % REQUESTS_PER_BURST == 0:
                time.sleep(time_to_wait_between_bursts)
        if scooter.is_started():
            scooter.move_to_next_position()

for s_num, scooter in enumerate(scooters):
    if s_num % REQUESTS_PER_BURST == 0:
        time.sleep(time_to_wait_between_bursts)
    if scooter.is_started():
        scooter.end_scooter_rental()
