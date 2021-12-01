import unittest
from math import ceil, pi
import random

from distance_calc.distance_funs import (
    calculate_bearing,
    calculate_geo_distance,
    calculate_step_lat_lon,
    move_lat_lon,
    random_point,
    random_p_lund,
)
from distance_calc.distance_constants import UPPSALA_GEO, LUND_GEO

class TestDistanceCalc(unittest.TestCase):
    def test_calculate_bearing(self):
        """
        Initial bearing when starting from Uppsala and pointing at Lund is
        approximated to close to 3.69430449 rad.
        """
        bearing_correct = 3.69430449
        bearing_calculated = calculate_bearing(
            UPPSALA_GEO['center_lat'],
            UPPSALA_GEO['center_lon'],
            LUND_GEO['center_lat'],
            LUND_GEO['center_lon']
        )
        self.assertAlmostEqual(bearing_correct, bearing_calculated, 5)

    def test_calculate_geo_distance(self):
        """
        Distance between Uppsala and Lund should be close to
        531.4 kilometers
        """
        dist_correct = 531.4
        dist_calculated = calculate_geo_distance(
            UPPSALA_GEO['center_lat'],
            UPPSALA_GEO['center_lon'],
            LUND_GEO['center_lat'],
            LUND_GEO['center_lon']
        )
        self.assertAlmostEqual(dist_correct, dist_calculated, 1)

    def test_random_point(self):
        """
        Ten randomly generated points are all within expected distance of center.
        """
        random_points = [random_p_lund() for i in range(10)]
        for p in random_points:
            dist_lund_c = calculate_geo_distance(
                p[0],
                p[1],
                LUND_GEO['center_lat'],
                LUND_GEO['center_lon']
            )
            self.assertLessEqual(dist_lund_c, LUND_GEO['radius'])

    def test_move_lat_lon(self):
        # move 200m (0.2km)
        move_dist = 0.2
        # move at a bearing/angle of pi/2 (ie straight east, 90 degrees from north)
        bearing = pi/2
        post_move_point = move_lat_lon(
            UPPSALA_GEO['center_lat'],
            UPPSALA_GEO['center_lon'],
            move_dist,
            bearing
        )
        postmove_start_dist = calculate_geo_distance(
            UPPSALA_GEO['center_lat'],
            UPPSALA_GEO['center_lon'],
            post_move_point[0],
            post_move_point[1]
        )
        self.assertAlmostEqual(move_dist, postmove_start_dist, 5)
        # check that the move was made in the right direction, meaning
        # longitude increased (moving east) while latitude stayed essentially
        # the same
        diff_lat = post_move_point[0] - UPPSALA_GEO['center_lat']
        diff_lon = post_move_point[1] - UPPSALA_GEO['center_lon']
        self.assertAlmostEqual(diff_lat, 0, 7)
        self.assertGreater(diff_lon, 0.00001)

    def test_calculate_step_lat_lon(self):
        """
        Taking steps from start point toward end point brings one close to end point.
        (repeated with 10 random target points)
        """
        for i in range(10):
            # move 10 meters (0.01 km) per 'step'
            step_distance = 0.01
            # the complete 'trip' is to be at most 5km
            max_move_distance = 5
            # select random point within 5km distance from starting point
            end_point = random_point(max_move_distance, UPPSALA_GEO['center_lat'], UPPSALA_GEO['center_lon'])
            step_lat, step_lon = calculate_step_lat_lon(
                UPPSALA_GEO['center_lat'],
                UPPSALA_GEO['center_lon'],
                end_point[0],
                end_point[1],
                step_distance
            )
            move_distance = calculate_geo_distance(
                UPPSALA_GEO['center_lat'],
                UPPSALA_GEO['center_lon'],
                end_point[0],
                end_point[1]
            )
            # calculate number of steps that should be needed to move from start
            # to end point
            num_steps = ceil(move_distance / step_distance)
            post_stepping_point = (
                UPPSALA_GEO['center_lat'] + num_steps * step_lat,
                UPPSALA_GEO['center_lon'] + num_steps * step_lon
            )
            # calculate distance between where we actually ended up and the
            # intended target/end point
            dist_finish_target = calculate_geo_distance(
                post_stepping_point[0],
                post_stepping_point[1],
                end_point[0],
                end_point[1]
            )
            # if the distance is less than three 'steps', we'll consider the function
            # to work well enough
            self.assertLessEqual(dist_finish_target, 3 * step_distance)
