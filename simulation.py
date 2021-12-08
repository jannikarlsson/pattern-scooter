"""
Main simulation file
"""
# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order

from dotenv import load_dotenv

# load environment variables from .env.
# (this must be done before importing from
# create_scooters_functions and simulation_flow_functions)
load_dotenv()

import os
from concurrent.futures import ThreadPoolExecutor
import random
import time

import create_scooters_functions as req_funs
import simulation_flow_functions as sff

TOTAL_NUM_SCOOTERS = int(os.environ['TOTAL_NUM_SCOOTERS'])
MOVE_TIME = float(os.environ['MOVE_TIME'])
NUM_THREADS = int(os.environ['NUM_THREADS'])
THREAD_STAGGER_S = float(os.environ['THREAD_STAGGER_S'])

def run_simulations():
    """ Run simulations """
    # get selected number of scooters (from 1)
    scooters = req_funs.get_scooters(TOTAL_NUM_SCOOTERS)

    # shuffle scooters to make sure that some scooters in each city are being
    # moved.
    random.shuffle(scooters)

    # split list of scooters up to enable delegation of work between
    # threads
    scooter_chunks = list(sff.split_evenly(scooters, NUM_THREADS))

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        # spin up one thread per 'chunk' of scooters
        for scooter_chunk in scooter_chunks:
            executor.submit(
                sff.single_simulation,
                scooters=scooter_chunk,
                move_time=MOVE_TIME
            )
            time.sleep(THREAD_STAGGER_S)

if __name__ == "__main__":
    run_simulations()
