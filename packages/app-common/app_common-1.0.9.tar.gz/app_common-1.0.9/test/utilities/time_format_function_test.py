import unittest
from app_common.utilities import convert_to_erddap_time_format, time_zone_replace, str_to_timeobj, time_to_str
from app_common.utilities.time_format_functions import time_period_overlap


class TimeFormatFunctionTest(unittest.TestCase):
    def setUp(self):
        self.time1 = "2019-03-12 14:55:02"
        self.errdap_time1 = "2019-03-12T14:55:02Z"

        self.start_time1 = "2019-03-12 14:55:02"
        self.start_time2 = "2020-09-12 14:55:02"
        self.start_time3 = "2019-03-12 14:55:02"
        self.end_time1 = "2020-03-12 14:55:02"
        self.end_time2 = "2021-03-12 14:55:02"
        self.end_time3 = "2020-04-12 14:55:02"

    def test_convert_to_erddap_time_format(self):
        self.assertEqual(convert_to_erddap_time_format(self.time1), self.errdap_time1)

    def test_time_zone_replace(self):
        time_1 = time_zone_replace(self.time1)
        self.assertEqual(time_1.tzinfo.zone, 'UTC')

    def test_time_str_convert_function(self):
        time_obj = str_to_timeobj(self.time1)
        time_str = time_to_str(time_obj)
        self.assertEqual(time_str, self.time1)

    # test time_period_overlap
    def test_time_period_overlap_identical(self):
        self.assertTrue(time_period_overlap(str_to_timeobj(self.start_time1), str_to_timeobj(self.end_time1),
                                            str_to_timeobj(self.start_time1), str_to_timeobj(self.end_time1)))

    def test_time_period_overlap_no_overlap(self):
        self.assertFalse(time_period_overlap(str_to_timeobj(self.start_time1), str_to_timeobj(self.end_time1),
                                             str_to_timeobj(self.start_time2), str_to_timeobj(self.end_time2)))
        self.assertFalse(time_period_overlap(str_to_timeobj(self.start_time2), str_to_timeobj(self.end_time2),
                                             str_to_timeobj(self.start_time1), str_to_timeobj(self.end_time1)))

    def test_time_period_overlap_left_overlap(self):
        self.assertTrue(time_period_overlap(str_to_timeobj(self.start_time1), None, str_to_timeobj(self.start_time2),
                                            str_to_timeobj(self.end_time2)))
        self.assertFalse(time_period_overlap(str_to_timeobj(self.start_time1), str_to_timeobj(self.end_time3),
                                             str_to_timeobj(self.start_time2), str_to_timeobj(self.end_time2)))
        self.assertTrue(time_period_overlap(str_to_timeobj(self.start_time1), None, str_to_timeobj(self.start_time2),
                                            None))

    def test_time_period_overlap_right_overlap(self):
        self.assertTrue(time_period_overlap(str_to_timeobj(self.start_time2),
                                            str_to_timeobj(self.end_time2), str_to_timeobj(self.start_time1), None))
        self.assertFalse(time_period_overlap(str_to_timeobj(self.start_time2), str_to_timeobj(self.end_time2),
                                             str_to_timeobj(self.start_time1), str_to_timeobj(self.end_time3)))
        self.assertTrue(
            time_period_overlap(str_to_timeobj(self.start_time2), None, str_to_timeobj(self.start_time1), None))

    def test_time_period_overlap_value_error(self):
        try:
            time_period_overlap(None,
                                None, None, None)
        except ValueError as e:
            self.assertEqual(type(ValueError()), type(e))

