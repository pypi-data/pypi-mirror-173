import unittest
import os
import shutil
import warnings
import json
from app_common.config import ConfigHandler
from app_common.config.config_handler import load_yml_from_path
from app_common.config.config_handler import dump_yml_to_path
from app_common.config.config_handler import setting_file_path_validation
from app_common.config import DjangoConfigAgent, ConfigAgent
from app_common.utilities.file_prepare import check_create_dir


class DatasetIDGenerateFunctionTest(unittest.TestCase):
    def setUp(self):
        self.output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        self.setting_dir_name = "passwd"
        self.setting_file_name = "pw_info.yml"
        self.setting_path = os.path.join(*[self.output_path, self.setting_dir_name, self.setting_file_name])
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.config_obj = ConfigHandler(
            self.setting_path,
            os.path.join(*[current_path, "resource", "default_setting.yml-tpl"]),
            'default_django_setting.yml-tpl')
        self.tpl_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource")

    def test_create_the_config_handler_obj(self):
        ...

    def test_load_default_yml_tpl(self):
        yml_dict = self.config_obj.load_default_yml_template()
        self.assertEqual(yml_dict["general_info"]["ENVIRONMENT"], "ENVIRONMENT")

    def test_yml_templates_with_no_overlap(self):
        # load real template and merge
        # Test template merge with no overlap template
        default_yml_dict = self.config_obj.load_default_yml_template()
        tpl_path = os.path.join(self.tpl_dir_path, 'default_setting.yml-tpl')
        user_yml_template = load_yml_from_path(tpl_path)
        merged_yml = self.config_obj.merge_yml(default_yml_dict, user_yml_template)
        expected_yml = {
            "bugs": {
                "USER": "",
                "HOST": "",
                "SLOCUM_DELAY_BINARY_DATA_DIR": "",
                "SLOCUM_LIVE_BINARY_DATA_DIR": "",
                "WEB_HOOK_TOKEN": "",
            },
            "general_info": {
                "ENVIRONMENT": "ENVIRONMENT",
            },
            "django_settings": {
                "SECRET_KEY": "SECRET_KEY",
            }
        }
        self.assertEqual(expected_yml, merged_yml)

    def test_merge_yml_templates_with_overlap(self):
        # Test template merge with overlap template
        default_yml_dict = self.config_obj.load_default_yml_template()
        tpl_path2 = os.path.join(self.tpl_dir_path, 'user_setting1.yml')
        user_yml_template2 = load_yml_from_path(tpl_path2)
        merged_yml2 = self.config_obj.merge_yml(default_yml_dict, user_yml_template2)
        expected_yml2 = {
            "bugs": {
                "USER": "",
                "HOST": "",
                "SLOCUM_DELAY_BINARY_DATA_DIR": "",
                "SLOCUM_LIVE_BINARY_DATA_DIR": "",
                "WEB_HOOK_TOKEN": "",
            },
            "general_info": {
                "ENVIRONMENT": "ENVIRONMENT",
                "SECRET_KEY": "",
            },
            "django_settings": {
                "SECRET_KEY": "SECRET_KEY",
            }
        }
        self.assertEqual(expected_yml2, merged_yml2)

    def test_yml_templates_with_overlap_with_value(self):
        default_yml_dict = self.config_obj.load_default_yml_template()
        tpl_path2 = os.path.join(self.tpl_dir_path, 'user_setting2.yml')
        user_yml_template2 = load_yml_from_path(tpl_path2)
        merged_yml2 = self.config_obj.merge_yml(default_yml_dict, user_yml_template2)
        expected_yml2 = {
            "bugs": {
                "USER": "the_user",
                "HOST": "the_host",
                "SLOCUM_DELAY_BINARY_DATA_DIR": "the_data_dir",
                "SLOCUM_LIVE_BINARY_DATA_DIR": "the_data_dir",
                "WEB_HOOK_TOKEN": "git",
            },
            "general_info": {
                "ENVIRONMENT": "ENVIRONMENT",
                "SECRET_KEY": "key_keys",
            },
            "django_settings": {
                "SECRET_KEY": "SECRET_KEY",
            }
        }
        self.assertEqual(expected_yml2, merged_yml2)

    def test_compare_yaml_dict_simple_for_same(self):
        test_dict1 = {
            "valur": "a"
        }
        self.assertEqual(False, self.config_obj.is_yaml_dict_different(test_dict1, test_dict1))

    def test_compare_yaml_simple_for_different(self):
        test_dict1 = {
            "value": "a",
            "value2": "b"
        }
        test_dict2 = {
            "value": "a",
            "value3": "d"
        }
        self.assertEqual(True, self.config_obj.is_yaml_dict_different(test_dict1, test_dict2))

    def test_compare_yaml_dict_complex_for_same(self):
        test_dict1 = {
            "value": "a",
            "value2": {
                "value3": 1,
                "value4": [1, 2],
                "value": "a",
                "value5": {
                    "value1": 2
                }
            }
        }
        self.assertEqual(False, self.config_obj.is_yaml_dict_different(test_dict1, test_dict1))

    def test_compare_yaml_dict_complex_for_different(self):
        test_dict1 = {
            "value": "a",
            "value2": {
                "value3": 1,
                "value4": [1, 2],
                "value": "a",
                "value5": {
                    "value1": 2
                }
            }
        }
        test_dict2 = {
            "value": "a",
            "value2": {
                "value3": 1,
                "value4": [1, 2],
                "value": "c",
                "value6": {
                    "value1": 2
                }
            }
        }
        self.assertEqual(True, self.config_obj.is_yaml_dict_different(test_dict1, test_dict2))

    def test_build_or_load_no_setting_file(self):
        try:
            self.config_obj.build_or_load()
        except FileNotFoundError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_build_or_load_with_existing_incomplete_setting_file(self):
        passwd = check_create_dir(os.path.join(self.output_path, self.setting_dir_name))
        setting_path = os.path.join(passwd, self.setting_file_name)
        example_yaml_dict = {
            "value": "a"
        }
        dump_yml_to_path(setting_path, example_yaml_dict)
        try:
            self.config_obj.build_or_load()
        except (ValueError, AttributeError):
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_build_or_load_with_existing_correct_setting_file(self):
        passwd = check_create_dir(os.path.join(self.output_path, self.setting_dir_name))
        setting_path = os.path.join(passwd, self.setting_file_name)
        example_yaml_dict = {
            "bugs": {
                "USER": "",
                "HOST": "",
                "SLOCUM_DELAY_BINARY_DATA_DIR": "",
                "SLOCUM_LIVE_BINARY_DATA_DIR": "",
                "WEB_HOOK_TOKEN": ""
            },
            "general_info": {
                "ENVIRONMENT": 'ENVIRONMENT',
            },
            "django_settings": {
                "SECRET_KEY": "SECRET_KEY",
            }
        }
        dump_yml_to_path(setting_path, example_yaml_dict)
        try:
            self.config_obj.build_or_load()
        except ValueError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_build_or_load_with_existing_correct_setting_file2(self):
        passwd = check_create_dir(os.path.join(self.output_path, self.setting_dir_name))
        setting_path = os.path.join(passwd, self.setting_file_name)
        example_yaml_dict = {
            "general_info": {
                "ENVIRONMENT": 'ENVIRONMENT',
            },
            "bugs": {
                "USER": "",
                "HOST": "",
                "SLOCUM_DELAY_BINARY_DATA_DIR": "",
                "SLOCUM_LIVE_BINARY_DATA_DIR": "",
                "WEB_HOOK_TOKEN": ""
            },
            "django_settings": {
                "SECRET_KEY": "SECRET_KEY",
            }
        }
        dump_yml_to_path(setting_path, example_yaml_dict)
        try:
            self.config_obj.build_or_load()
        except ValueError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_merge_yml_file(self):
        # make sure merged toward yml file doesn't change it's orignial value
        user_setting2 = os.path.join(self.tpl_dir_path, 'user_setting2.yml')
        user_setting3 = os.path.join(self.tpl_dir_path, 'user_setting3.yml')
        u2 = load_yml_from_path(user_setting2)
        u3 = load_yml_from_path(user_setting3)
        u2["general_info"]["SOME_THING"] = "2"

        merged = self.config_obj.merge_yml(u3, u2)
        self.assertEqual(u2, merged)

    def test_build_or_load_with_existing_incomplete_setting_file2(self):
        passwd = check_create_dir(os.path.join(self.output_path, self.setting_dir_name))
        setting_path = os.path.join(passwd, self.setting_file_name)
        example_yaml_dict = {
            "bugs": {
                "USER": "",
                "HOST": "",
                "SLOCUM_DELAY_BINARY_DATA_DIR": "",
                "SLOCUM_LIVE_BINARY_DATA_DIR": "",
                "WEB_HOOK_TOKEN": ""
            }
        }
        dump_yml_to_path(setting_path, example_yaml_dict)
        try:
            self.config_obj.build_or_load()
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_build_or_load_with_existing_more_setting_file(self):
        passwd = check_create_dir(os.path.join(self.output_path, self.setting_dir_name))
        setting_path = os.path.join(passwd, self.setting_file_name)
        example_yaml_dict = {
            "bugs": {
                "USER": "",
                "HOST": "",
                "SLOCUM_DELAY_BINARY_DATA_DIR": "",
                "SLOCUM_LIVE_BINARY_DATA_DIR": "",
                "WEB_HOOK_TOKEN": ""
            },
            "general_info": {
                "ENVIRONMENT": 'ENVIRONMENT',
                'Something': "extra",
            },
            "django_settings": {
                "SECRET_KEY": "SECRET_KEY",
            }
        }
        dump_yml_to_path(setting_path, example_yaml_dict)
        try:
            self.config_obj.build_or_load()
        except ValueError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_build_or_load_with_envir_variable(self):

        example_yaml_dict = {
            "bugs": {
                "USER": "",
                "HOST": "",
                "SLOCUM_DELAY_BINARY_DATA_DIR": "",
                "SLOCUM_LIVE_BINARY_DATA_DIR": "",
                "WEB_HOOK_TOKEN": ""
            },
            "general_info": {
                "ENVIRONMENT": 'ENVIRONMENT',
                'Something': "extra",
            },
            "django_settings": {
                "SECRET_KEY": "SECRET_KEY",
            }
        }
        os.environ.setdefault("bugs", json.dumps({
            "USER": "",
            "HOST": "",
            "SLOCUM_DELAY_BINARY_DATA_DIR": "",
            "SLOCUM_LIVE_BINARY_DATA_DIR": "",
            "WEB_HOOK_TOKEN": ""
        }))
        os.environ.setdefault("general_info", json.dumps({
            "ENVIRONMENT": 'ENVIRONMENT',
            'Something': "extra",
        }))
        os.environ.setdefault("django_settings", json.dumps({
            "SECRET_KEY": "SECRET_KEY",
        }))
        setting_path = ""
        self.config_obj.setting_path = setting_path

        res = self.config_obj.build_or_load()
        self.assertEqual(example_yaml_dict, res)

    def test_setting_file_path_validation(self):
        try:
            setting_file_path_validation(self.setting_path)
        except ValueError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

        try:
            setting_file_path_validation(self.output_path)
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_unchanged_field(self):
        passwd = check_create_dir(os.path.join(self.output_path, self.setting_dir_name))
        setting_path = os.path.join(passwd, self.setting_file_name)
        example_yaml_dict = {
            "bugs": {
                "USER": "",
                "HOST": "",
                "SLOCUM_DELAY_BINARY_DATA_DIR": "",
                "SLOCUM_LIVE_BINARY_DATA_DIR": "",
                "WEB_HOOK_TOKEN": "WEB_HOOK_TOKEN"
            },
            "general_info": {
                "ENVIRONMENT": 'ENVIRONMENT',
            },
            "django_settings": {
                "SECRET_KEY": "SECRET_KEY",
            }
        }
        dump_yml_to_path(setting_path, example_yaml_dict)
        self.config_obj.build_or_load()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.config_obj.build_or_load()
            assert len(w) == 1
            assert "SECRET_KEY" in str(w[-1].message)
            assert "ENVIRONMENT" in str(w[-1].message)

    def tearDown(self):
        self.output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        for the_file in os.listdir(self.output_path):
            file_path = os.path.join(self.output_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)


class ConfigAgentFunctionTest(unittest.TestCase):
    def setUp(self):
        self.agent = DjangoConfigAgent()
        self.agent2 = ConfigAgent()
        self.output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        self.resource = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource")
        self.setting_path = os.path.join(self.resource, "passwd/pw_info.yml")
        self.tpl_path = os.path.join(self.resource, 'default_setting.yml-tpl')

    def test_load(self):
        self.agent.load(self.setting_path, self.tpl_path)
        self.assertTrue(hasattr(self.agent, 'general_info'))
        self.assertTrue(hasattr(self.agent, 'bugs'))

    def test_DEBBUG_value_for_prod(self):
        self.agent.load(self.setting_path, self.tpl_path)
        self.assertEqual(False, self.agent.DEBUG)

    def test_DEBUG_value_before_load(self):
        self.assertEqual(True, self.agent.DEBUG)


if __name__ == '__main__':
    unittest.main()
