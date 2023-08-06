import collections


def compare_list2(list1, list2):
    """
    No Matter order if list1 and list2 contains same element then return True

    """
    a = list_check(list1)
    b = list_check(list2)
    res = collections.Counter(a) == collections.Counter(b)
    return res


def list_check(list_value):
    if type(list_value) is tuple:
        list_value = list(list_value)
    list_value = ["" if x is None else str(x) for x in list_value]

    return list_value


def compare_list(list1, list2):
    """
    To test two list are same or not if they are same then return True
    if they are not same return false but if list1 contain some value doesn't exist in
    list 2 then return the value exist in both list.
    """
    a = list_check(list1)
    b = list_check(list2)
    counter1 = collections.Counter(a)
    counter2 = collections.Counter(b)

    res1 = counter2 - counter1
    res2 = counter1 - counter2

    if res2:
        return list(counter1 - res2)
    else:
        if not res1:
            return True
        else:
            return False


def list_common_element(list1, list2, case_sensitive=False):
    """Given two lists and return a new list with common element of two list, the element comes from the first list
    """
    new_list = []

    for item1 in list1:
        for item2 in list2:
            if case_sensitive:
                if item1 == item2:
                    new_list.append(item1)
            else:

                if str(item1).lower() == str(item2).lower():
                    new_list.append(item1)
    return new_list
