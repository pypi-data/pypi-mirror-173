import os
from app_common.test_common.base import TestBase


class TestLiberdadeTestCase(TestBase):
    def setUp(self):
        self.expect_output_dir = os.path.join(os.path.dirname(__file__), "output")
        self.expect_resource_dir = os.path.join(os.path.dirname(__file__), "resource")

    def test_base_setup(self):
        # test to see if 1st create output and resource dir
        self.base_setup()
        self.assertTrue(os.path.isdir(self.expect_output_dir))
        self.assertTrue(os.path.isdir(self.expect_resource_dir))
        self.assertEqual(self.expect_output_dir, self.output_dir)
        self.assertEqual(self.expect_resource_dir, self.resource_dir)
        self.clear_up()

    def test_clean_up(self):
        self.base_setup()
        self.output_file_path = os.path.join(self.output_dir, 'output_file.txt')
        with open(self.output_file_path, 'w') as f:
            f.write('something')
        self.assertTrue(os.path.isfile(self.output_file_path))
        self.clear_up()
        self.assertTrue(not os.path.isfile(self.output_file_path))
