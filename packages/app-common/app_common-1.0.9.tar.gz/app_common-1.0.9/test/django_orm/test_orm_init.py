import os
import shutil
from unittest import TestCase
from app_common.utilities.file_prepare import check_create_dir

from app_common.django_orm.django_orm import init_django_orm


def init_orm():
    setting = {
        "DATABASES": {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'output/testing_django_orm_database',
            'USER': 'xiang',
            'PASSWORD': '123',
            'HOST': 'localhost',
            'PORT': '', },
        "INSTALLED_APPS": ["test.django_orm.general"]
    }
    init_django_orm(setting)


class TestDjangoOrmInit(TestCase):
    def setUp(self):
        self.output_dir = os.path.join(*[os.path.dirname(os.path.realpath(__file__)), "output"])
        check_create_dir(self.output_dir)

    def test_django_orm_init(self):

        init_orm()
        from test.django_orm.general.models import Reader
        from django.db.utils import OperationalError
        try:
            list(Reader.objects.all())
        except OperationalError as e:
            self.assertTrue("general_reader" in e.args[0])
        self.assertTrue(os.path.isfile(os.path.join(self.output_dir, "testing_django_orm_database")))

    def tearDown(self):
        shutil.rmtree(self.output_dir)
