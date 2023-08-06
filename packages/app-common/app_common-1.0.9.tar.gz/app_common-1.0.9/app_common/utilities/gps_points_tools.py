import math


# ------------------------------------------------------------------------------+
#
#   Nathan A. Rooy
#   Haversine Formula
#   June, 2016
#
# ------------------------------------------------------------------------------+

class Haversine:
    """
    use the haversine class to calculate the distance between
    two lon/lat coordnate pairs.
    output distance available in kilometers, meters, miles, and feet.
    example usage: Haversine([lon1,lat1],[lon2,lat2]).feet
    """

    def __init__(self):
        self.R = 6371000  # radius of Earth in meters

    def get_distance(self, coord1, coord2):
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        phi_1 = math.radians(lat1)
        phi_2 = math.radians(lat2)

        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + \
            math.cos(phi_1) * math.cos(phi_2) * \
            math.sin(delta_lambda / 2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        meters = self.R * c  # output distance in meters
        km = meters / 1000.0  # output distance in kilometers
        return km


def gps_point_range_check(point):
    lat = point[0]
    lng = point[1]
    if -90.0 < lat < 90.0 and -180.0 < lng < 180.0:
        return True
    return False


def simplified_float(number, keep_digit):
    """
    A function which can round the float (it is faster than round())

    """
    keep_digit = 10 ** keep_digit
    keep_digit = keep_digit / 100
    number = float(number)
    if number:
        number = number * keep_digit
        number = int(number)
        number = float(number) / keep_digit
    return number
