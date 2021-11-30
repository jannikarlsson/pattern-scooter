import time
import random
import requests

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
        data = {
            'customer_id': self._user
        }
        url = 'http://localhost:8000/api/scooters/' + str(self._id)
        requests.put(url, data=data)

    # Replace with http request
    def write_checkpoint_to_db(self):
        """
        Updates scooter data while running
        """
        data = {
            'station_id': "setNull",
            'speed_kph': self._speed,
            'battery_level': self._battery,
            'lat_pos': self._position[0],
            'lon_pos': self._position[1]
        }
        url = 'http://localhost:8000/api/scooters/' + str(self._id)
        requests.put(url, data=data)

    # Replace with http request
    def write_finish_to_db(self):
        """
        Writes to database on finish, used in stop method
        """
        data = {
            'customer_id': "setNull",
            'speed_kph': 0
        }
        url = 'http://localhost:8000/api/scooters/' + str(self._id)
        requests.put(url, data=data)

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
        positions = [[58.39882600376766,13.871569099334012],[58.395693371106624,13.843618868614481],[58.38618768808369,13.848690760645137],[58.395616863824756,13.881262424434263],[58.39564653590455,13.852659064934594],[58.38645878896987,13.839360941370566],[58.40668859857108,13.9443357855501],[58.3993093655605,13.869271845936805],[58.3867690335166,13.94114929091914],[58.42078698972386,13.88732444409999],[58.402068818577845,13.898481276015227],[58.39093400065418,13.831671651606877],[58.359628139007526,13.926565086729251],[58.381790919512476,13.828074274364441],[58.394947663336474,13.898459346970263],[58.39901159966676,13.87231895676518],[58.37078774987054,13.81393344129093],[58.38875533395506,13.943838249466689],[58.4091588571796,13.902874348640488],[58.35643855682776,13.86120219344085],[58.36664864442891,13.829360407854987],[58.40243816229685,13.88603772084677],[58.42583631742574,13.870538305148568],[58.42141884095812,13.904379724696929],[58.36553763373325,13.910976526055618],[58.41930623277213,13.926203604619575],[58.40700829129591,13.817870328448713],[58.4194614495202,13.895149563243644],[58.42301812205896,13.858256685075908],[58.39075263923765,13.842429867228173],[58.42956448291202,13.88060720598044],[58.38331881022612,13.871024449312158],[58.38893835908344,13.88392612584412],[58.36695527016371,13.872791288978831],[58.39806371355143,13.844891648201553],[58.403611738186015,13.926943961188151],[58.39994128559166,13.887063033220045],[58.39447151445227,13.812954771592192],[58.384490988921144,13.851775528602973],[58.3736157492296,13.829464295393175]]
        rand = positions[random.randint(0, 20)]
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
            # This happens every five seconds
            time.sleep(5)
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
            runtime -= 5
        # Stops the scooter and logs trip
        self.stop()
        print('Trip was logged')