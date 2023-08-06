import os
import getpass
import time
from app_common.test_common.base import TestBase
from app_common.linux_file_handler.file_system_manager import FileSystemManager


class TestFileSystemManager(TestBase):

    def setUp(self):
        self.base_setup()
        self.fsm = FileSystemManager()
        self.fsm.load("bugs.ocean.dal.ca", "slocum", controller_tag="slocum")

    def test_make_directory(self):
        folder_name = "test_folder"
        folder_path = os.path.join(self.output_dir, folder_name)
        self.fsm.local.make_directory(folder_path)
        self.fsm.local.commit()
        self.assertTrue(os.path.isdir(folder_path))

    def test_local_linux_handler_to_create_file(self):
        file_name = "random.txt"
        file_path = os.path.join(self.output_dir, file_name)
        self.fsm.local.create_file(file_path)
        self.fsm.local.commit()
        self.assertTrue(os.path.isfile(file_path))

    def test_local_linux_list_files(self):
        file_name = "random.txt"
        file_path = os.path.join(self.output_dir, file_name)
        self.fsm.local.create_file(file_path)
        self.fsm.local.commit()
        self.fsm.local.list_files(self.output_dir)
        self.fsm.local.commit()
        res = self.fsm.local.get_result()[0]
        self.assertTrue(file_name in str(res))

    def test_local_move_files(self):
        file_name = "test.txt"
        new_file_name = "new_test.txt"
        file_path = os.path.join(self.output_dir, file_name)
        new_file_path = os.path.join(self.output_dir, new_file_name)
        self.fsm.local.create_file(file_path)
        self.fsm.local.commit()
        self.assertTrue(os.path.isfile(file_path))
        self.fsm.local.move_files(file_path, new_file_path)
        self.fsm.local.commit()
        self.assertTrue(os.path.isfile(new_file_path))

    def test_remove_file(self):
        file_name = "test.txt"
        file_path = os.path.join(self.output_dir, file_name)
        self.fsm.local.create_file(file_path)
        self.fsm.local.commit()
        self.assertTrue(os.path.isfile(file_path))
        self.fsm.local.remove_file(file_path)
        self.fsm.local.commit()
        self.assertTrue(not os.path.isfile(file_path))

    def test_bash_script(self):
        test_bash = """#!/usr/bin/env bash
NAME="John"
echo "Hello $NAME!"
"""
        expect_output = "Hello John"
        file_name = "test.txt"
        file_path = os.path.join(self.output_dir, file_name)
        with open(file_path, 'w') as f:
            f.write(test_bash)
        self.fsm.local.bash_script(test_bash)
        self.fsm.local.commit()
        res = str(self.fsm.local.get_result()[0])
        self.assertTrue(expect_output in res)

    def test_whoami(self):
        user_name = getpass.getuser()
        self.fsm.local.whoami()
        self.fsm.local.commit()
        res = str(self.fsm.local.get_result()[0])
        self.assertTrue(user_name in res)

    def test_get_current_path(self):
        dirpath = os.getcwd()
        self.fsm.local.current_path()
        self.fsm.local.commit()
        res = str(self.fsm.local.get_result()[0])
        self.assertTrue(dirpath in res)

    def test_copy_files(self):
        folder_name = "test_folder"
        folder_path = os.path.join(self.output_dir, folder_name)
        self.fsm.local.make_directory(folder_path)
        file_name = "test.txt"
        file_path = os.path.join(self.output_dir, file_name)
        self.fsm.local.create_file(file_path)
        self.fsm.local.commit()
        time.sleep(1)
        self.fsm.local.copy_file(file_path, folder_path)
        self.fsm.local.commit()
        new_place_file = os.path.join(folder_path, file_name)
        self.assertTrue(os.path.isfile(new_place_file))
        new_file_name = "new_test.txt"
        self.fsm.local.copy_file(file_path, folder_path, new_file_name)
        self.fsm.local.commit()
        new_soft_file_path = os.path.join(folder_path, new_file_name)
        self.assertTrue(os.path.isfile(new_soft_file_path))

    def test_make_soft_link(self):
        folder_name = "test_folder"
        folder_path = os.path.join(self.output_dir, folder_name)
        self.fsm.local.make_directory(folder_path)
        file_name = "test.txt"
        file_path = os.path.join(self.output_dir, file_name)
        self.fsm.local.create_file(file_path)
        self.fsm.local.commit()
        time.sleep(1)
        self.fsm.local.make_soft_link(file_path, folder_path)
        self.fsm.local.commit()
        new_place_file = os.path.join(folder_path, file_name)
        self.assertTrue(os.path.isfile(new_place_file))
        new_file_name = "new_test.txt"
        self.fsm.local.make_soft_link(file_path, folder_path, new_file_name)
        self.fsm.local.commit()
        new_soft_file_path = os.path.join(folder_path, new_file_name)
        self.assertTrue(os.path.isfile(new_soft_file_path))

    def tearDown(self):
        self.clear_up()
