import platform
import os
from setuptools import setup, find_packages

path_to_my_project = os.path.dirname(__file__)  # Do any sort of fancy resolving of the path here if you need to

if platform.system().lower() == 'windows':
    install_requires = [
        f"twisted @ file://localhost/{path_to_my_project}/Twisted-22.4.0-py3-none-any.whl",
        "pytz",
        "netCDF4",
        "pandas",
        "PyYAML",
        "pexpect",
        "mysql-connector-python",
        "erddapy"
    ]
else:
    install_requires = [
        "pytz",
        "netCDF4",
        "pandas",
        "PyYAML",
        "pexpect",
        "mockssh",
        "mysql-connector-python",
        "erddapy",
        "urllib3"
    ]

setup(name='app_common',
      version='1.0.8',
      description="Common python and django application tools",
      author="CEOTR",
      author_email="support@ceotr.ca",
      url="https://gitlab.oceantrack.org/ceotr/app_common.git",
      packages=find_packages(exclude=['tests']).append('.twisted_iocpsupport-1.0.2-pp38-pypy38_pp73-win_amd64.whl'),
      package_data={'': ['*.yml-tpl', 'cf-standard-name-table.xml']},
      include_package_data=True,
      python_requires='>=3.5',
      license="GNU General Public License v3 (GPLv3)",
      install_requires=install_requires,
      zip_safe=True
      )
