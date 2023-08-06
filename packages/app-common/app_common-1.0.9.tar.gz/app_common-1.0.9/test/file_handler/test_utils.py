import os
from app_common.linux_file_handler.utils import (
    get_files,
    convert_list_to_str,
    path_complement,
    WrapperProxy
)
from app_common.test_common.base import TestBase


class TestLocalLinuxFileSystemController(TestBase):
    def setUp(self):
        self.base_setup()

    def test_get_files(self):
        test_file_name = "text_file.txt"
        test_file_name_path = os.path.join(self.output_dir, test_file_name)
        res = get_files(self.output_dir)
        self.assertEqual([], res)
        with open(test_file_name_path, 'w') as f:
            f.write("something")
        res2 = get_files(self.output_dir)
        self.assertEqual([test_file_name_path], res2)

    def test_path_complement(self):
        test_name1 = "/a/b"
        expected_path = "/a/b"
        self.assertEqual(expected_path, path_complement(test_name1))
        test_nam2 = "a"
        expected_path2 = "/a"
        self.assertEqual(expected_path2, path_complement(test_nam2))
        test_folder_name = "/a/b"
        expected_folder = "/a/b/"
        self.assertEqual(expected_folder, path_complement(test_folder_name, folder=True))

    def test_convert_list_to_str(self):
        test_list = ["test1", "test2", "test3"]
        expected_str = "/test1 /test2 /test3"
        res = convert_list_to_str(test_list)
        self.assertEqual(expected_str.strip(), res.strip())

    def test_wrapper_proxy(self):
        class DummyWrappedClass:
            def __init__(self):
                self.test_variable = 1
                self._test_private_variable = 2

            def public_method(self):
                return 3

            def _private_method(self):
                return 4

        dummy_wrapped_obj = DummyWrappedClass()

        class DummyClass(WrapperProxy):
            def __init__(self):
                super().__init__()

            def _setup(self):
                return dummy_wrapped_obj

        test_obj = DummyClass()
        self.assertEqual(dummy_wrapped_obj.test_variable, test_obj.test_variable)
        self.assertEqual(dummy_wrapped_obj.public_method(), test_obj.public_method())

        try:
            test_obj._test_private_variable
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            test_obj._private_method()
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            test_obj.no_exist_variable
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            test_obj.no_exist_method()
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def tearDown(self):
        self.clear_up()
