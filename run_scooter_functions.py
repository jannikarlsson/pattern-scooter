import os

from distance_calc import distance_funs as dfun
import requests
import random

req_s = requests.Session()

put_scooters_base_url = os.environ['REQUEST_ROOT_URL'] + '/scooter-client/scooters/'

def put_wait_resp(id, data):
    url = put_scooters_base_url + str(id)
    req_s.put(url, data=data)

def get_step(speed, duration):
    """
    Calculates step distance
    """
    # scooterns hatighet i km/s
    scooter_kmps = speed / 3600
    # förflyttning i km per 'steg', alltså per 'hopp' som ska ske. 
    return scooter_kmps * duration

def get_next(lat_pos, lon_pos, target_lat, target_lon, step):
    """ 
    Returns next position for scooter
    """
    lat_diff_per_step, lon_diff_per_step = dfun.calculate_step_lat_lon(lat_pos, lon_pos, target_lat, target_lon, step)
    next_lat = lat_pos + lat_diff_per_step
    next_lon = lon_pos + lon_diff_per_step
    return (next_lat, next_lon)

def random_speed():
    """
    Randomizes speed within reason
    """
    return random.randint(10, 20)

def start(id, data):
    """
    Starts scooter, writes user and speed to db, removes station
    """
    put_wait_resp(id, data)

def checkpoint(id, data):
    """
    Writes position to db
    """
    put_wait_resp(id, data)

def stop(id, data):
    """
    Stops scooter, removes customer and sets speed to zero
    """
    put_wait_resp(id, data)
