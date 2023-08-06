import os


def is_sudo_user():
    """return True if script is triggered by a super user"""
    uid = os.getuid() if hasattr(os, 'getuid') else 65535
    gid = os.getgid() if hasattr(os, 'getgid') else 65535
    euid = os.geteuid() if hasattr(os, 'geteuid') else 65535
    egid = os.getegid() if hasattr(os, 'getegid') else 65535

    return not uid or not gid or not euid or not egid


