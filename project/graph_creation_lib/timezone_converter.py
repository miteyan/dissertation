from datetime import datetime
from pytz import timezone


def to_local_time(coords):
    tz = 'Europe/Berlin'
    local_now = datetime.now(timezone(tz))
    time_difference = local_now.utcoffset().total_seconds() / 60 / 60  # time difference between UTC and local timezones in 5:30:00 format
    return {'time_difference': time_difference}
    # to_local_time(coords = [39.9042, 116.4074])
