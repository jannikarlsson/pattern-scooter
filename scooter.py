import time
import random
import sqlite3

"""
Scooter class
"""
class Scooter():
    """
    Scooter class
    """
    def __init__(self, id, battery, user, lat, lon):
        """
        Constructor function
        """
        self._id = id
        self._speed = 0
        self._battery = battery
        self._started = False
        self._user = user
        self._position = [lat, lon]

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

    # Replace with http request
    def write_user_to_db(self):
        """
        Connects user to scooter on start, used in start method
        """
        db = sqlite3.connect('scooters.sqlite')
        cursor = db.cursor()
        cursor.execute("UPDATE scooter SET customer_id=?, rented=? WHERE id=?", (self._user, 1, self._id))
        db.commit()
        db.close()

    # Replace with http request
    def write_checkpoint_to_db(self):
        """
        Updates scooter data while running
        """
        db = sqlite3.connect('scooters.sqlite')
        cursor = db.cursor()
        cursor.execute("UPDATE scooter SET speed=?, battery_level=?, lat_pos=?, lon_pos=? WHERE id=?", (self._speed, self._battery, self._position[0], self._position[1], self._id))
        db.commit()
        db.close()

    # Replace with http request
    def write_finish_to_db(self):
        """
        Writes to database on finish, used in stop method
        """
        db = sqlite3.connect('scooters.sqlite')
        cursor = db.cursor()
        cursor.execute("UPDATE scooter SET customer_id=?, speed=?, rented=?  WHERE id=?", (None, 0, 0, self._id))
        db.commit()
        db.close()

    def start(self):
        """
        Starts scooter
        """
        if self._started is not True:
            if self._battery > 0:
                self._started = True
                self._speed = 15
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

    def random_pos(self):
        """
        Returns random position
        """
        positions = [[55.5882842, 13.0270255], [55.5953205, 12.9969136], [55.5918419, 13.0069535], [55.5934653, 13.0341114]]
        rand = positions[random.randint(0, 3)]
        self.move(rand[0], rand[1])

    def position(self):
        """
        Prints position
        """
        print('Position is {}, {}'.format(self._position[0], self._position[1]))

    def faster(self):
        """
        Accelerates scooter by 1 kph
        """
        limit = 20 # Set to speed limit
        # Makes sure scooter is started and runs below limit
        if self._started is True:
            if self._speed < limit:
                self._speed += 1
                print('Scooter now does {} kph'.format(self._speed))
            else:
                print('It is not safe to go faster')
        else:
            print('You have to start the scooter first')

    def slower(self):
        """
        Slows down scooter by 1 kph
        """
        # Makes sure scooter is started and speed is above 1 kph
        if self._started is True:
            if self._speed > 1:
                # Lowers speed
                self._speed -= 1
                print('Scooter now does {} km per hour'.format(self._speed))
            else:
                print('You cannot go slower')
        else:
            print('You have to start the scooter first')

    def lower_battery(self):
        """
        Lowers battery by 1 percent
        """
        self._battery -= 1
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
        self.speed(random.randint(1, 20))
        print('Scooter is running at {} kph'.format(self._speed))

    def run(self, runtime, delay=0):
        """
        Runs scooter
        """
        # Collects speeds during runtime to calculate average
        self.print_nice()
        print('Waiting for {} seconds'.format(delay))
        time.sleep(delay)
        speeds = []
        # Starts scooter
        self.start()
        # Loops a timeout for duration of runtime
        while runtime > 0 and self._started is True:
            print('---------------------')
            # This happens every second
            time.sleep(1)
            # Randomizes scooter speed
            self.random_speed()
            # Randomizes new position
            self.random_pos()
            self.position()
            # Battery drops and a warning is issued if battery is too low
            self.lower_battery()
            self.write_checkpoint_to_db()
            # Breaks if battery goes to 0
            if self._battery == 0:
                break
            # Subtracts from runtime before doing another loop
            runtime -= 1
        # Stops the scooter and logs trip
        self.stop()
        print('Trip was logged')