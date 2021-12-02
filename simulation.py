from dotenv import load_dotenv

# load environment variables from .env.
# (this must be done before importing from
# create_scooters_functions)
load_dotenv()  

import time
import os

import requests

import create_scooters_functions as req_funs

NUM_SCOOTERS = 800
# how long it should take to perform an action with all scooters (in seconds).
# this can't be set too low, as the time needed for each request puts limits on
# how fast updates can be done.
UPDATE_INTERVAL = 20
TOTAL_RUNTIME = 20
# number of requests to do in rapid succession, before doing a 'sleep()' call
# to give the backend room to breathe
REQUESTS_PER_BURST = 50
# handling each scooter action/request takes a bit of time. this needs to be
# compensated for when setting waiting times. here an average value (in seconds)
# based timing (with time.perf_counter) scooter handling/request run times is
# used.
AVG_TIME_REQ = 0.013852

num_bursts = NUM_SCOOTERS / REQUESTS_PER_BURST
time_to_wait_between_bursts = UPDATE_INTERVAL / num_bursts
# compensate waiting time based on time it takes to handle each action/request
time_to_wait_between_bursts -= AVG_TIME_REQ * REQUESTS_PER_BURST

# check that the update interval isn't unrealistic
assert time_to_wait_between_bursts > 0.25, (
    "Can't go that fast! You must decrease NUM_SCOOTERS or increase UPDATE_INTERVAL."
)

flush_url = os.environ['REQUEST_ROOT_URL'] + '/scooter-client/scooters/flush-cache'

# Gets selected number of scooters (from 1)
scooters = req_funs.get_scooters(NUM_SCOOTERS)

def sleep_if_burst_end(scooter_number):
    if scooter_number > 0 and (scooter_number % REQUESTS_PER_BURST == 0):
        time.sleep(time_to_wait_between_bursts)

def request_flush_cache_to_db():
    requests.post(flush_url)

for s_num, scooter in enumerate(scooters):
    sleep_if_burst_end(s_num)
    scooter.start_scooter_rental()
request_flush_cache_to_db()

start_time = time.perf_counter()
while (time.perf_counter() - start_time) < TOTAL_RUNTIME:
    t0 = time.perf_counter()
    for s_num, scooter in enumerate(scooters):
        sleep_if_burst_end(s_num)
        if scooter.is_started():
            scooter.move_to_next_position()
request_flush_cache_to_db()

for s_num, scooter in enumerate(scooters):
    sleep_if_burst_end(s_num)
    if scooter.is_started():
        scooter.end_scooter_rental()
request_flush_cache_to_db()
