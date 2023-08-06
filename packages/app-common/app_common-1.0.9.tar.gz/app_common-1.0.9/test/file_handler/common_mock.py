from pexpect import pxssh


class DummyMockPxssh:
    def __init__(self, success=True):
        self.res = []
        self.success = success

    def login(self, *args, **kwargs):
        self.res.append((args, kwargs))
        if not self.success:
            raise pxssh.ExceptionPxssh("connection fail")

    def logout(self):
        self.res.append("logout")

    def close(self):
        self.res.append("close")

    def sendline(self, command):
        self.res.append(command)

    def prompt(self):
        self.res.append("prompt")

    @property
    def before(self):
        self.res.append("before")
        return None
