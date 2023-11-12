from app.config.constants import WEEKDAYS

def check_weekday(weekday):
    return weekday in WEEKDAYS


def check_start_time(time):
    if len(time) != 5:
        return False

    if time[2] != ':':
        return False

    hour, minute = time.split(':')

    if minute != "00":
        return False

    hour_found = False
    for hour_int in range(24):
        hour_str = str(hour_int)
        if len(hour_str) == 1:
            hour_str = "0" + hour_str

        if hour == hour_str:
            hour_found = True
            break

    if not hour_found:
        return False

    return True


def check_end_time(time):
    if len(time) != 5:
        return False

    if time[2] != ':':
        return False

    hour, minute = time.split(':')

    if minute != "00":
        return False

    hour_found = False
    for hour_int in range(1, 25):
        hour_str = str(hour_int)
        if len(hour_str) == 1:
            hour_str = "0" + hour_str

        if hour == hour_str:
            hour_found = True
            break

    if not hour_found:
        return False

    return True
