import requests
import time
import req_funs


scooters = req_funs.get_scooters()
runtime = 20

for scooter in scooters:
    scooter.start()
while runtime > 0:
    # time.sleep(5)
    start = time.perf_counter()

    for scooter in scooters:
        scooter.next()
        # scooter.lower_battery()
        # scooter.write_checkpoint_to_db()
        if scooter._battery == 0.00:
                scooter.stop()
    runtime -= 5
    end = time.perf_counter()
    print(end - start)
for scooter in scooters:
    scooter.stop()