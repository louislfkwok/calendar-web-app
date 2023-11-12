from app.config.constants import WEEKDAYS

def get_left_bound(weekday):
    cnt = 1
    for WEEKDAY in WEEKDAYS:
        if weekday == WEEKDAY:
            return cnt
        cnt += 1


def get_right_bound(weekday):
    cnt = 2
    for WEEKDAY in WEEKDAYS:
        if weekday == WEEKDAY:
            return cnt
        cnt += 1


def get_bound(time):
    hour_part = time.split(":")[0]
    hour = int(hour_part)
    return hour + 1
