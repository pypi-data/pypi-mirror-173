"""You can find time relate function here"""

import time
import datetime
import logging

from pytz import timezone

logger = logging.getLogger(__file__)


def timeit(method):
    """
    credit to:
    https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d
    Use as decorator to measure a function running time
    """

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            logger.debug('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def time_zone_replace(time_str_or_time_object, time_zone='UTC'):
    """
    This function can convert time str to datetime object and replace its time zone to make Django happen
    enter None return None. default time zoom is UTC
    """
    if time_str_or_time_object:
        t = type(time_str_or_time_object)
        if t is str:
            et = datetime.datetime.strptime(time_str_or_time_object, "%Y-%m-%d %H:%M:%S")
        else:
            et = time_str_or_time_object
        time_str_or_time_object = et.replace(tzinfo=timezone(time_zone))
    return time_str_or_time_object


def time_to_str(time_str, time_str_format="%Y-%m-%d %H:%M:%S"):
    """Given time str return datetime object
    Given None return None
    Given datetime object return itself
    other raise"""
    res = None
    if time_str:
        t = type(time_str)
        if t is not str:
            str_time = time_str.strftime(time_str_format)
            res = str_time
        elif t == datetime:
            res = time_str
        else:
            msg = "Input must be string or datetime object"
            raise ValueError(msg)
    return res


def str_to_timeobj(time_str, time_format='%Y-%m-%d %H:%M:%S'):
    """Convert time str to datetime object"""
    try:
        time_obj = datetime.datetime.strptime(time_str, time_format)
    except Exception as e:
        if type(time_str) is datetime:
            return time_str
        msg = "Input must be string or datetime object\ninput: {}".format(time_str)
        raise ValueError(msg)

    return time_obj


def str_to_timestamp(time_str, time_format='%Y-%m-%d %H:%M:%S'):
    """Convert time string to Unix timestamp"""
    time_obj = str_to_timeobj(time_str, time_format=time_format)
    time_stamp = time_obj.timestamp()
    return time_stamp


def timestamp_format_check(time_stamp):
    # This is a bad solution
    if type(time_stamp) is str:
        time_stamp = float(time_stamp)

    if time_stamp > 9999999999:
        time_stamp = time_stamp / 1000.0

    return time_stamp


def time_comparison(first_time, second_time):
    if type(first_time) is float:
        first_time_obj = first_time
    else:
        first_time_obj = str_to_timeobj(first_time)
    if type(second_time) is float:
        second_time_obj = second_time
    else:
        second_time_obj = str_to_timeobj(second_time)
    if first_time_obj == second_time_obj:
        return 0
    if first_time_obj > second_time_obj:
        # first time is later than second time
        return 1
    if first_time_obj < second_time_obj:
        # first time is earlier than second time
        return -1


def convert_to_erddap_time_format(time_str):
    """
    accept time format like:
        2019-03-12 14:55:02
    convert it to
        2019-03-12T14:55:02Z

    if input was None, return None
    """
    ret_time_str = None
    if time_str and type(time_str) is str:
        ret_time_str = time_str.lstrip(' ')
        ret_time_str = ret_time_str.rstrip(' ')
        ret_time_str = ret_time_str.replace(" ", 'T')
        ret_time_str = ret_time_str + 'Z'
    return ret_time_str


def seconds_to_days_hours_minutes_seconds(seconds):
    """Given second and then convert it into day hour minutes and second"""
    days = 0
    hours = 0
    minutes = 0
    if seconds < 60:
        n_seconds = seconds
    else:
        minutes = int(seconds / 60)
        n_seconds = seconds - minutes * 60
        if minutes > 60:
            hours = int(minutes / 60)
            minutes = minutes - hours * 60
            if hours > 24:
                days = int(hours / 24)
                hours = hours - days * 24

    return days, hours, minutes, n_seconds


def time_period_overlap(start_time1, end_time1, start_time2, end_time2):
    """Check to see if time period 1 and time period 2 have overlap,
    return true if they have overlap and false they does not

    :param start_time1: datetime obj of start time of time period 1
    :param end_time1:  datetime obj of end time of time period 1
    :param start_time2: datetime obj of start time of time period 2
    :param end_time2: datetime obj of start time of time period 2
    :return: True means they have overlap and False means they have no overlap
    """

    def none_or_datetime(time_obj):
        if time_obj is None or type(time_obj) is datetime.datetime:
            return True
        return False

    if not (type(start_time1) is datetime.datetime and none_or_datetime(end_time1) and
            type(start_time2) is datetime.datetime and none_or_datetime(end_time2)):
        msg = "start_time must be datetime obj end_time must be datetime obj or None" \
              "\nstart_time1: {}\nend_time1: {}\nstart_time2: {}\nend_time2: {}".format(
            start_time1, end_time1, start_time2, end_time2)
        raise ValueError(msg)

    if end_time1 is not None and end_time2 is not None:
        if end_time1 <= start_time2:
            return False
        elif end_time2 <= start_time1:
            return False
        else:
            return True
    elif end_time1 is None and end_time2 is not None:
        if start_time1 >= end_time2:
            return False
    elif end_time1 is not None and end_time2 is None:
        if start_time2 >= end_time1:
            return False
    return True
