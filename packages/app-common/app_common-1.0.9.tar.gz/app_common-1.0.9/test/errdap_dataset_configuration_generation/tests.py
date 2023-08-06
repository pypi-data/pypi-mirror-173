import os
from app_common.test_common.base import TestBase
from app_common.errdap_dataset_configuration_editor.erddap_dataset_configure_parser import dataset_xml_parser, \
    header_matcher, end_matcher

from app_common.errdap_dataset_configuration_editor.dataset_xml_editor import ERDDAPDatasetXMLEditor


class TestErrdapXmlParser(TestBase):
    def setUp(self):
        self.expect_output_dir = os.path.join(os.path.dirname(__file__), "output")
        self.expect_resource_dir = os.path.join(os.path.dirname(__file__), "resource")
        self.sample_xml_file = os.path.join(self.expect_resource_dir, "errdap_xml_file.xml")
        self.sample_xml_file5 = os.path.join(self.expect_resource_dir, "errdap_xml_file2.xml")
        self.sample_xml_file2 = os.path.join(self.expect_resource_dir, "errdap_xml_file_raw.out")
        self.sample_xml_file3 = os.path.join(self.expect_resource_dir, "empty_file.xml")
        self.sample_xml_file4 = os.path.join(self.expect_resource_dir, "random_thing")

    def test_parse_file(self):
        res1 = dataset_xml_parser(self.sample_xml_file)
        res2 = dataset_xml_parser(self.sample_xml_file5)
        self.assertEqual(res1.strip(), res2.strip())

    def test_parse_file_contain_nothing(self):
        res1 = dataset_xml_parser(self.sample_xml_file3)
        self.assertEqual(res1, "")

    def test_parse_no_xml_file(self):
        res1 = dataset_xml_parser(self.sample_xml_file4)
        self.assertEqual(res1, "")

    def test_end_match(self):
        match_str = "</dataset>"
        self.assertTrue(end_matcher(match_str))

    def test_header_match1(self):
        match_str = "<dataset type=\"EDDTableFromNcFiles\" datasetID=\"datast_id\" active=\"true\">"
        self.assertTrue(header_matcher(match_str))

    def test_header_match2(self):
        match_str = "<dataset  datasetID=\"datast_id\" type=\"EDDTableFromNcFiles\" active=\"true\">"
        self.assertTrue(header_matcher(match_str))

    def test_header_match3(self):
        match_str = "<dataset active=\"true\" type=\"EDDTableFromNcFiles\" datasetID=\"datast_id\" >"
        self.assertTrue(header_matcher(match_str))

    def test_header_match4(self):
        match_str = "<dataset active=\"false\" type=\"EDDTableFromNcFiles\" datasetID=\"datast_id\" >"
        self.assertTrue(header_matcher(match_str))


