import os
import time

import requests


ACTION_DURATION = float(os.environ['ACTION_DURATION'])

flush_url = os.environ['REQUEST_ROOT_URL'] + '/scooter-client/scooters/flush-cache'

# borrowed from
# https://stackoverflow.com/questions/2130016/
# splitting-a-list-into-n-parts-of-approximately-equal-length
def split_evenly(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def request_flush_cache_to_db():
    requests.post(flush_url)

def keep_time_and_flush_decorator(fun):
    def decorated_fun(*args, **kwargs):
        t_start_action = time.perf_counter()
        ret_val = fun(*args, **kwargs)
        request_flush_cache_to_db()
        t_end_action = time.perf_counter()
        action_duration = t_end_action - t_start_action
        interval_time_left = ACTION_DURATION - action_duration
        if interval_time_left > 0:
            time.sleep(interval_time_left)        
        return ret_val
    return decorated_fun

@keep_time_and_flush_decorator
def start_scooters(scooters):
    for s_num, scooter in enumerate(scooters):
        scooter.start_scooter_rental()

@keep_time_and_flush_decorator
def move_scooters(scooters):
    for s_num, scooter in enumerate(scooters):
        if scooter.is_started():
            scooter.move_to_next_position()

@keep_time_and_flush_decorator
def stop_scooters(scooters):
    for s_num, scooter in enumerate(scooters):
        if scooter.is_started():
            scooter.end_scooter_rental()

def single_simulation(scooters, move_time):
    start_scooters(scooters)
    start_time = time.perf_counter()
    while (time.perf_counter() - start_time) < move_time:
        move_scooters(scooters)
    stop_scooters(scooters)
