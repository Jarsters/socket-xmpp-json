import time, datetime

def get_timestamp():
    return int(time.time() * 1000)

def see_in_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')