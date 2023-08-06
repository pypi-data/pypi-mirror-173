import unittest
from app_common.utilities.dataset_id_generate_function import IDGenerator


class DatasetIDGenerateFunctionTest(unittest.TestCase):
    def setUp(self):
        self.slocum_input1 = {"platform_name": "Fundy", "start_time": "2018-05-17 16:02:26", "deployment_number": "83",
                              "test": False, "mode": False}
        self.slocum_input2 = {"platform_name": "dal556", "start_time": "2018-10-23 19:50:45", "deployment_number": "93",
                              "test": False, "mode": True}
        self.slocum_input3 = {"platform_name": "dal556", "start_time": "2018-10-23 19:50:45", "deployment_number": "93",
                              "test": True, "mode": True}
        self.wave_input1 = {"platform_name": "DL", "start_time": "2017-05-29 18:40:00", "deployment_number": "72",
                            "test": False}
        self.wave_input2 = {"platform_name": "DL", "start_time": "2015-11-29 11:39:00", "deployment_number": "54",
                            "test": False}
        self.wave_input3 = {"platform_name": "DL", "start_time": "2015-11-29 11:39:00", "deployment_number": "54",
                            "test": True}

    def test_slocum_id_generate(self):
        slocum_id1 = IDGenerator.generate_id(IDGenerator.GLIDER, **self.slocum_input1)
        slocum_id2 = IDGenerator.generate_id(IDGenerator.GLIDER, **self.slocum_input2)
        slocum_id3 = IDGenerator.generate_id(IDGenerator.GLIDER, **self.slocum_input3)
        expect_id_1 = "Fundy_20180517_83_delayed"
        expect_id_2 = "dal556_20181023_93_realtime"
        expect_id_3 = "dal556_20181023_93_realtime_test"

        self.assertEqual(expect_id_1, slocum_id1)
        self.assertEqual(expect_id_2, slocum_id2)
        self.assertEqual(expect_id_3, slocum_id3)
