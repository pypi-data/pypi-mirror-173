import unittest

from app_common.utilities.list_compare import compare_list


class TestCompareList(unittest.TestCase):
    def setUp(self):
        self.list1 = ['1', '2', '3']
        self.list2 = ['1', '2', '3']
        self.list3 = ['1', '2', '3', '4']
        self.list4 = ['2', '3']
        self.list5 = ['7', '8']
        self.list6 = ['']

    def test_compare_list(self):
        """
        equal list return true
        :return:
        """
        res = compare_list(self.list1, self.list2)
        self.assertEqual(res, True)

    def test_compare_list2(self):
        """
        not equal list and list2 contain list1,
        return false
        :return:
        """
        res = compare_list(self.list1, self.list3)
        self.assertEqual(res, False)

    def test_compare_list3(self):
        res = compare_list(self.list5, self.list3)
        self.assertEqual(res, [])

    def test_compare_list4(self):
        res = compare_list(self.list6, self.list3)
        self.assertEqual(res, [])

    def test_compare_list5(self):
        res = compare_list(self.list1, self.list4)
        self.assertEqual(res, ['2', '3'])
