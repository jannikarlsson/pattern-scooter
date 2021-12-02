import random
from distance_calc import distance_funs as dfun
import run_funs as rfun

"""
Scooter class
"""
class Scooter():
    """
    Scooter class
    """    
    def __init__(self, data):
        """
        Constructor function
        """
        self._id = data["id"]
        self._battery = data["battery"]
        self._speed = self.random_speed()
        self._started = False
        self._user = data["user"]
        self._position = [float(data["lat"]), float(data["lon"])]
        if data["city"] == 1:
            self._target = dfun.random_p_skovde()
        elif data["city"] == 2:
            self._target = dfun.random_p_lund()
        elif data["city"] == 3:
            self._target = dfun.random_p_uppsala()
        self._step = rfun.get_step(self._speed, 10)
        # self._next_step = functions.get_next(self._position[0], self._position[1], self._target[0], self._target[1], self._step)
        # print(type(self._position[0]), type(self._position[1]))
        self._remainder = dfun.calculate_geo_distance(self._position[0], self._position[1], self._target[0], self._target[1])

    @property
    def get(self):
        """
        Returns scooter
        """
        return self._id, self._speed, self._battery, self._started

    def print_nice(self):
        """
        Prints scooter deets
        """
        print('Scooter id is {}'.format(self._id))
        print('User id is {}'.format(self._user))
        print('Current speed is {}'.format(self._speed))
        print('Battery level is {}'.format(self._battery))
        print('Position is {}, {}'.format(self._position[0], self._position[1]))
        print('Scooter is running') if self._started else print('Scooter is not running')
        print('Target is {}, {}'.format(self._target[0], self._target[1]))
        print('Step length is {}'.format(self._step))
        # print('Next step is {}'.format(self._next_step))
        print('{} km remains'.format(self._remainder))

    def write_user_to_db(self):
        """
        Connects user to scooter on start, used in start method
        """
        data = {
            'customer_id': self._user,
            'speed_kph': self._speed
        }
        rfun.start(self._id, data)

    def write_checkpoint_to_db(self):
        """
        Updates scooter data while running
        """
        data = {
            'station_id': "setNull",
            'battery_level': self._battery,
            'lat_pos': self._position[0],
            'lon_pos': self._position[1]
        }
        rfun.checkpoint(self._id, data)

    def write_finish_to_db(self):
        """
        Writes to database on finish, used in stop method
        """
        data = {
            'customer_id': "setNull",
            'speed_kph': 0
        }
        rfun.stop(self._id, data)

    def start(self):
        """
        Starts scooter
        """
        if self._started is not True:
            if self._battery > 0:
                self._started = True
                # self._speed = 15
                print('Scooter started')
                self.write_user_to_db()
            else:
                print('The battery is dead, charge the scooter.')
        else:
            print('Scooter is already running')

    def stop(self):
        """
        Stops scooter
        """
        if self._started is True:
            self._started = False
            self._speed = 0
            print('Scooter stopped')
            self.write_finish_to_db()
        else:
            print('Scooter is not running')

    def next(self):
        """
        Move to next position
        """
        next_step = rfun.get_next(self._position[0], self._position[1], self._target[0], self._target[1], self._step)
        self.move(next_step[0], next_step[1])

    def speed(self, speed):
        """
        Changes speed
        """
        self._speed = speed if self._started else print('Scooter is not running')

    def move(self, lat, lon):
        """
        Changes position
        """
        self._position = [lat, lon]
        self._remainder = dfun.calculate_geo_distance(self._position[0], self._position[1], self._target[0], self._target[1])
        self.lower_battery()
        self.write_checkpoint_to_db()
        # print('New position is {}'.format(self._position))
        # print('Distance to target is {}'.format(self._remainder))
        # print('Battery level is {}'.format(self._battery))

    # def position(self):
    #     """
    #     Prints position
    #     """
    #     print('Position is {}, {}'.format(self._position[0], self._position[1]))

    # def faster(self):
    #     """
    #     Accelerates scooter by 1 kph
    #     """
    #     limit = 20 # Set to speed limit
    #     # Makes sure scooter is started and runs below limit
    #     if self._started is True:
    #         if self._speed < limit:
    #             self._speed += 1
    #             print('Scooter now does {} kph'.format(self._speed))
    #         else:
    #             print('It is not safe to go faster')
    #     else:
    #         print('You have to start the scooter first')

    # def slower(self):
    #     """
    #     Slows down scooter by 1 kph
    #     """
    #     # Makes sure scooter is started and speed is above 1 kph
    #     if self._started is True:
    #         if self._speed > 1:
    #             # Lowers speed
    #             self._speed -= 1
    #             print('Scooter now does {} km per hour'.format(self._speed))
    #         else:
    #             print('You cannot go slower')
    #     else:
    #         print('You have to start the scooter first')

    def lower_battery(self):
        """
        Lowers battery by 1 percent
        """
        self._battery -= 1/6
        print('Battery level is {}'.format(self._battery))
        self.battery_warning()

    def battery_warning(self):
        """
        Warns if battery is too low
        """
        if self._battery < 10:
            print('Battery low')

    def fill_battery(self):
        """
        Charges battery to full
        """
        self._battery = 100
        print('Battery level is now at 100 per cent')

    def random_speed(self):
        """
        Randomizes speed within reason
        """
        return random.randint(10, 20)


    # def run(self, runtime, delay=0):
    #     """
    #     Runs scooter
    #     """
    #     # Collects speeds during runtime to calculate average
    #     self.print_nice()
    #     print('Waiting for {} seconds'.format(delay))
    #     time.sleep(delay)
    #     speeds = []
    #     # Starts scooter
    #     self.start()
    #     # Loops a timeout for duration of runtime
    #     while runtime > 0 and self._started is True:
    #         print('---------------------')
    #         # This happens every five seconds
    #         time.sleep(5)
    #         # Randomizes scooter speed
    #         self.random_speed()
    #         # Randomizes new position
    #         self.random_pos()
    #         self.position()
    #         # Battery drops and a warning is issued if battery is too low
    #         self.lower_battery()
    #         self.write_checkpoint_to_db()
    #         # Breaks if battery goes to 0
    #         if self._battery == 0:
    #             break
    #         # Subtracts from runtime before doing another loop
    #         runtime -= 5
    #     # Stops the scooter and logs trip
    #     self.stop()
    #     print('Trip was logged')