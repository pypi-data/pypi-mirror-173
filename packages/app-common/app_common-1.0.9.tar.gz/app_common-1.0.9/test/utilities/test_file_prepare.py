import os
import shutil
import unittest
from app_common.utilities.file_prepare import check_create_dir


class TestFilePrepare(unittest.TestCase):
    def setUp(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "output")

    def test_check_create_dir(self):
        # test create a dir in output file, and the file doesn't exist
        os.mkdir(self.output_dir)
        target_dir = os.path.join(self.output_dir, "test_dir")
        self.assertFalse(os.path.isdir(target_dir))
        check_create_dir(target_dir)
        self.assertTrue(target_dir)

    def test_create_dir_with_exist_dir(self):
        # test create a dir in output file, while the file already exist. it should do nothing
        os.mkdir(self.output_dir)
        target_dir = os.path.join(self.output_dir, "test_dir")
        os.mkdir(target_dir)
        self.assertTrue(os.path.isdir(target_dir))
        check_create_dir(target_dir)

    def test_create_dir_missing_root_dir(self):
        # test create a dir but root parent folder is not exist. it should raise a error
        target_dir = os.path.join(self.output_dir, "test_dir")
        try:
            check_create_dir(target_dir)
        except FileNotFoundError as e:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_create_dir_recursively_missing_root_dir(self):
        # test create a dir recursively but root parent folder is not exist, it should not raise a error
        target_dir = os.path.join(self.output_dir, "test_dir")
        try:
            check_create_dir(target_dir, True)
        except FileNotFoundError as e:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_create_dir_but_have_a_file_with_same_name(self):
        # it should raise a error and do nothing
        os.mkdir(self.output_dir)
        target_dir = os.path.join(self.output_dir, "test_dir")
        with open(target_dir, "w") as f:
            f.write("s")
        try:
            check_create_dir(target_dir)
        except FileExistsError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def tearDown(self):
        if os.path.isdir(self.output_dir) or os.path.isfile(self.output_dir):
            shutil.rmtree(self.output_dir)
