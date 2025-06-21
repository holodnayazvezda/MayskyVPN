import time
from datetime import datetime


def unix_to_date(unix_timestamp):
    date = datetime.fromtimestamp(unix_timestamp / 1000)
    return date.strftime("%d.%m.%Y")


def calculate_remaining_time(unix_timestamp):
    current_time = int(time.time() * 1000)
    total_hours = (unix_timestamp - current_time) // (1000 * 60 * 60)
    days = total_hours // 24
    hours = total_hours % 24
    return days, hours


def is_expired(unix_timestamp):
    current_time = int(time.time() * 1000)
    return unix_timestamp < current_time
