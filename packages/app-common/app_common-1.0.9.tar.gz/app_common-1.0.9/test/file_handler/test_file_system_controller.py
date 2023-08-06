import os
import unittest
import getpass
from .common_mock import DummyMockPxssh
from app_common.linux_file_handler.file_system_controller import (LocalLinuxFileSystemController,
                                                                  RemoteLinuxFileSystemController)
from app_common.test_common.base import TestBase
from app_common.linux_file_handler.remote_server_connector import RemoteServer


def example_test_fun1(a):
    return a + "_decorated"


class TestLinuxFileSystemController(unittest.TestCase):
    def setUp(self):
        self.file_controller = LocalLinuxFileSystemController()

    def test_send_decorator(self):
        """
        Test the send_decorator
        the decorator would save the function output to the un_commit_list
        :return:
        """

        decorated_func = self.file_controller.send_decorate(example_test_fun1)
        test_res = decorated_func('ls')
        res = self.file_controller._un_commit_list
        expected_res = 'ls_decorated'
        expected_res_list = [expected_res]
        self.assertEqual(test_res, expected_res)
        self.assertEqual(res, expected_res_list)

    def test_send_command_from_wrapped_commands(self):
        dir1 = "/usr/a"
        dir2 = "/usr/b"
        expect_value1 = 'mkdir -p ' + dir1
        expect_value2 = 'mkdir -p ' + dir2
        res = self.file_controller.make_directory(dir1)
        res_from_un_commit_list = self.file_controller._un_commit_list
        self.assertEqual(expect_value1, res)
        self.assertEqual([expect_value1], res_from_un_commit_list)
        self.file_controller.make_directory(dir2)
        self.assertEqual([expect_value1, expect_value2], res_from_un_commit_list)

    def test_get_result(self):
        self.assertEqual([], self.file_controller.get_result())