class TestDatasetXmlEditor(TestBase):
    def setUp(self):
        self.expect_output_dir = os.path.join(os.path.dirname(__file__), "output")
        self.expect_resource_dir = os.path.join(os.path.dirname(__file__), "resource")
        self.sample_xml_file = os.path.join(self.expect_resource_dir, "errdap_xml_file.xml")
        self.sample_xml_file2 = os.path.join(self.expect_resource_dir, "xml_to_string_res.xml")
        self.maxDiff = None

        xml_str = dataset_xml_parser(self.sample_xml_file2)
        xml_str2 = dataset_xml_parser(self.sample_xml_file)
        self.editor = ERDDAPDatasetXMLEditor(xml_str)
        self.editor2 = ERDDAPDatasetXMLEditor(xml_str2)

    def test_xml_edit_header_alter_attribute_(self):
        self.editor.set_header("datasetID", "new_dataset_id")
        output_path = os.path.join(self.expect_output_dir, "out")

        # set int
        self.editor.set_attr("reloadEveryNMinutes", 12345)
        # set str
        self.editor.set_attr("fileDir", "/my/path/")
        # set no exist
        self.editor.set_attr("some_attr", "no important")
        # remove attr
        self.editor.remove_attr("preExtractRegex")
        self.editor.remove_attr("postExtractRegex")
        self.editor.remove_attr("extractRegex")
        self.editor.remove_attr("columnNameForExtract")
        self.editor.write(os.path.join(output_path))
        with open(output_path, 'r') as f:
            out_content = f.read()

        with open(os.path.join(self.resource_dir, "expected_xml_string_header_attr_change.xml"), 'r') as f:
            expected_content = f.read()

        self.assertEqual(expected_content.replace("\n", ""), out_content.replace("\n", ""))

    def test_xml_set_added_attr(self):
        output_path = os.path.join(self.expect_output_dir, "out")
        self.editor.set_added_attr("test", "example")
        self.editor.set_added_attr("cdm_profile_variables", "example")
        self.editor.set_added_attr("cdm_trajectory_variables", "example")
        self.editor.remove_added_attr("creator_name")
        self.editor.write(os.path.join(output_path))
        with open(output_path, 'r') as f:
            out_content = f.read()

        with open(os.path.join(self.resource_dir, "expected_xml_addedAttribute_res.xml"), 'r') as f:
            expected_content = f.read()

        self.assertEqual(expected_content.replace("\n", "").replace(" ", ""),
                         out_content.replace("\n", "").replace(" ", ""))

    def test_xml_get_header(self):
        n = self.editor.get_header()
        expected_dict = {
            'type': 'EDDTableFromNcFiles',
            'datasetID': '1557432033_2426023_0a86_8c8c_12d2',
            'active': 'true'
        }
        self.assertEqual(n, expected_dict)

    def test_remove_data_variable(self):
        output_path = os.path.join(self.expect_output_dir, "out")
        self.editor.remove_data_variable("m_water_depth")
        self.editor.write(os.path.join(output_path))

        self.editor.write(os.path.join(output_path))
        with open(output_path, 'r') as f:
            out_content = f.read()

        with open(os.path.join(self.resource_dir, "expected_xml_remove_from_data_variables.xml"), 'r') as f:
            expected_content = f.read()

        self.assertEqual(expected_content.replace("\n", "").replace(" ", ""),
                         out_content.replace("\n", "").replace(" ", ""))

    def test_set_data_variable_add_attribute(self):
        output_path = os.path.join(self.expect_output_dir, "out")
        self.editor.set_data_variable_add_attribute("m_water_depth", "_ChunkSizes", "something")
        self.editor.set_data_variable_add_attribute("m_water_depth", "test", "something")
        self.editor.write(os.path.join(output_path))
        with open(output_path, 'r') as f:
            out_content = f.read()

        with open(os.path.join(self.resource_dir, "expected_xml_set_data_variable_add_atrribute.xml"), 'r') as f:
            expected_content = f.read()

        self.assertEqual(expected_content.replace("\n", "").replace(" ", ""),
                         out_content.replace("\n", "").replace(" ", ""))

    def test_remove_data_variable_add_attribute(self):
        output_path = os.path.join(self.expect_output_dir, "out")
        self.editor.remove_data_variable_add_attribute("m_water_depth", "_ChunkSizes")
        self.editor.write(os.path.join(output_path))
        with open(output_path, 'r') as f:
            out_content = f.read()

        with open(os.path.join(self.resource_dir, "expected_xml_remove_data_variable_add_attribute.xml"), 'r') as f:
            expected_content = f.read()

        self.assertEqual(expected_content.replace("\n", "").replace(" ", ""),
                         out_content.replace("\n", "").replace(" ", ""))

    def test_edit_data_variable_destination_name(self):
        output_path = os.path.join(self.expect_output_dir, "out")
        self.editor.edit_data_variable_destination_name("m_water_depth", "something")
        self.editor.write(os.path.join(output_path))
        with open(output_path, 'r') as f:
            out_content = f.read()

        with open(os.path.join(self.resource_dir, "exected_edit_data_variable_desination_name.xml"), 'r') as f:
            expected_content = f.read()

        self.assertEqual(expected_content.replace("\n", "").replace(" ", ""),
                         out_content.replace("\n", "").replace(" ", ""))

    def test_edit_data_variable_data_type(self):
        output_path = os.path.join(self.expect_output_dir, "out")
        self.editor.edit_data_variable_data_type("m_water_depth", "int")
        self.editor.write(os.path.join(output_path))
        with open(output_path, 'r') as f:
            out_content = f.read()

        with open(os.path.join(self.resource_dir, "expected_edit_data_variable_data_type.xml"), 'r') as f:
            expected_content = f.read()

        self.assertEqual(expected_content.replace("\n", "").replace(" ", ""),
                         out_content.replace("\n", "").replace(" ", ""))

    def test_get_unit(self):
        units = self.editor2.get_unit()
        expected_result = {'m_water_depth': 'Celsius', 'conductivity': 'S.m-1', 'temperature': 'Celsius'}
        self.assertEqual(expected_result, units)