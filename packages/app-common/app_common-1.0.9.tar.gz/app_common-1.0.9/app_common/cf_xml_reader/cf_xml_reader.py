import os
from xml.etree.ElementTree import (
    parse as ETparse
)


class CFXMLReader:
    """
    convert the cf standard name xml into dictionary
    """

    def __init__(self, xml_path: str):
        self.tree = ETparse(xml_path)
        self.root = self.tree.getroot()
        self._dict = None

    @property
    def dict(self) -> dict:
        if self._dict is None:
            self.xml_to_dict()
        return self._dict

    def xml_to_dict(self) -> None:
        """
        convert xml to dict
        :return:
        """
        # convert entries to dict
        for entry in self.root.iter("entry"):
            if self._dict is None:
                self._dict = dict()
            standard_name = entry.attrib['id']
            self._dict[standard_name] = dict()
            content = list(entry)
            for i in content:
                self._dict[standard_name][i.tag] = i.text

        # convert alis to dict
        for alias in self.root.iter("alias"):
            standard_name = alias.attrib['id']
            for entry in alias:
                self._dict[standard_name] = self._dict[entry.text]


# the xml come from github repo version 78: https://github.com/cf-convention/cf-convention.github.io/blob/main/Data/cf-standard-names/78/src/cf-standard-name-table.xml

xml_name = "cf-standard-name-table.xml"
dir_path = os.path.dirname(__file__)
cf_xml_reader = CFXMLReader(os.path.join(dir_path, xml_name))