class TestLocalLinuxFileSystemController(TestBase):
    def setUp(self):
        self.base_setup()
        self.file_controller = LocalLinuxFileSystemController()

    def test_commit_command_for_list_file_and_create_file(self):
        # create a file named `test` under output dir. test if the test is created, and can it be listed
        create_file_name = "test"
        file_path = os.path.join(self.output_dir, create_file_name)
        self.file_controller.create_file(file_path)
        self.file_controller.list_files(self.output_dir)
        self.file_controller.commit()
        self.assertEqual([b'test\n'], self.file_controller._result_cache[1][0])
        self.assertTrue(os.path.isfile(file_path))

    def test_commit_command_for_make_directory(self):
        # create a dir under output dir. test 1. is it created 2. it should not do anything if the file already exist.3. it should
        # save the error in the cache if it already a file with same name exist.
        create_folder_name = "test"
        folder_path = os.path.join(self.output_dir, create_folder_name)
        self.file_controller.make_directory(folder_path)
        self.file_controller.commit()
        self.assertEqual(0, self.file_controller.get_result()[0][1])
        self.assertTrue(os.path.isdir(folder_path))
        try:
            self.file_controller.commit()
        except Exception:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

        create_file_and_folder_name = "test2"
        file_or_folder_path2 = os.path.join(self.output_dir, create_file_and_folder_name)
        self.file_controller.create_file(file_or_folder_path2)
        self.file_controller.commit()
        self.assertEqual(0, self.file_controller.get_result()[0][1])
        self.file_controller.make_directory(file_or_folder_path2)
        self.file_controller.commit()
        self.assertEqual(1, self.file_controller.get_result()[0][1])

    def test_commit_command_for_change_directory(self):
        """
        send multiple commands and test change directory command
        """
        # create a test file first
        create_dir_name = "test"
        folder_path = os.path.join(self.output_dir, create_dir_name)
        create_file_name = "test.txt"
        file_path = os.path.join(folder_path, create_file_name)
        self.file_controller.make_directory(folder_path)
        self.file_controller.list_files()
        self.file_controller.change_directory(folder_path)
        self.file_controller.create_file(file_path)
        self.file_controller.list_files()
        self.file_controller.commit(parallel=False)
        result = self.file_controller.get_result()
        # test if the command finished successfully
        self.assertEqual(0, self.file_controller.get_result()[0][1])
        res = self.file_controller.get_result()[0][0]
        self.assertTrue(b'test.txt\n' in res)

    def test_commit_command_for_remove_files(self):
        create_file_name = "test.txt"
        file_path = os.path.join(self.output_dir, create_file_name)
        self.file_controller.create_file(file_path)
        self.file_controller.commit()
        self.file_controller.list_files(self.output_dir)
        self.file_controller.commit()
        self.assertEqual([b'test.txt\n'], self.file_controller.get_result()[0][0])
        self.file_controller.remove_file(file_path)
        self.file_controller.commit()
        self.file_controller.list_files(self.output_dir)
        self.file_controller.commit()
        self.assertEqual([], self.file_controller.get_result()[0][0])

    def test_commit_command_for_whoami(self):
        self.file_controller.whoami()
        self.file_controller.commit()
        res = self.file_controller.get_result()
        username = getpass.getuser()
        self.assertTrue(username in str(res[0][0]))

    def test_commit_command_for_current_path(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.file_controller.change_directory(current_path)
        self.file_controller.current_path()
        self.file_controller.commit(parallel=False)
        res = self.file_controller.get_result()
        self.assertTrue(current_path in str(res[0][0]))

    # def test_compress_dir(self):
    #     """ create a file first and then compress it
    #     """
    #     # first test compress a dir
    #     dir_name = "test"
    #     dir_path = os.path.join(self.output_dir, dir_name)
    #     res_name = "test.bar.gz"
    #     res_path = os.path.join(self.output_dir, res_name)
    #     os.mkdir(dir_path)
    #     self.file_controller.compress_files(dir_path, self.output_dir, res_name)
    #     self.file_controller.commit()
    #     self.assertTrue(os.path.isfile(res_path))
    #     # second test compress a list of dirs
    #     file_name1 = "sample1.txt"
    #     file_name2 = "sample2.txt"
    #     file_name3 = "sample3.txt"
    #     file_name_list = [file_name1, file_name2, file_name3]
    #     file_path_list = []
    #     res_name2 = "test2.bar.gz"
    #     res_path2 = os.path.join(self.output_dir, res_name2)
    #     for x in file_name_list:
    #         file_path_list.append(os.path.join(self.output_dir, x))
    #     self.file_controller.compress_files(file_name_list, self.output_dir, res_name2)
    #     self.file_controller.commit()
    #     self.assertTrue(os.path.isfile(res_path2))

    def test_make_soft_link(self):
        """
         First create a file and a directory
         create a soft link to the file under the directory
         """
        # first test compress a dir
        dir_name = "test"
        dir_path = os.path.join(self.output_dir, dir_name)
        os.mkdir(dir_path)
        file_name = "sample.txt"
        file_path = os.path.join(self.output_dir, file_name)
        with open(file_path, 'w') as f:
            f.write("test")
        new_file_name = "sample2.txt"
        self.file_controller.make_soft_link(file_path, dir_path, new_file_name)
        self.file_controller.commit()
        self.assertTrue(os.path.isfile(file_path))
        self.assertTrue(os.path.isfile(os.path.join(*[dir_path, new_file_name])))

    def test_copy_file(self):
        dir_name = "test"
        dir_path = os.path.join(self.output_dir, dir_name)
        os.mkdir(dir_path)
        file_name = "sample.txt"
        file_path = os.path.join(self.output_dir, file_name)
        with open(file_path, 'w') as f:
            f.write("test")
        new_file_name = "sample2.txt"
        self.file_controller.copy_file(file_path, dir_path, new_file_name)
        self.file_controller.commit()
        self.assertTrue(os.path.isfile(file_path))
        self.assertTrue(os.path.isfile(os.path.join(*[dir_path, new_file_name])))

    def test_send_command_from_wrapped_commands(self):
        dir1 = "/usr/a"
        dir2 = "/usr/b"
        expect_value1 = 'mkdir -p ' + dir1
        expect_value2 = 'mkdir -p ' + dir2
        res = self.file_controller.make_directory(dir1)
        res_from_un_commit_list = self.file_controller._un_commit_list
        self.assertEqual(expect_value1, res)
        self.assertEqual([expect_value1], res_from_un_commit_list)
        self.file_controller.make_directory(dir2)
        self.assertEqual([expect_value1, expect_value2], res_from_un_commit_list)

    def tearDown(self):
        self.clear_up()


class TestLinuxRemoteFileSystemController(unittest.TestCase):
    def setUp(self):
        RemoteServer.pxssh_session = DummyMockPxssh()
        RemoteLinuxFileSystemController.RemoteServerClass = RemoteServer
        self.file_controller = RemoteLinuxFileSystemController("test_host", "the_user")

    def test_commit(self):
        self.file_controller._un_commit_list = ["a", "b"]
        self.file_controller.commit()
        self.assertEqual([None, None], self.file_controller.get_result())
        self.assertEqual([], self.file_controller._un_commit_list)
