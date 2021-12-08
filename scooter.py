"""
Scooter class
"""
from distance_calc import distance_funs as dfun
import run_scooter_functions as rfun

class Scooter():
    """
    Scooter class
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, data):
        """
        Constructor function
        """
        # Sets scooter details
        self._id = data["id"]
        self._battery = data["battery"]
        self._speed = rfun.random_speed()
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
        self._remainder = dfun.calculate_geo_distance(
            self._position[0],
            self._position[1],
            self._target[0],
            self._target[1]
        )

    # Ride methods

    def start_scooter_rental(self):
        """
        Starts scooter
        """
        if self._started is not True:
            if self._battery > 0:
                self.turn_engine_on()
                self.write_user_to_db()
                print(f'Scooter {self._id} was started')
            else:
                print('The battery is dead, charge the scooter.')
        else:
            print('Scooter is already running')

    def move_to_next_position(self):
        """
        Move to next position
        """
        next_step = rfun.get_next(
            self._position[0],
            self._position[1],
            self._target[0],
            self._target[1],
            self._step
        )
        self.move(next_step[0], next_step[1])
        self.lower_battery()
        self.write_checkpoint_to_db()
        print(f'Scooter {self._id} moved forward')
        if self._battery < 0.02 or self._remainder < 0.1:
            self.end_scooter_rental()

    def end_scooter_rental(self):
        """
        Stops scooter
        """
        if self._started is True:
            self.turn_engine_off()
            self.write_finish_to_db()
            print(f'Scooter {self._id} was returned')
        else:
            print('Scooter is not running')

    # Utility methods

    def turn_engine_on(self):
        """
        Sets scooter to started
        """
        self._started = True

    def turn_engine_off(self):
        """
        Sets scooter to not started
        """
        self._started = False
        self._speed = 0

    def is_started(self):
        """
        Is the scooter running?
        """
        return self._started

    def move(self, lat, lon):
        """
        Changes position
        """
        self._position = [lat, lon]
        self._remainder = dfun.calculate_geo_distance(
            self._position[0],
            self._position[1],
            self._target[0],
            self._target[1]
        )
        # print('New position is {}'.format(self._position))
        # print('Distance to target is {}'.format(self._remainder))
        # print('Battery level is {}'.format(self._battery))

    def lower_battery(self):
        """
        Lowers battery
        """
        self._battery -= 1/6
        # print('Battery level is {}'.format(self._battery))


    # Methods for writing to database

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


    # Methods for interactive mode

    def fill_battery(self):
        """
        Charges battery to full
        """
        self._battery = 100
        print('Battery level is now at 100 per cent')

    def print_nice(self):
        """
        Prints scooter deets
        """
        print(f'Scooter id is {self._id}')
        print(f'User id is {self._user}')
        print(f'Current speed is {self._speed}')
        print(f'Battery level is {self._battery}')
        print(f'Position is {self._position[0]}, {self._position[1]}')
        if self._started:
            print('Scooter is running')
        else:
            print('Scooter is not running')
        print(f'Target is {self._target[0]}, {self._target[1]}')
        print(f'Step length is {self._step}')
        print(f'{self._remainder} km remains')
        