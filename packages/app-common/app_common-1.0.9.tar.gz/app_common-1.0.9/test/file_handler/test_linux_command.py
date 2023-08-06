import unittest
import os
from app_common.linux_file_handler.linux_command import LinuxCommand


class TestLinuxCommand(unittest.TestCase):
    def setUp(self):
        self.linux_commands = LinuxCommand()
        self.target_dir1 = "/usr/a/b"
        self.target_dir2 = "/usr/a/c"
        self.target_dir3 = ["/usr/a/c", "/usr/a/d"]

        self.user = "test_user"
        self.host = "test_host"

    """
    testing mkdir command
    """

    def test_make_dir(self):
        expect_res = "mkdir -p " + self.target_dir1
        self.assertEqual(expect_res, self.linux_commands.make_directory(self.target_dir1))

    """
    testing ls command
    """

    def test_list_files(self):
        expect_res = "ls " + self.target_dir1
        self.assertEqual(expect_res, self.linux_commands.list_files(self.target_dir1))
        expect_res = "ls"
        self.assertEqual(expect_res, self.linux_commands.list_files())

    """
    testing mv command
    """

    def test_change_directory(self):
        expect_res = "cd " + self.target_dir1
        self.assertEqual(expect_res, self.linux_commands.change_directory(self.target_dir1))

    """
    testing mv command
    """

    def test_move_files(self):
        target_path = "/usr/a/c"
        expect_res = "mv " + self.target_dir1 + " " + target_path
        self.assertEqual(expect_res, self.linux_commands.move_files(self.target_dir1, target_path))

    """
    testing rm command
    """

    def test_remove_files(self):
        expect_res = "rm " + self.target_dir1
        self.assertEqual(expect_res, self.linux_commands.remove_file(self.target_dir1))

    """
    test whoami command
    """

    def test_whoami(self):
        expect_res = "whoami"
        self.assertEqual(expect_res, self.linux_commands.whoami())

    """
    test scp files command
    """

    def test_scp(self):
        expect1 = "scp -p para1 para2"
        expect2 = "scp para1 para2"
        self.assertEqual(expect1, self.linux_commands.scp("para1", "para2", "-p"))
        self.assertEqual(expect2, self.linux_commands.scp("para1", "para2"))

    """
    test scp file command
    """

    def test_scp_file(self):
        expect1 = "scp {} {}:{}".format(self.target_dir1, "{}@{}".format(self.user, self.host), self.target_dir2)
        self.assertEqual(expect1,
                         self.linux_commands.scp_file(self.target_dir1, self.target_dir2, self.user, self.host))
        expect1 = "scp -r {} {}:{}".format(self.target_dir1, "{}@{}".format(self.user, self.host), self.target_dir2)
        self.assertEqual(expect1,
                         self.linux_commands.scp_file(self.target_dir1, self.target_dir2, self.user, self.host,
                                                      folder=True))
        expect3 = "scp {}:{} {}".format("{}@{}".format(self.user, self.host), self.target_dir1, self.target_dir2)
        self.assertEqual(expect3,
                         self.linux_commands.scp_file(self.target_dir1, self.target_dir2, self.user, self.host,
                                                      upload=False))
        expect4 = "scp -r {}:{} {}".format("{}@{}".format(self.user, self.host), self.target_dir1, self.target_dir2)
        self.assertEqual(expect4,
                         self.linux_commands.scp_file(self.target_dir1, self.target_dir2, self.user, self.host,
                                                      folder=True, upload=False))

    """
    Test Compress file command
    """

    # def test_compress_file1(self):
    #     """test compress a file with no dst_dir
    #     """
    #     test_file_name = "/test/file/name/file_name.txt"
    #     test_dst_file_dir = "test/dst/dir/"
    #     test_dst_file_name = "dst_file_name.tar"
    #     expected_command1 = "tar -cjvf {} {}".format(test_file_name, os.path.join(test_dst_file_dir, test_dst_file_name))
    #     res1 = LinuxCommand.compress_files(test_file_name, test_dst_file_dir, test_dst_file_name)
    #     self.assertEqual(expected_command1, res1)

    # def test_compress_file2(self):
    #     """ test compress a one list with one file with dst_dir and dst_name
    #     """
    #     test_dst_file_name = "test/dst/dir/dst_file_name.tar"
    #     test_file_list1 = ["/test/file/name/file_name.txt"]
    #     expected_command2 = "tar -cjvf {} {}".format(test_dst_file_name, "/test/file/name/file_name.txt")
    #     res2 = LinuxCommand.compress_files(test_file_list1, test_dst_file_name)
    #     self.assertEqual(expected_command2.strip(), res2.strip())
    #
    # def test_compress_file3(self):
    #     """test compress a one list with two file with dst_dir and dst_name
    #     """
    #     test_dst_file_name = "test/dst/dir/dst_file_name.tar"
    #     test_file_list = ["/test/file/name/file_name.txt", "/test/file/name/file_name.txt2"]
    #     expected_command = "tar -cjvf {} {}".format(test_dst_file_name,
    #                                                 "/test/file/name/file_name.txt /test/file/name/file_name.txt2")
    #     res = LinuxCommand.compress_files(test_file_list, test_dst_file_name)
    #     self.assertEqual(expected_command.strip(), res.strip())
    #
    # def test_compress_file4(self):
    #     """test compress a one list with no file with dst_dir and dst_name
    #     """
    #     test_dst_file_name = "test/dst/dir/dst_file_name.tar"
    #     test_file_list4 = []
    #     expected_command4 = "tar -cjvf {} {}".format(test_dst_file_name,
    #                                                  " ")
    #     res4 = LinuxCommand.compress_files(test_file_list4, test_dst_file_name)
    #     self.assertEqual(expected_command4.strip(), res4.strip())
    #
    # def test_compress_file5(self):
    #     """Test given invalid file name
    #         It should raise Attribute error since It is not suppose to
    #     """
    #     test_file_list4 = 1
    #     test_dst_file_name = "test/dst/dir/dst_file_name.tar"
    #     try:
    #         LinuxCommand.compress_files(test_file_list4, 1)
    #     except AttributeError:
    #         self.assertTrue(True)
    #     else:
    #         self.assertTrue(False)

    """
    Test uncompress command
    """

    # def test_uncompress_file_with_path_to_extract_dir(self):
    #     """Test uncompress files Linux command
    #     """
    #     path_to_extract_dir = "/usr/file/"
    #     target_file = "/path/to/target/compress_file"
    #     expected_command = "tar -xzvf {} -C {}".format(target_file, path_to_extract_dir)
    #     res_command = LinuxCommand.uncompress_files(target_file, path_to_extract_dir)
    #     self.assertEqual(res_command, expected_command)
    #
    # def test_uncompress_file_with_no_path_to_extract_dir(self):
    #     target_file = "/path/to/target/compress_file"
    #     expected_command = "tar -xzvf {}".format(target_file)
    #     res_command = LinuxCommand.uncompress_files(target_file)
    #     self.assertEqual(res_command.strip(), expected_command.strip())

    """
    copy file
    """

    # def test_copy_file_command_scr_path_is_dir(self):
    #     src_path = "/data/path/"
    #     dst_dir = "/dst/dir/"
    #     expected_command = "cp -R {} {}".format(src_path, dst_dir)
    #     self.assertEqual(expected_command.strip(), LinuxCommand.copy_file(src_path, dst_dir))

    def test_copy_file_command_scr_path_is_file_path(self):
        src_path = "/data/path/file.txt"
        dst_dir = "/dst/dir/"
        expected_command = "cp {} {}".format(src_path, "/dst/dir/file.txt")
        self.assertEqual(expected_command.strip(), LinuxCommand.copy_file(src_path, dst_dir).strip())

    """
    make soft link
    """

    def test_make_soft_link_for_a_folder(self):
        src_path = "/data/path/"
        dst_dir = "/dst/dir/"
        expected_command = "ln -s {} {}".format(src_path, dst_dir)
        self.assertEqual(expected_command, LinuxCommand.make_soft_link(src_path, dst_dir))

    def test_make_soft_link_with_a_file_path(self):
        src_path = "/data/path/path.txt"
        dst_dir = "/dst/dir/"
        expected_command = "ln -s {} {}".format(src_path, "/dst/dir/path.txt")
        self.assertEqual(expected_command, LinuxCommand.make_soft_link(src_path, dst_dir))
