import re
import time
import datetime


def str2timestamp(string, fmt="%Y-%m-%d %H:%M:%S"):
    return int(datetime.datetime.strptime(string, fmt).timestamp())


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
    date_en = datetime.datetime.combine(date_st, date_st.time().max)
    return int(date_st.timestamp()), int(date_en.timestamp())


def extract_date(string) -> str:
    date_str = re.search(r"(\d{4}).*?(\d{2}).*?(\d{2})", string).groups()
    return "-".join(date_str)

def extract_time(string) -> str:
    time_str = re.split(r'[ :/\-T年月日]', string)
    time_str = "".join(time_str)
    if len(time_str) != 14:
        time_str += "0" * (14 - len(time_str))
    return time_str


if __name__ == "__main__":
    extract_time("2023-02-11 20 49 23")