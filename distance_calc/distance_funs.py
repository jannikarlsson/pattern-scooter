"""
Functions for doing distance calculations based on latitudes/longitudes.

Most of this is based on formulas from:
https://www.movable-type.co.uk/scripts/latlong.html
"""
import random

from .distance_constants import (
    EARTH_RADIUS_KM,
    LUND_GEO,
    SKOVDE_GEO,
    UPPSALA_GEO
)

from math import sin, asin, cos, pi, atan2

def deg_to_rad(deg):
    """[summary]

    Args:
        deg (float): Angle in degrees
    
    Returns:
        float: Angle in radians
    """
    return deg / 180 * pi

def calculate_bearing(start_lat, start_lon, end_lat, end_lon):
    """Calculates (initial) bearing from geological start to end point.
    This 'initial' bearing should be a good enough approximation for
    setting bearing of a whole trip if the distance to be travelled is only
    on the order of a few kilometers.

    Args:
        start_lat (float): Start latitude (in degrees)
        start_lon (float): Start longitude (in degrees)
        end_lat (float): End latitude (in degrees)
        end_lon (float): End longitude (in degrees)

    Returns:
        float: Bearing (in radians)
    """
    start_lat_r, start_lon_r = deg_to_rad(start_lat), deg_to_rad(start_lon)
    end_lat_r, end_lon_r = deg_to_rad(end_lat), deg_to_rad(end_lon)
    d_lon_r = end_lon_r - start_lon_r
    y = sin(d_lon_r) * cos(end_lat_r)
    x = cos(start_lat_r) * sin(end_lat_r) - sin(start_lat_r) * cos(end_lat_r) * cos(d_lon_r)
    theta = atan2(y, x)
    bearing = (theta + 2 * pi) % (2 * pi)
    return bearing

def move_lat_lon(start_lat, start_lon, move_dist, bearing_angle):
    """Takes in a start latitude/longitude and a distance and angle of direction to
    'move' in. Returns the latitude/longitude that one would end up at given the
    direction.

    Args:
        start_lat (float): Start latitude (in degrees)
        start_lon (float): Start longitude (in degrees)
        move_dist (float): Distance to 'move' (in kilometers)
        bearing_angle (float): Angle to 'move' in (in radians)
    Returns:
        float[]: 2-element tuple holding 'post-move' latitude and longitude
    """
    d = move_dist/EARTH_RADIUS_KM
    start_lat_r, start_lon_r = deg_to_rad(start_lat), deg_to_rad(start_lon)

    lat_radians = asin(sin(start_lat_r)*cos(d)+cos(start_lat_r)*sin(d)*cos(bearing_angle))
    lon_radians = start_lon_r + atan2(
        sin(bearing_angle) * sin(d) * cos(start_lat_r),
        cos(d) - sin(start_lat_r) * sin(lat_radians)
    )
    end_lat_deg = lat_radians / pi * 180
    end_lon_deg = lon_radians / pi * 180
    return end_lat_deg, end_lon_deg

def calculate_step_lat_lon(start_lat, start_lon, end_target_lat, end_target_lon, step_distance):
    """Given a start point, a 'final target' point and a 'step distance' in kilometers,
    returns how large changes in latitude/longitude correspond to a single step in the direction
    from the start point toward the final target.

    Args:
        start_lat (float): Start latitude (in degrees)
        start_lon (float): Start longitude (in degrees)
        end_target_lat (float): End target latitude (in degrees)
        end_target_lon (float): End target longitude (in degrees)
        step_distance (float): Distance to move in each step (in kilometers)

    Returns:
        float[]: 2-element tuple holding the change in latitude and longitude (in degrees)
    """
    bearing = calculate_bearing(start_lat, start_lon, end_target_lat, end_target_lon)
    step_end_lat, step_end_lon = move_lat_lon(start_lat, start_lon, step_distance, bearing)
    delta_lat, delta_lon = (step_end_lat - start_lat), (step_end_lon - start_lon)
    return delta_lat, delta_lon

def calculate_geo_distance(start_lat, start_lon, end_lat, end_lon):
    """Given a start/end point, returns 'as-the-crow-flies' distance in kilometers,
    based on the Haversine formula.

    Args:
        start_lat (float): Start latitude (in degrees)
        start_lon (float): Start longitude (in degrees)
        end_lat (float): End latitude (in degrees)
        end_lon (float): End longitude (in degrees)

    Returns:
        float: Distance (in kilometers)
    """
    start_lat_r, start_lon_r = deg_to_rad(start_lat), deg_to_rad(start_lon)
    end_lat_r, end_lon_r = deg_to_rad(end_lat), deg_to_rad(end_lon)
    d_lat_r = end_lat_r - start_lat_r
    d_lon_r = end_lon_r - start_lon_r
    a = (
        sin(d_lat_r / 2)**2 +
        cos(start_lat_r) * cos(end_lat_r) *
        sin(d_lon_r / 2)**2
    )
    c = 2 * atan2(a**(1/2), (1-a)**(1/2))
    d_km = EARTH_RADIUS_KM * c
    return d_km

def random_point(radius, center_lat, center_lon):
    """Generate a random point within a certain radius from a center point.

    Args:
        radius (float): Maximum distance from center point (kilometers)
        center_lat (float): Center point latitude (degrees)
        center_lon (float): Center point longitude (degrees)

    Returns:
        float[]: 2-element tuple holding random point latitude and longitude
    """
    distance_centre_km = random.random() * radius
    # 'radial' degrees in radians
    bearing_angle = random.random() * 2 * pi
    return move_lat_lon(center_lat, center_lon, distance_centre_km, bearing_angle)

def random_p_lund():
    return random_point(**LUND_GEO)

def random_p_skovde():
    return random_point(**SKOVDE_GEO)

def random_p_uppsala():
    return random_point(**UPPSALA_GEO)
