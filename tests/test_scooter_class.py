#!/usr/bin/env python3
""" Module for unittests """
from dotenv import load_dotenv

# load environment variables from .env.
# (this must be done before importing from
# create_scooters_functions and simulation_flow_functions)
load_dotenv()

import unittest
import responses
import os
from scooter import Scooter

class TestScooter(unittest.TestCase):
    """ Submodule for unittests, derives from unittest.TestCase """
    def setUp(self):
        """ Create object for all tests """
        # Arrange
        data = {
            "id": 1,
            "battery": 50.0,
            "user": 2,
            "lat": 58.39882600376766,
            "lon": 13.871569099334012,
            "city": 1
        }
        self.scooter = Scooter(data)

        put_scooters_base_url = os.environ['REQUEST_ROOT_URL'] + '/scooter-client/scooters/'
        responses.add(
            responses.Response(
            method='PUT',
            url=put_scooters_base_url + str(self.scooter._id)
            )
        )

    def tearDown(self):
        """ Remove dependencies after test """
        self.scooter = None

    def test_scooter_info(self):
        """Test that init values are correct for scooter"""
        # Assert
        self.assertEqual(self.scooter._id, 1)
        self.assertEqual(self.scooter._user, 2)
        self.assertEqual(self.scooter._battery, 50)
        self.assertEqual(self.scooter._position, [58.39882600376766, 13.871569099334012])
        self.assertGreater(self.scooter._speed, 0)
        self.assertTrue(self.scooter._target)
        self.assertEqual(self.scooter._started, False)

    def test_lower_battery(self):
        """ Test that battery lowers """
        # Arrange
        old_battery = self.scooter._battery
        battery_loss = 1/6
        # Act
        self.scooter.lower_battery()
        # Assert
        self.assertLess(self.scooter._battery, old_battery)

    def test_fill_battery(self):
        """ Test that battery fills """
        # Act
        self.scooter.fill_battery()
        # Assert
        self.assertEqual(self.scooter._battery, 100)

    def test_get_started(self):
        """ Test that function to check if scooter is started works """
        # Act
        result = self.scooter.is_started()
        # Assert
        self.assertFalse(result)

    def test_turn_on(self):
        """ Test that scooter starts """
        # Act
        self.scooter.turn_engine_on()
        # Assert
        self.assertTrue(self.scooter._started)
        self.assertTrue(self.scooter.is_started())

    def test_turn_off(self):
        """ Test that scooter turns off """
        # Act
        self.scooter.turn_engine_off()
        # Assert
        self.assertFalse(self.scooter._started)
        self.assertFalse(self.scooter.is_started())
        self.assertEqual(self.scooter._speed, 0)

    @responses.activate
    def test_new_position(self):
        """ Test that position and remaining distance are changed """
        # Arrange
        old_lat = self.scooter._position[0]
        old_lon = self.scooter._position[1]
        old_remainder = self.scooter._remainder
        # Act
        self.scooter.move(58.34082600376766, 13.881569099334012)
        # Assert
        self.assertNotEqual(self.scooter._position[0], old_lat)
        self.assertNotEqual(self.scooter._position[1], old_lon)
        self.assertNotEqual(self.scooter._remainder, old_remainder)

    @responses.activate
    def test_start_move(self):
        """ Test that start process works """
        # Act
        self.scooter.start_scooter_rental()
        # Assert
        self.assertTrue(self.scooter._started)

        # Arrange
        self.scooter._started = False
        self.scooter._battery = 0
        # Act
        self.scooter.start_scooter_rental()
        # Assert
        self.assertFalse(self.scooter._started)

    @responses.activate
    def test_move_move(self):
        """ Test that checkpoint works """
        # Arrange
        self.scooter._started = True
        old_lat = self.scooter._position[0]
        old_lon = self.scooter._position[1]
        old_remainder = self.scooter._remainder
        old_battery = self.scooter._battery
        # Act
        self.scooter.move_to_next_position()
        # Assert
        self.assertNotEqual(self.scooter._position[0], old_lat)
        self.assertNotEqual(self.scooter._position[1], old_lon)
        self.assertNotEqual(self.scooter._remainder, old_remainder)
        self.assertLess(self.scooter._battery, old_battery)
        self.assertTrue(self.scooter._started)

        # Arrange
        self.scooter._battery = 0.01
        # Act
        self.scooter.move_to_next_position()
        # Assert
        self.assertFalse(self.scooter._started)

        # Arrange
        self.scooter._remainder = 0.01
        # Act
        self.scooter.move_to_next_position()
        # Assert
        self.assertFalse(self.scooter._started)

    @responses.activate
    def test_end_move(self):
        # Arrange
        self.scooter._started = True
        # Act
        self.scooter.end_scooter_rental()
        # Assert
        self.assertFalse(self.scooter._started)
        self.assertEqual(self.scooter._speed, 0)