from unittest import TestCase
from app_common.utilities import simplified_float


class TestGPSPointTools(TestCase):
    def test_gps_point_tool(self):
        test_point = 42.113
        res = simplified_float(test_point, 3)
        print(res)
