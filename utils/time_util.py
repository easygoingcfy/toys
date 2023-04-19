import re
import time
import datetime


def str2timestamp(s, fmt="%Y-%m-%d %H:%M:%S"):
    timeArray = time.strptime(s, fmt)
    timestamp = time.mktime(timeArray)
    return timestamp


def timestamp2str(timestamp, fmt="%Y-%m-%d %H:%M:%S"):
    d = datetime.datetime.fromtimestamp(timestamp)
    str1 = d.strftime(fmt)
    return str1


def timestr2str(timestr, fmt, to_fmt="%Y-%m-%d %H:%M:%S"):
    timestamp = str2timestamp(timestr, fmt)
    return timestamp2str(timestamp, to_fmt)

def today(fmt="%Y-%m-%d"):
    now = time.time()
    return timestamp2str(now, fmt)


def ts_range_by_date(date):
    if not isinstance(date, str):
        date = str(date)
    date = re.search("\d{4}-\d{2}-\d{2}", date).group()
    date_st = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_en = date_st + datetime.timedelta(days=1, seconds=0)
    return date_st.timestamp(), date_en.timestamp()