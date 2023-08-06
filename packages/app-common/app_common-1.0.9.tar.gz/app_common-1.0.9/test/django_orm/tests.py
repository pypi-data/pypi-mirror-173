import sys
import unittest
from unittest import TestCase
from app_common.django_orm.django_orm import (
    setting_content_validation,
    database_config_validation_and_proxy,
    module_database_config_replace_adapter
)


class TestDjangoOrmInitFunctions(TestCase):
    def setUp(self):
        self.DATABASE = {
            "default": {
                "ENGINE": "",
                "NAME": "",
                "USER": "",
                "PASSWORD": "",
                "HOST": ""
            }
        }
        self.INSTALLED_APPS = ["general"]
        self.invalid_input = [1, 2, 3]

        class TestSetting:
            def __init__(self, DATABASE, INSTALLED_APPS):
                self.DATABASES = DATABASE
                self.INSTALLED_APPS = INSTALLED_APPS

        self.object_input = TestSetting(self.DATABASE, self.INSTALLED_APPS)

        self.dict_input = {
            "DATABASES": self.DATABASE,
            "INSTALLED_APPS": self.INSTALLED_APPS
        }

    def test_setting_variable_format(self):
        try:
            setting_content_validation(self.invalid_input)
        except AttributeError:
            self.assertTrue(True)
        else:
            assert False

        try:
            setting_content_validation(self.object_input)
        except AttributeError:
            self.assertTrue(False)
        else:
            assert True

        try:
            setting_content_validation(self.dict_input)
        except AttributeError:
            self.assertTrue(False)
        else:
            assert True

    def test_database_variable_format_validation_and_proxy(self):
        dataset_config1 = {
            'default': {
                'ENGINE': 'django.db.backends.oracle',
                'NAME': 'xe',
                'USER': 'a_user',
                'PASSWORD': 'a_password',
                'HOST': '',
                'PORT': '',
            }
        }
        try:
            database_config_validation_and_proxy(dataset_config1)
        except AttributeError:
            assert False
        else:
            assert True

        dataset_config2 = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'xe',
            }
        }
        try:
            database_config_validation_and_proxy(dataset_config2)
        except AttributeError:
            assert False
        else:
            assert True

        dataset_config3 = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'xe',
            }
        }
        try:
            database_config_validation_and_proxy(dataset_config3)
        except AttributeError:
            assert True
        else:
            assert False

    def test_module_database_config_replace_adapter(self):
        MODULE_NAME = "app_common.django_orm.orm_config"
        sample_dataset_config1 = {
            'default': {
                'ENGINE': 'django.db.backends.oracle',
                'NAME': 'xe',
                'USER': 'a_user',
                'PASSWORD': 'a_password',
                'HOST': '',
                'PORT': '',
            }
        }
        if MODULE_NAME in sys.modules:
            assert True
        else:
            assert False

        self.assertNotEqual(sys.modules[MODULE_NAME], sample_dataset_config1)
        sample_dataset_config1 = database_config_validation_and_proxy(sample_dataset_config1)
        module_database_config_replace_adapter(sample_dataset_config1)
        res_dataset_config = sys.modules[MODULE_NAME].DATABASES["default"]
        self.assertEqual(res_dataset_config, sample_dataset_config1)




if __name__ == '__main__':
    unittest.main()
