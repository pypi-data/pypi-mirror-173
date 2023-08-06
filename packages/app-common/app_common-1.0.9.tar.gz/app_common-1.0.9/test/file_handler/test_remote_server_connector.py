from pexpect import pxssh
from test.file_handler.common_mock import DummyMockPxssh
from app_common.linux_file_handler.remote_server_connector import RemoteServer
from app_common.test_common.base import TestBase


class TestLocalLinuxFileSystemController(TestBase):
    def setUp(self):
        self.base_setup()

    def test_password_login(self):
        errors = []
        dummy_ssh = DummyMockPxssh()
        RemoteServer.pxssh_session = dummy_ssh
        server_obj = RemoteServer("user", "host", "test_password")
        server_obj._password_login(errors)
        res = dummy_ssh.res
        self.assertEqual(
            [((), {"username": "user", "server": "host", "password": "test_password"})],
            res)

    def test_password_free_login(self):
        errors = []
        dummy_ssh = DummyMockPxssh()
        RemoteServer.pxssh_session = dummy_ssh
        server_obj = RemoteServer("user", "host")
        server_obj._password_free_login(errors)
        res = dummy_ssh.res
        self.assertEqual(
            [((), {"username": "user", "server": "host"})],
            res)

    def test_password_login_with_raise(self):
        errors = []
        dummy_ssh = DummyMockPxssh(success=False)
        RemoteServer.pxssh_session = dummy_ssh
        server_obj = RemoteServer("user", "host", "test_password")
        server_obj._password_login(errors)
        res = dummy_ssh.res
        self.assertEqual(
            [((), {"username": "user", "server": "host", "password": "test_password"})],
            res)
        self.assertEqual(1, len(errors))
        self.assertEqual("connection fail", errors[0])

    def test_password_free_login_with_raise(self):
        errors = []
        dummy_ssh = DummyMockPxssh(success=False)
        RemoteServer.pxssh_session = dummy_ssh
        server_obj = RemoteServer("user", "host")
        server_obj._password_free_login(errors)
        res = dummy_ssh.res
        self.assertEqual(
            [((), {"username": "user", "server": "host"})],
            res)
        self.assertEqual(1, len(errors))
        self.assertEqual("connection fail", errors[0])

    def test_login_with_password(self):
        dummy_ssh = DummyMockPxssh()
        RemoteServer.pxssh_session = dummy_ssh
        server_obj = RemoteServer("user", "host")
        server_obj._login()
        res = dummy_ssh.res
        self.assertEqual(
            [((), {"username": "user", "server": "host"})],
            res)

    def test_login_without_password(self):
        dummy_ssh = DummyMockPxssh()
        RemoteServer.pxssh_session = dummy_ssh
        server_obj = RemoteServer("user", "host")
        server_obj._login()
        res = dummy_ssh.res
        self.assertEqual(
            [((), {"username": "user", "server": "host"})],
            res)

    def test_login_fail_without_password(self):
        dummy_ssh = DummyMockPxssh(success=False)
        RemoteServer.pxssh_session = dummy_ssh
        server_obj = RemoteServer("user", "host")
        try:
            server_obj._login()
        except pxssh.ExceptionPxssh as e:
            self.assertEqual(["connection fail"], e.value)

    def test_login_fail_with_password(self):
        dummy_ssh = DummyMockPxssh(success=False)
        RemoteServer.pxssh_session = dummy_ssh
        server_obj = RemoteServer("user", "host", "test_password")
        try:
            server_obj._login()
        except pxssh.ExceptionPxssh as e:
            self.assertEqual(["connection fail", "connection fail"], e.value)

    def test_with(self):
        dummy_ssh = DummyMockPxssh()
        RemoteServer.pxssh_session = dummy_ssh
        with RemoteServer("user", "host"):
            ...
        self.assertEqual([((), {'server': 'host', 'username': 'user'}), 'logout', 'close'], dummy_ssh.res)

    def test_send_command(self):
        command = "test command"
        dummy_ssh = DummyMockPxssh()
        RemoteServer.pxssh_session = dummy_ssh
        with RemoteServer("user", "host") as remote_server:
            remote_server.send_command(command)
        self.assertEqual(
            [((), {'server': 'host', 'username': 'user'}), 'test command', 'prompt', 'before', 'logout', 'close'],
            dummy_ssh.res)

    def tearDown(self):
        self.clear_up()
